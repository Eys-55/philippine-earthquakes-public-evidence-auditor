#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { execFileSync, spawnSync } from "node:child_process";

const ROOT = path.resolve(process.env.TRACKER_ROOT || path.join(import.meta.dirname, ".."));
const VALID_RUN_STATUSES = new Set([
  "open",
  "waiting_on_user",
  "blocked",
  "completed",
  "handed_off",
  "abandoned",
]);
const TRACKER_COMMAND_SUITE = [
  {
    id: "tracker.status",
    adapter: "tracker-status",
    category: "status",
    purpose: "Read tracker-owned project, workstream, skill-run, and upload status before answering in Codex chat.",
    required_args: [],
  },
  {
    id: "tracker.upload_gate",
    adapter: "tracker-upload-gate",
    category: "closeout",
    purpose: "Verify live git cleanliness and remote upload truth before claiming the repo is synced.",
    required_args: [],
  },
  {
    id: "tracker.session_start",
    adapter: "tracker-session-start",
    category: "intake",
    purpose: "Create or lock a tracker session for a repo skill workflow before work continues.",
    required_args: ["project-id", "repo-id", "workstream-id", "objective"],
  },
  {
    id: "tracker.workflow_start",
    adapter: "tracker-workflow-start",
    category: "intake",
    purpose: "Create a skill-first workflow run with repo skill identity, phase skill, owned paths, and validation gates.",
    required_args: ["project-id", "session-id", "skill-id", "title", "flow-id", "current-skill", "owned-path", "validation-command", "next-action"],
  },
  {
    id: "tracker.workflow_checkpoint",
    adapter: "tracker-workflow-checkpoint",
    category: "checkpoint",
    purpose: "Record a durable workflow checkpoint without closing the skill run.",
    required_args: ["workflow-run-id", "next-action"],
  },
  {
    id: "tracker.workflow_close",
    adapter: "tracker-workflow-close",
    category: "closeout",
    purpose: "Close a skill run only after validation evidence and next-action state are recorded.",
    required_args: ["workflow-run-id", "next-action"],
  },
  {
    id: "tracker.validate",
    adapter: "validate-tracker",
    category: "validation",
    purpose: "Fail closed when tracker runs lack skill identity, context manifests, owned paths, or valid state.",
    required_args: [],
  },
  {
    id: "tracker.validate_all",
    adapter: "validate-all",
    category: "validation",
    purpose: "Run the repo tracker, inventory, progress-doc, and active-lane validators together.",
    required_args: [],
  },
  {
    id: "tracker.dashboard_export",
    adapter: "export-tracker-ui-data",
    category: "view",
    purpose: "Export read-only tracker data for the lightweight Astro tracker monitor.",
    required_args: [],
  },
  {
    id: "tracker.command_list",
    adapter: "tracker-command-list",
    category: "discovery",
    purpose: "List the callable tracker command suite available to Codex skills.",
    required_args: [],
  },
  {
    id: "tracker.command_describe",
    adapter: "tracker-command-describe",
    category: "discovery",
    purpose: "Describe one callable tracker command, including its adapter, skill ownership, and required args.",
    required_args: ["command"],
  },
];

function repoPath(...parts) {
  return path.join(ROOT, ...parts);
}

function rel(file) {
  return path.relative(ROOT, file).split(path.sep).join("/") || ".";
}

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, "utf8"));
}

function writeJson(file, value) {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, `${JSON.stringify(value, null, 2)}\n`);
}

function appendJsonl(file, value) {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.appendFileSync(file, `${JSON.stringify(value, Object.keys(value).sort())}\n`);
}

function parseArgs(argv) {
  const out = { _: [] };
  for (let i = 0; i < argv.length; i += 1) {
    const item = argv[i];
    if (!item.startsWith("--")) {
      out._.push(item);
      continue;
    }
    const key = item.slice(2);
    const next = argv[i + 1];
    if (!next || next.startsWith("--")) {
      out[key] = true;
    } else if (out[key] === undefined) {
      out[key] = next;
      i += 1;
    } else if (Array.isArray(out[key])) {
      out[key].push(next);
      i += 1;
    } else {
      out[key] = [out[key], next];
      i += 1;
    }
  }
  return out;
}

function required(args, key) {
  const value = args[key];
  if (typeof value !== "string" || !value.trim()) {
    throw new Error(`missing --${key}`);
  }
  return value.trim();
}

function many(args, key) {
  const value = args[key];
  const values = Array.isArray(value) ? value : value ? [value] : [];
  const cleaned = values.map((item) => String(item).trim()).filter(Boolean);
  if (cleaned.length === 0) throw new Error(`missing --${key}`);
  return [...new Set(cleaned)];
}

function records(payload, key) {
  return Array.isArray(payload[key]) ? payload[key].filter((item) => item && typeof item === "object") : [];
}

function expectedSkillPath(skillId) {
  return `skills/${skillId}/SKILL.md`;
}

function resolveSkillPath(skillId, explicitPath) {
  const candidate = explicitPath || expectedSkillPath(skillId);
  const expected = expectedSkillPath(skillId);
  if (candidate !== expected) {
    throw new Error(`skill_path must equal ${expected}`);
  }
  if (!fs.existsSync(repoPath(candidate))) {
    throw new Error(`missing skill file ${candidate}`);
  }
  return candidate;
}

function skillIdentityErrors(run) {
  const errors = [];
  if (typeof run.skill_id !== "string" || !run.skill_id.trim()) {
    errors.push(`${run.id}: missing skill_id`);
    return errors;
  }
  if (typeof run.skill_path !== "string" || !run.skill_path.trim()) {
    errors.push(`${run.id}: missing skill_path`);
    return errors;
  }
  const expected = expectedSkillPath(run.skill_id);
  if (run.skill_path !== expected) errors.push(`${run.id}: skill_path must equal ${expected}`);
  if (path.resolve(ROOT, run.skill_path) !== path.resolve(ROOT, expected)) errors.push(`${run.id}: skill_path escapes canonical skill path`);
  if (!fs.existsSync(repoPath(expected))) errors.push(`${run.id}: missing skill file ${expected}`);
  return errors;
}

function visibleText(value) {
  if (typeof value !== "string") return value;
  return value
    .replace(/python3\s+scripts\/[^\s,;]+/g, "current Node tracker adapter")
    .replace(/python3\s+-m\s+unittest\s+[^\s,;]+/g, "npm test")
    .replace(/scripts\/[A-Za-z0-9_/-]+\.py/g, "superseded internal adapter")
    .replace(/tests\/test_[A-Za-z0-9_/-]+\.py/g, "current Node regression tests")
    .replace(/validate_tracker\.py/g, "current Node tracker validation")
    .replace(/\/tracker workflow/g, "plain Codex chat workflow intake")
    .replace(/add new Python only for internal adapters, validators, UI export, or tests/g, "do not add Python; use skills plus the Node internal adapter");
}

function visibleValue(value) {
  if (typeof value === "string") return visibleText(value);
  if (Array.isArray(value)) return value.map(visibleValue);
  if (value && typeof value === "object") {
    return Object.fromEntries(Object.entries(value).map(([key, item]) => [key, visibleValue(item)]));
  }
  return value;
}

function trackerCommandRecords() {
  return TRACKER_COMMAND_SUITE.map((command) => ({
    ...command,
    skill_id: "control-repo-manager",
    skill_path: "skills/control-repo-manager/SKILL.md",
    operator_surface: "Codex chat plus repo skills",
    internal_only: true,
    user_runs_terminal: false,
  }));
}

function printJson(value) {
  console.log(JSON.stringify(value, null, 2));
}

function trackerCommandList(args) {
  const commands = trackerCommandRecords();
  if (args.json) {
    printJson({ commands });
    return 0;
  }
  console.log("# Callable Tracker Command Suite\n");
  console.log("Skills are the operator interface. Codex chat is the operator surface. The user never runs tracker scripts.\n");
  for (const command of commands) {
    console.log(`- ${command.id}: ${command.purpose}`);
    console.log(`  adapter: ${command.adapter}`);
    console.log(`  category: ${command.category}`);
  }
  return 0;
}

function trackerCommandDescribe(args) {
  const id = required(args, "command");
  const command = trackerCommandRecords().find((item) => item.id === id || item.adapter === id);
  if (!command) throw new Error(`unknown tracker command ${id}`);
  if (args.json) {
    printJson(command);
    return 0;
  }
  console.log(`# ${command.id}\n`);
  console.log(`Adapter: ${command.adapter}`);
  console.log(`Category: ${command.category}`);
  console.log(`Skill: ${command.skill_id} (${command.skill_path})`);
  console.log(`Internal only: ${command.internal_only}`);
  console.log(`Purpose: ${command.purpose}`);
  console.log(`Required args: ${command.required_args.length ? command.required_args.join(", ") : "none"}`);
  return 0;
}

function contextManifestErrors(run, manifestPath) {
  const errors = [];
  const text = fs.readFileSync(repoPath(manifestPath), "utf8");
  const markerGroups = [
    ["Loaded Context", "Loaded ECC Context"],
    ["Premise", "Premise Lock", "Current Premise"],
    ["Question", "First Context-Aware Question", "Next Question"],
  ];
  for (const group of markerGroups) {
    if (!group.some((marker) => text.includes(marker))) {
      errors.push(`${run.id}: context manifest missing marker ${group[0]}`);
    }
  }
  if (!text.includes(run.skill_id) && !text.includes(run.skill_path)) {
    errors.push(`${run.id}: context manifest missing repo skill identity`);
  }
  return errors;
}

function activeRun(status) {
  return ["open", "waiting_on_user", "blocked"].includes(status);
}

function intentRequiresWorkflowIntake(run) {
  const haystack = [
    run.title,
    run.next_action,
    run.flow_id,
    run.current_skill,
  ].filter(Boolean).join(" ").toLowerCase();
  const explicitWorkflowIntent = /\bworkflow\b/.test(haystack) && /\b(bug|problem|issue|intake|continue|continuation|router|flow)\b/.test(haystack);
  const editIntent = /\b(edit|change|fix|update|revise|work on|touch)\b/.test(haystack) && /\b(project|proj|lane|skill|workflow|earthquake)\b/.test(haystack);
  return explicitWorkflowIntent || editIntent;
}

function trackerState() {
  const projects = records(readJson(repoPath("ops/registry/projects.json")), "projects");
  const workstreams = records(readJson(repoPath("ops/registry/workstreams.json")), "workstreams");
  const projectIds = new Set(projects.map((item) => item.id));
  const sessionIds = new Set(workstreams.flatMap((item) => item.session_ids || []));
  return { projects, workstreams, projectIds, sessionIds };
}

function assertKnownProjectAndSession(projectId, sessionId) {
  const state = trackerState();
  if (!state.projectIds.has(projectId)) throw new Error(`unknown project_id ${projectId}`);
  if (!state.sessionIds.has(sessionId)) throw new Error(`unknown session_id ${sessionId}`);
}

function byId(items) {
  return new Map(items.filter((item) => typeof item.id === "string").map((item) => [item.id, item]));
}

function now() {
  return new Date().toISOString();
}

function dateStamp() {
  return new Date().toISOString().slice(0, 10);
}

function compactStamp() {
  return new Date().toISOString().replace(/[-:TZ.]/g, "").slice(0, 14);
}

function suffix() {
  return Math.random().toString(16).slice(2, 6).padEnd(4, "0");
}

function git(args) {
  return execFileSync("git", args, { cwd: ROOT, encoding: "utf8" }).trim();
}

function statusCounts() {
  const output = git(["status", "--porcelain=v1", "--untracked-files=all"]);
  let dirty = 0;
  let untracked = 0;
  for (const line of output.split("\n").filter(Boolean)) {
    if (line.startsWith("?? ")) untracked += 1;
    else dirty += 1;
  }
  return { dirty, untracked };
}

function remoteHead(branch) {
  const output = git(["ls-remote", "origin", `refs/heads/${branch}`]);
  return output.split(/\s+/)[0] || "";
}

function validateTrackerRoot() {
  const errors = [];
  const projectsPath = repoPath("ops/registry/projects.json");
  const reposPath = repoPath("ops/registry/repos.json");
  const workstreamsPath = repoPath("ops/registry/workstreams.json");
  const runsPath = repoPath("ops/registry/workflow-runs.json");
  const projectsPayload = readJson(projectsPath);
  const reposPayload = readJson(reposPath);
  const workstreamsPayload = readJson(workstreamsPath);
  const runsPayload = readJson(runsPath);
  const projects = records(projectsPayload, "projects");
  const repos = records(reposPayload, "repos");
  const workstreams = records(workstreamsPayload, "workstreams");
  const runs = records(runsPayload, "workflow_runs");
  const projectIds = new Set(projects.map((item) => item.id));
  const repoIds = new Set(repos.map((item) => item.id));
  const workstreamIds = new Set(workstreams.map((item) => item.id));
  const sessionIds = new Set();

  for (const project of projects) {
    for (const repoId of project.repos || []) {
      if (!repoIds.has(repoId)) errors.push(`${project.id}: unknown repo ${repoId}`);
    }
    for (const workstreamId of project.workstreams || []) {
      if (!workstreamIds.has(workstreamId)) errors.push(`${project.id}: unknown workstream ${workstreamId}`);
    }
  }
  for (const workstream of workstreams) {
    if (!projectIds.has(workstream.project_id)) errors.push(`${workstream.id}: unknown project_id ${workstream.project_id}`);
    if (!repoIds.has(workstream.repo_id)) errors.push(`${workstream.id}: unknown repo_id ${workstream.repo_id}`);
    for (const sessionId of workstream.session_ids || []) sessionIds.add(sessionId);
  }
  for (const run of runs) {
    if (!projectIds.has(run.project_id)) errors.push(`${run.id}: unknown project_id ${run.project_id}`);
    if (run.session_id && !sessionIds.has(run.session_id)) errors.push(`${run.id}: unknown session_id ${run.session_id}`);
    if (!VALID_RUN_STATUSES.has(run.status)) errors.push(`${run.id}: invalid status ${run.status}`);
    errors.push(...skillIdentityErrors(run));
    if (!Array.isArray(run.owned_paths) || run.owned_paths.length === 0) errors.push(`${run.id}: owned_paths must contain at least one entry`);
    if (run.skill_path && Array.isArray(run.owned_paths) && !run.owned_paths.includes(run.skill_path)) errors.push(`${run.id}: owned_paths must include skill_path ${run.skill_path}`);
    if (!Array.isArray(run.validation_commands) || run.validation_commands.length === 0) errors.push(`${run.id}: validation_commands must contain at least one entry`);
    const manifestPath = run.context_manifest_path || (run.artifacts || []).find((item) => typeof item === "string" && item.endsWith("-context.md"));
    if ((run.current_skill === "workflow_intake" || run.flow_id === "workflow_specific_bug" || intentRequiresWorkflowIntake(run)) && !manifestPath) {
      errors.push(`${run.id}: workflow intake requires context manifest`);
    }
    if (manifestPath && !fs.existsSync(repoPath(manifestPath))) {
      errors.push(`${run.id}: missing context manifest ${manifestPath}`);
    } else if (manifestPath && (run.current_skill === "workflow_intake" || run.flow_id === "workflow_specific_bug" || intentRequiresWorkflowIntake(run))) {
      errors.push(...contextManifestErrors(run, manifestPath));
    }
    if (activeRun(run.status) && run.current_skill === "workflow_intake" && manifestPath) {
      errors.push(`${run.id}: workflow_intake with context manifest must checkpoint to grilling before asking the user`);
    }
  }
  for (const folder of ["ops/sessions", "ops/workflow-runs"]) {
    if (!fs.existsSync(repoPath(folder))) continue;
    for (const file of fs.readdirSync(repoPath(folder), { recursive: true })) {
      const full = repoPath(folder, file);
      if (!fs.statSync(full).isFile() || !full.endsWith(".jsonl")) continue;
      fs.readFileSync(full, "utf8").split("\n").filter(Boolean).forEach((line, index) => {
        try {
          JSON.parse(line);
        } catch {
          errors.push(`${rel(full)}:${index + 1}: invalid JSONL`);
        }
      });
    }
  }
  return errors;
}

function validateTracker() {
  const errors = validateTrackerRoot();
  if (errors.length) {
    console.error(errors.map((error) => `- ${error}`).join("\n"));
    return 1;
  }
  console.log("tracker validation passed");
  return 0;
}

function validateInventory() {
  const inventoryPath = repoPath("data/project-surface-inventory.json");
  const inventory = readJson(inventoryPath);
  const errors = [];
  const warnings = [];
  const active = Array.isArray(inventory.active_current_projects) ? inventory.active_current_projects : [];
  if (inventory.user_stated_expected_current_project_count !== undefined && active.length !== inventory.user_stated_expected_current_project_count) {
    errors.push(`active project count mismatch: expected ${inventory.user_stated_expected_current_project_count}, inventory has ${active.length}`);
  }
  for (const project of active) {
    if (!project.slug) errors.push("active project missing slug");
    if (project.skill && !fs.existsSync(repoPath(project.skill))) errors.push(`${project.slug}: missing skill ${project.skill}`);
    for (const owned of project.owned_paths || []) {
      if (!fs.existsSync(repoPath(owned))) errors.push(`${project.slug}: owned path does not exist: ${owned}`);
    }
  }
  for (const surface of inventory.non_current_surfaces || []) {
    const existing = (surface.paths || []).filter((item) => fs.existsSync(repoPath(item)));
    if (existing.length) warnings.push(`${surface.slug}: ${surface.classification} still present with ${existing.length} path(s)`);
  }
  console.log(`validated inventory: ${rel(inventoryPath)}`);
  console.log(`active projects: ${active.length}`);
  if (warnings.length) console.log(`warnings:\n${warnings.map((w) => `- ${w}`).join("\n")}`);
  if (errors.length) {
    console.error(`errors:\n${errors.map((e) => `- ${e}`).join("\n")}`);
    return 1;
  }
  return 0;
}

function validateProgressDocs() {
  const chart = fs.readFileSync(repoPath("docs/plans/building-code-progress-chart.md"), "utf8");
  const table = fs.readFileSync(repoPath("docs/plans/building-code-progress-table.md"), "utf8");
  const html = fs.readFileSync(repoPath("reports/building-code-progress-view.html"), "utf8");
  const required = [
    "```mermaid",
    "graph TD",
    "Gate 1 Exact<br/>Building Identity",
    "Gate 4 Overclaim<br/>Audit",
  ];
  for (const phrase of required) {
    if (!chart.includes(phrase)) throw new Error(`progress chart missing ${phrase}`);
  }
  for (const phrase of ["1a. Place-lock tests | Archived", "2. Audit scope lock | Archived"]) {
    if (!table.includes(phrase)) throw new Error(`progress table missing ${phrase}`);
  }
  if (!html.includes('src="assets/building-code-progress-chart.svg"')) throw new Error("progress viewer missing SVG");
  return 0;
}

function validateBuildingCodeV2() {
  const base = repoPath("data/philippines-building-code-evidence-auditor-v2");
  const files = fs.readdirSync(base).filter((file) => file.endsWith(".json"));
  for (const file of files) readJson(path.join(base, file));
  const skill = fs.readFileSync(repoPath("skills/philippines-building-code-evidence-auditor-v2/SKILL.md"), "utf8");
  for (const phrase of ["NSCP / seismic design evidence", "Latest post-earthquake tag / status", "missing public evidence"]) {
    if (!skill.includes(phrase)) throw new Error(`V2 skill missing ${phrase}`);
  }
  return 0;
}

function buildDashboard() {
  const projectsPayload = readJson(repoPath("ops/registry/projects.json"));
  const workstreamsPayload = readJson(repoPath("ops/registry/workstreams.json"));
  const runsPayload = readJson(repoPath("ops/registry/workflow-runs.json"));
  const uploadPayload = readJson(repoPath("ops/sync/github-upload-state.json"));
  const workstreams = records(workstreamsPayload, "workstreams");
  const workstreamsById = byId(workstreams);
  const projects = records(projectsPayload, "projects").map((project) => ({
    id: project.id,
    title: project.title,
    status: project.status,
    owner_intent: project.owner_intent,
    current_goal: project.current_goal,
    workstreams: (project.workstreams || []).map((id) => workstreamsById.get(id)).filter(Boolean),
  }));
  const workflowRuns = records(runsPayload, "workflow_runs").map((run) => visibleValue(run));
  const trackerCommands = trackerCommandRecords();
  const trackedSkills = [...new Map(workflowRuns.filter((run) => run.skill_id && run.skill_path).map((run) => [run.skill_id, {
    id: run.skill_id,
    path: run.skill_path,
    open_runs: workflowRuns.filter((item) => item.skill_id === run.skill_id && ["open", "waiting_on_user", "blocked"].includes(item.status)).length,
    total_runs: workflowRuns.filter((item) => item.skill_id === run.skill_id).length,
  }])).values()].sort((a, b) => a.id.localeCompare(b.id));
  const uploadRepos = Object.entries(uploadPayload.repos || {}).map(([id, repo]) => ({ id, ...repo }));
  const statuses = new Set(uploadRepos.map((repo) => repo.status || "unknown"));
  const uploadStatus = statuses.size === 1 ? [...statuses][0] : statuses.has("pending_local_changes") ? "pending_local_changes" : "mixed";
  return {
    kind: "tracker_astro_monitor_dashboard",
    generated_at: latestTrackerTimestamp(projectsPayload, workstreamsPayload, runsPayload),
    source_root: ".",
    summary: {
      active_projects: projects.filter((project) => project.status === "active").length,
      tracked_skills: trackedSkills.length,
      tracker_commands: trackerCommands.length,
      workstreams: workstreams.length,
      workflow_runs: workflowRuns.length,
      open_workflow_runs: workflowRuns.filter((run) => ["open", "waiting_on_user", "blocked"].includes(run.status)).length,
      upload_status: uploadStatus,
      repos: uploadRepos.length,
    },
    projects,
    tracked_skills: trackedSkills,
    tracker_commands: trackerCommands,
    workflow_runs: workflowRuns,
    upload_repos: uploadRepos,
    non_projects: projectsPayload.non_projects || [],
  };
}

function latestTrackerTimestamp(...payloads) {
  const values = [];
  const visit = (value) => {
    if (typeof value === "string" && /^\d{4}-\d{2}-\d{2}T/.test(value)) values.push(value);
    else if (Array.isArray(value)) value.forEach(visit);
    else if (value && typeof value === "object") Object.values(value).forEach(visit);
  };
  payloads.forEach(visit);
  return values.sort().at(-1) || "unknown";
}

function exportDashboard(args) {
  const output = path.resolve(ROOT, args.output || "tracker-ui/src/data/tracker-dashboard.json");
  writeJson(output, buildDashboard());
  console.log(rel(output));
  return 0;
}

function trackerStatus() {
  const projectsPayload = readJson(repoPath("ops/registry/projects.json"));
  const workstreamsPayload = readJson(repoPath("ops/registry/workstreams.json"));
  const runsPayload = readJson(repoPath("ops/registry/workflow-runs.json"));
  const workstreams = records(workstreamsPayload, "workstreams");
  const runs = records(runsPayload, "workflow_runs");
  console.log("# Project Status\n");
  for (const project of records(projectsPayload, "projects").filter((item) => item.status === "active")) {
    console.log(`## ${project.title}`);
    console.log(`- ID: \`${project.id}\``);
    console.log(`- Status: ${project.status}`);
    console.log(`- Current goal: ${project.current_goal}`);
    for (const workstream of workstreams.filter((item) => item.project_id === project.id)) {
      console.log(`- Workstream \`${workstream.id}\`: ${workstream.status}; next action: ${workstream.next_action}`);
    }
    const projectRuns = runs.filter((run) => run.project_id === project.id);
    if (!projectRuns.length) console.log("- Skill Runs: none recorded");
    else {
      console.log("- Skill Runs:");
      for (const run of projectRuns) {
        console.log(`  - Skill \`${run.skill_id || "missing"}\` (${run.skill_path || "missing"}): \`${run.id}\` ${run.status} - ${visibleText(run.title)}; phase: ${run.current_skill}; next action: ${visibleText(run.next_action)}`);
      }
    }
    console.log("");
  }
  const uploadGate = trackerUploadGate({ quiet: true });
  console.log("## GitHub Upload State");
  console.log(`- market-research-agent-control: ${uploadGate === 0 ? "uploaded" : "pending"}`);
  return 0;
}

function trackerUploadGate(args = {}) {
  const repos = readJson(repoPath("ops/registry/repos.json"));
  const repo = records(repos, "repos")[0] || {};
  const branch = git(["rev-parse", "--abbrev-ref", "HEAD"]);
  const localHead = git(["rev-parse", "HEAD"]);
  const remote = remoteHead(branch);
  const counts = statusCounts();
  const uploaded = counts.dirty === 0 && counts.untracked === 0 && localHead === remote;
  const state = {
    schema_version: 1,
    generated_at: now(),
    repos: {
      [repo.id || "market-research-agent-control"]: {
        status: uploaded ? "uploaded" : "pending_local_changes",
        local_branch: branch,
        local_head: localHead,
        remote_branch: branch,
        remote_head: remote,
        dirty: counts.dirty > 0,
        dirty_file_count: counts.dirty,
        untracked_file_count: counts.untracked,
        last_verified_at: now(),
        verification_command: "node scripts/control-repo.mjs tracker-upload-gate",
      },
    },
  };
  if (args.write || args.record) writeJson(repoPath("ops/sync/github-upload-state.json"), state);
  if (!args.quiet) console.log(uploaded ? "uploaded to GitHub" : "local changes still need upload");
  return uploaded ? 0 : 1;
}

function sessionStart(args) {
  const projectId = required(args, "project-id");
  const repoId = required(args, "repo-id");
  const workstreamId = required(args, "workstream-id");
  const objective = required(args, "objective");
  const sessionId = `${compactStamp()}-${suffix()}`;
  const sessionPath = repoPath("ops/sessions", dateStamp(), `session-${sessionId}.jsonl`);
  appendJsonl(sessionPath, { event_type: "session_started", timestamp: now(), session_id: sessionId, project_id: projectId, repo_id: repoId, workstream_id: workstreamId, objective });
  const workstreamsPath = repoPath("ops/registry/workstreams.json");
  const payload = readJson(workstreamsPath);
  payload.workstreams = records(payload, "workstreams").map((workstream) => workstream.id === workstreamId ? { ...workstream, session_ids: [...new Set([...(workstream.session_ids || []), sessionId])] } : workstream);
  writeJson(workstreamsPath, payload);
  console.log(rel(sessionPath));
  return 0;
}

function workflowStart(args) {
  const projectId = required(args, "project-id");
  const sessionId = required(args, "session-id");
  const skillId = required(args, "skill-id");
  const skillPath = resolveSkillPath(skillId, args["skill-path"]);
  assertKnownProjectAndSession(projectId, sessionId);
  const id = `wfr-${compactStamp()}-${suffix()}`;
  const logPath = `ops/workflow-runs/${dateStamp()}/${id}.jsonl`;
  const run = {
    id,
    project_id: projectId,
    session_id: sessionId,
    skill_id: skillId,
    skill_path: skillPath,
    title: required(args, "title"),
    flow_id: required(args, "flow-id"),
    status: "open",
    current_skill: required(args, "current-skill"),
    owned_paths: [...new Set([skillPath, ...many(args, "owned-path")])],
    validation_commands: many(args, "validation-command"),
    started_at: now(),
    last_checkpoint_at: now(),
    next_action: required(args, "next-action"),
    log_path: logPath,
  };
  const registryPath = repoPath("ops/registry/workflow-runs.json");
  const registry = readJson(registryPath);
  registry.workflow_runs = [...records(registry, "workflow_runs"), run];
  writeJson(registryPath, registry);
  appendJsonl(repoPath(logPath), { event_type: "workflow_started", timestamp: now(), workflow_run_id: id, ...run });
  console.log(id);
  return 0;
}

function updateWorkflow(args, close = false) {
  const id = required(args, "workflow-run-id");
  const registryPath = repoPath("ops/registry/workflow-runs.json");
  const registry = readJson(registryPath);
  const existing = records(registry, "workflow_runs").find((item) => item.id === id);
  if (!existing) throw new Error(`unknown workflow_run_id ${id}`);
  const identityErrors = skillIdentityErrors(existing);
  if (identityErrors.length) throw new Error(identityErrors.join("; "));
  if (args.status && !VALID_RUN_STATUSES.has(args.status)) throw new Error(`invalid status ${args.status}`);
  const updates = {
    last_checkpoint_at: now(),
    next_action: required(args, "next-action"),
  };
  if (args.status) updates.status = args.status;
  if (args["current-skill"]) updates.current_skill = required(args, "current-skill");
  if (args.summary) updates.final_summary = args.summary;
  if (close) updates.closed_at = now();
  for (const key of ["artifact", "validation-result"]) {
    if (args[key]) updates[key === "artifact" ? "artifacts" : "validation_results"] = many(args, key);
  }
  if (args["review-state"]) updates.review_state = args["review-state"];
  if (args.decision) updates.decision = args.decision;
  registry.workflow_runs = records(registry, "workflow_runs").map((run) => run.id === id ? { ...run, ...updates } : run);
  writeJson(registryPath, registry);
  const run = records(registry, "workflow_runs").find((item) => item.id === id);
  appendJsonl(repoPath(run.log_path), { event_type: close ? "workflow_closed" : "checkpoint", timestamp: now(), workflow_run_id: id, ...updates });
  console.log(id);
  return 0;
}

function runValidateAll() {
  let status = 0;
  for (const validator of [
    validateTracker,
    validateInventory,
    validateProgressDocs,
    validateBuildingCodeV2,
  ]) {
    try {
      const result = validator();
      if (result !== 0) status = 1;
    } catch (error) {
      console.error(error.message);
      status = 1;
    }
  }
  return status;
}

const commands = {
  "export-tracker-ui-data": exportDashboard,
  "validate-tracker": validateTracker,
  "validate-project-surface-inventory": validateInventory,
  "validate-progress-docs": validateProgressDocs,
  "validate-building-code-v2": validateBuildingCodeV2,
  "validate-all": runValidateAll,
  "tracker-status": trackerStatus,
  "tracker-upload-gate": trackerUploadGate,
  "tracker-command-list": trackerCommandList,
  "tracker-command-describe": trackerCommandDescribe,
  "tracker-session-start": sessionStart,
  "tracker-workflow-start": workflowStart,
  "tracker-workflow-checkpoint": (args) => updateWorkflow(args, false),
  "tracker-workflow-close": (args) => updateWorkflow(args, true),
};

const [command, ...rest] = process.argv.slice(2);
if (!command || !commands[command]) {
  console.error(`usage: node scripts/control-repo.mjs <${Object.keys(commands).join("|")}>`);
  process.exit(2);
}

try {
  process.exit(commands[command](parseArgs(rest)));
} catch (error) {
  console.error(error.message);
  process.exit(1);
}
