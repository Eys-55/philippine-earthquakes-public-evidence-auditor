import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { execFileSync, spawnSync } from "node:child_process";

const ROOT = path.resolve(import.meta.dirname, "..");

function read(file) {
  return fs.readFileSync(path.join(ROOT, file), "utf8");
}

function listFiles(dir) {
  const root = path.join(ROOT, dir);
  if (!fs.existsSync(root)) return [];
  const out = [];
  for (const entry of fs.readdirSync(root, { recursive: true })) {
    const full = path.join(root, entry);
    if (fs.statSync(full).isFile()) out.push(path.join(dir, entry).split(path.sep).join("/"));
  }
  return out.sort();
}

function runControl(command, options = {}) {
  return spawnSync("node", ["scripts/control-repo.mjs", ...command], {
    cwd: ROOT,
    env: { ...process.env, ...(options.env || {}) },
    encoding: "utf8",
  });
}

function writeJson(file, value) {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, `${JSON.stringify(value, null, 2)}\n`);
}

function makeTrackerRoot() {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "skill-tracker-"));
  fs.mkdirSync(path.join(root, "skills/agent-workflow-project-maker"), { recursive: true });
  fs.writeFileSync(path.join(root, "skills/agent-workflow-project-maker/SKILL.md"), "# Agent Workflow Project Maker\n");
  writeJson(path.join(root, "ops/registry/projects.json"), {
    projects: [{
      id: "agent-workflow-project-maker",
      title: "Agent Workflow Project Maker",
      status: "active",
      repos: ["market-research-agent-control"],
      workstreams: ["control-repo-tracker"],
    }],
  });
  writeJson(path.join(root, "ops/registry/repos.json"), {
    repos: [{ id: "market-research-agent-control", path: "." }],
  });
  writeJson(path.join(root, "ops/registry/workstreams.json"), {
    workstreams: [{
      id: "control-repo-tracker",
      project_id: "agent-workflow-project-maker",
      repo_id: "market-research-agent-control",
      status: "active",
      session_ids: [],
    }],
  });
  writeJson(path.join(root, "ops/registry/workflow-runs.json"), { workflow_runs: [] });
  return root;
}

function startFixtureRun(root, overrides = {}) {
  const env = { TRACKER_ROOT: root };
  const session = runControl([
    "tracker-session-start",
    "--project-id", "agent-workflow-project-maker",
    "--repo-id", "market-research-agent-control",
    "--workstream-id", "control-repo-tracker",
    "--objective", "Battle test fixture",
  ], { env });
  assert.equal(session.status, 0, session.stderr);
  const sessionId = path.basename(session.stdout.trim()).replace(/^session-/, "").replace(/\.jsonl$/, "");
  const args = [
    "tracker-workflow-start",
    "--project-id", overrides.projectId || "agent-workflow-project-maker",
    "--session-id", overrides.sessionId || sessionId,
    "--skill-id", overrides.skillId || "agent-workflow-project-maker",
    "--title", overrides.title || "Skill identity fixture",
    "--flow-id", overrides.flowId || "agent_workflow_project_maker",
    "--current-skill", overrides.currentSkill || "implement",
    "--owned-path", "tests/control-repo.test.mjs",
    "--validation-command", "npm test",
    "--next-action", overrides.nextAction || "Verify skill-first tracker behavior.",
  ];
  if (overrides.skillPath) args.splice(7, 0, "--skill-path", overrides.skillPath);
  return { env, sessionId, result: runControl(args, { env }) };
}

function goodContextManifest(root, runId, skillId = "agent-workflow-project-maker") {
  const file = path.join(root, "ops/workflow-runs/2026-07-06", `${runId}-context.md`);
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, [
    `# Context Manifest: ${runId}`,
    "",
    "## Loaded ECC Context",
    "- `AGENTS.md`",
    `- \`skills/${skillId}/SKILL.md\``,
    "",
    "## Premise Lock",
    "A workflow bug must start with ECC-loaded intake before implementation.",
    "",
    "## First Context-Aware Question",
    "Which skill is being built or debugged?",
    "",
  ].join("\n"));
  return path.relative(root, file).split(path.sep).join("/");
}

test("repo contains no Python files", () => {
  const files = execFileSync("find", [".", "-path", "./.git", "-prune", "-o", "-path", "./node_modules", "-prune", "-o", "-path", "./dist", "-prune", "-o", "-name", "*.py", "-print"], { cwd: ROOT, encoding: "utf8" })
    .split("\n")
    .filter(Boolean)
    .map((file) => file.replace(/^\.\//, ""));

  assert.deepEqual(files, []);
});

test("package scripts use Node control adapter", () => {
  const pkg = JSON.parse(read("package.json"));

  assert.equal(pkg.scripts["prepare:tracker-ui"], "node scripts/control-repo.mjs export-tracker-ui-data");
  assert.equal(pkg.scripts.validate, "node scripts/control-repo.mjs validate-all");
  assert.equal(pkg.scripts.test, "node --test tests/*.test.mjs");
  assert(!JSON.stringify(pkg.scripts).includes("python"));
});

test("repo-local Codex slash prompts expose workflow commands", () => {
  const expected = [
    "tracker-workflow.md",
    "tracker-status.md",
    "tracker-closeout.md",
    "workflow-router.md",
    "workflow-intake.md",
    "workflow-grilling.md",
    "workflow-to-prd.md",
    "workflow-to-issues.md",
    "workflow-implement.md",
    "workflow-code-review.md",
    "workflow-closeout.md",
  ];
  const files = listFiles(".codex/prompts").map((file) => path.basename(file));

  for (const file of expected) assert(files.includes(file), file);
  for (const file of expected) {
    const text = read(`.codex/prompts/${file}`);
    assert(text.includes("Codex-facing slash prompt") || text.includes("Codex-facing command"), file);
    assert(text.includes("node scripts/control-repo.mjs") || text.includes("npm run"), file);
    assert(!text.includes("python"), file);
    assert(!text.includes("tracker_workflow_intake_start"), file);
    assert(!text.includes("validate_tracker.py"), file);
  }
});

test("skills-first chat contract remains authoritative", () => {
  const files = [
    "AGENTS.md",
    "CONTEXT.md",
    "skills/agent-workflow-project-maker/SKILL.md",
    "skills/control-repo-manager/SKILL.md",
  ];
  for (const file of files) {
    const text = read(file);
    assert(text.includes("Skills are the operator interface"), file);
    assert(text.includes("Codex chat is the operator surface"), file);
    assert(text.includes("The user never runs tracker scripts"), file);
  }
});

test("edit intent to tracked projects is a workflow trigger", () => {
  const files = [
    "AGENTS.md",
    "CONTEXT.md",
    "skills/agent-workflow-project-maker/SKILL.md",
    "skills/control-repo-manager/SKILL.md",
  ];
  for (const file of files) {
    const text = read(file);
    const normalized = text.replace(/\s+/g, " ");
    assert(normalized.includes("edit, change"), file);
    assert(normalized.includes("tracked project"), file);
    assert(normalized.includes("before asking what the edit is"), file);
  }

  const skill = read("skills/agent-workflow-project-maker/SKILL.md");
  assert(skill.includes("I will make an edit to my earthquake project"));
});

test("tracker runs are skill-first records", () => {
  const registry = JSON.parse(read("ops/registry/workflow-runs.json"));
  const runs = registry.workflow_runs;

  assert(runs.length > 0);
  for (const run of runs) {
    assert.equal(typeof run.skill_id, "string", run.id);
    assert(run.skill_id.length > 0, run.id);
    assert.equal(typeof run.skill_path, "string", run.id);
    assert(run.skill_path.startsWith("skills/"), run.id);
    assert(run.skill_path.endsWith("/SKILL.md"), run.id);
    assert(fs.existsSync(path.join(ROOT, run.skill_path)), run.id);
  }
});

test("workflow command-era Python surfaces are absent", () => {
  const forbidden = [
    "tracker_workflow_intake_start",
    "workflow_skill_slash_surface",
    "workflow_catalog_cli_run",
    "query_workflow_catalog",
    "validate_tracker",
  ];
  const scriptFiles = listFiles("scripts");

  for (const name of forbidden) {
    assert(!scriptFiles.some((file) => path.basename(file, path.extname(file)) === name), name);
  }
});

test("control adapter validates tracker and inventory", () => {
  for (const command of [
    ["validate-tracker"],
    ["validate-project-surface-inventory"],
    ["validate-progress-docs"],
    ["validate-building-code-v2"],
  ]) {
    const result = runControl(command);
    assert.equal(result.status, 0, `${command.join(" ")}\n${result.stdout}\n${result.stderr}`);
  }
});

test("tracker exposes a skills-first callable command suite", () => {
  const result = runControl(["tracker-command-list", "--json"]);
  assert.equal(result.status, 0, result.stderr);
  const payload = JSON.parse(result.stdout);
  const ids = payload.commands.map((command) => command.id);

  for (const id of [
    "tracker.status",
    "tracker.upload_gate",
    "tracker.session_start",
    "tracker.workflow_start",
    "tracker.workflow_checkpoint",
    "tracker.workflow_close",
    "tracker.validate",
    "tracker.validate_all",
    "tracker.dashboard_export",
    "tracker.command_list",
    "tracker.command_describe",
  ]) {
    assert(ids.includes(id), id);
  }
  assert(payload.commands.every((command) => command.internal_only === true));
  assert(payload.commands.every((command) => command.user_runs_terminal === false));
  assert(payload.commands.every((command) => command.operator_surface === "Codex chat plus repo skills"));
  assert(payload.commands.every((command) => command.skill_id === "control-repo-manager"));
  assert(payload.commands.every((command) => command.skill_path === "skills/control-repo-manager/SKILL.md"));
});

test("tracker command describe resolves ids and adapters", () => {
  for (const commandName of ["tracker.status", "tracker-status"]) {
    const result = runControl(["tracker-command-describe", "--command", commandName, "--json"]);
    assert.equal(result.status, 0, result.stderr);
    const command = JSON.parse(result.stdout);
    assert.equal(command.id, "tracker.status");
    assert.equal(command.adapter, "tracker-status");
    assert.equal(command.internal_only, true);
  }

  const missing = runControl(["tracker-command-describe", "--command", "tracker.missing", "--json"]);
  assert.notEqual(missing.status, 0);
  assert(missing.stderr.includes("unknown tracker command tracker.missing"));
});

test("tracker dashboard export is consumable by Astro page", () => {
  const output = path.join(fs.mkdtempSync(path.join(os.tmpdir(), "tracker-dashboard-")), "tracker-dashboard.json");
  const result = runControl(["export-tracker-ui-data", "--output", output]);
  assert.equal(result.status, 0, result.stderr);
  const dashboard = JSON.parse(fs.readFileSync(output, "utf8"));
  const page = read("tracker-ui/src/pages/index.astro");

  assert.equal(dashboard.kind, "tracker_astro_monitor_dashboard");
  assert(dashboard.summary.tracked_skills >= 1);
  assert(dashboard.summary.tracker_commands >= 1);
  assert(Array.isArray(dashboard.tracked_skills));
  assert(Array.isArray(dashboard.tracker_commands));
  assert(dashboard.tracked_skills.every((skill) => skill.path.startsWith("skills/")));
  assert(dashboard.tracker_commands.every((command) => command.internal_only === true));
  assert(dashboard.tracker_commands.every((command) => command.skill_path === "skills/control-repo-manager/SKILL.md"));
  assert(dashboard.summary.active_projects >= 1);
  assert(Array.isArray(dashboard.workflow_runs));
  assert(dashboard.workflow_runs.every((run) => run.skill_id && run.skill_path));
  assert(!JSON.stringify(dashboard).includes(".py"));
  assert(!JSON.stringify(dashboard).includes("/tracker workflow"));
  assert(page.includes("../data/tracker-dashboard.json"));
  assert(page.includes("Skills Being Built"));
  assert(page.includes("Skill Runs"));
  assert(page.includes("Active Skill Lanes"));
  assert(page.includes("Callable Tracker Commands"));
  assert(page.includes("Skill Lanes And Workstreams"));
  assert(page.includes("Inactive Surfaces"));
});

test("new tracker workflow runs require repo skill identity", () => {
  const result = runControl([
    "tracker-workflow-start",
    "--project-id", "agent-workflow-project-maker",
    "--session-id", "missing-session",
    "--title", "Missing skill identity fixture",
    "--flow-id", "agent_workflow_project_maker",
    "--current-skill", "implement",
    "--owned-path", "scripts/control-repo.mjs",
    "--validation-command", "npm test",
    "--next-action", "This should fail before mutating tracker state.",
  ]);

  assert.notEqual(result.status, 0);
  assert(result.stderr.includes("missing --skill-id"));
});

test("new tracker workflow runs persist and own repo skill identity", () => {
  const root = makeTrackerRoot();
  const { env, result: started } = startFixtureRun(root);
  assert.equal(started.status, 0, started.stderr);

  const registry = JSON.parse(fs.readFileSync(path.join(root, "ops/registry/workflow-runs.json"), "utf8"));
  assert.equal(registry.workflow_runs.length, 1);
  const [run] = registry.workflow_runs;
  assert.equal(run.skill_id, "agent-workflow-project-maker");
  assert.equal(run.skill_path, "skills/agent-workflow-project-maker/SKILL.md");
  assert(run.owned_paths.includes("skills/agent-workflow-project-maker/SKILL.md"));
  assert(run.owned_paths.includes("tests/control-repo.test.mjs"));

  const validated = runControl(["validate-tracker"], { env });
  assert.equal(validated.status, 0, validated.stderr);
});

test("tracker workflow start rejects missing skill files before mutation", () => {
  const root = makeTrackerRoot();
  const env = { TRACKER_ROOT: root };
  const before = fs.readFileSync(path.join(root, "ops/registry/workflow-runs.json"), "utf8");
  const result = runControl([
    "tracker-workflow-start",
    "--project-id", "agent-workflow-project-maker",
    "--session-id", "any-session",
    "--skill-id", "missing-skill",
    "--title", "Missing skill fixture",
    "--flow-id", "agent_workflow_project_maker",
    "--current-skill", "implement",
    "--owned-path", "tests/control-repo.test.mjs",
    "--validation-command", "npm test",
    "--next-action", "This must not mutate registry.",
  ], { env });

  assert.notEqual(result.status, 0);
  assert(result.stderr.includes("missing skill file skills/missing-skill/SKILL.md"));
  assert.equal(fs.readFileSync(path.join(root, "ops/registry/workflow-runs.json"), "utf8"), before);
});

test("tracker workflow start rejects skill path traversal and mismatches before mutation", () => {
  for (const skillPath of [
    "skills/../.agents/skills/code-review/SKILL.md",
    "skills/control-repo-manager/SKILL.md",
  ]) {
    const root = makeTrackerRoot();
    fs.mkdirSync(path.join(root, ".agents/skills/code-review"), { recursive: true });
    fs.writeFileSync(path.join(root, ".agents/skills/code-review/SKILL.md"), "# Outside Skill\n");
    fs.mkdirSync(path.join(root, "skills/control-repo-manager"), { recursive: true });
    fs.writeFileSync(path.join(root, "skills/control-repo-manager/SKILL.md"), "# Control Repo Manager\n");
    const before = fs.readFileSync(path.join(root, "ops/registry/workflow-runs.json"), "utf8");
    const { result } = startFixtureRun(root, { skillPath });

    assert.notEqual(result.status, 0);
    assert(result.stderr.includes("skill_path must equal skills/agent-workflow-project-maker/SKILL.md"));
    assert.equal(fs.readFileSync(path.join(root, "ops/registry/workflow-runs.json"), "utf8"), before);
  }
});

test("tracker workflow start rejects unknown project or session before mutation", () => {
  for (const overrides of [
    { projectId: "missing-project" },
    { sessionId: "missing-session" },
  ]) {
    const root = makeTrackerRoot();
    const before = fs.readFileSync(path.join(root, "ops/registry/workflow-runs.json"), "utf8");
    const { result } = startFixtureRun(root, overrides);

    assert.notEqual(result.status, 0);
    assert(result.stderr.includes(overrides.projectId ? "unknown project_id" : "unknown session_id"));
    assert.equal(fs.readFileSync(path.join(root, "ops/registry/workflow-runs.json"), "utf8"), before);
  }
});

test("tracker validation rejects mismatched skill identity in existing registry", () => {
  const root = makeTrackerRoot();
  const { env, result } = startFixtureRun(root);
  assert.equal(result.status, 0, result.stderr);
  const registryPath = path.join(root, "ops/registry/workflow-runs.json");
  const registry = JSON.parse(fs.readFileSync(registryPath, "utf8"));
  registry.workflow_runs[0].skill_path = "skills/control-repo-manager/SKILL.md";
  fs.mkdirSync(path.join(root, "skills/control-repo-manager"), { recursive: true });
  fs.writeFileSync(path.join(root, "skills/control-repo-manager/SKILL.md"), "# Control Repo Manager\n");
  writeJson(registryPath, registry);

  const validated = runControl(["validate-tracker"], { env });
  assert.notEqual(validated.status, 0);
  assert(validated.stderr.includes("skill_path must equal skills/agent-workflow-project-maker/SKILL.md"));
});

test("tracker validation rejects fake context manifests and workflow bugs that skip intake", () => {
  const root = makeTrackerRoot();
  const { env, result } = startFixtureRun(root, {
    title: "Adversarial workflow bug without intake",
    currentSkill: "implement",
    nextAction: "Fix the workflow problem directly.",
  });
  assert.equal(result.status, 0, result.stderr);
  let validated = runControl(["validate-tracker"], { env });
  assert.notEqual(validated.status, 0);
  assert(validated.stderr.includes("workflow intake requires context manifest"));

  const registryPath = path.join(root, "ops/registry/workflow-runs.json");
  const registry = JSON.parse(fs.readFileSync(registryPath, "utf8"));
  const run = registry.workflow_runs[0];
  const fakePath = `ops/workflow-runs/2026-07-06/${run.id}-context.md`;
  fs.mkdirSync(path.dirname(path.join(root, fakePath)), { recursive: true });
  fs.writeFileSync(path.join(root, fakePath), "fake context only\n");
  run.artifacts = [fakePath];
  writeJson(registryPath, registry);

  validated = runControl(["validate-tracker"], { env });
  assert.notEqual(validated.status, 0);
  assert(validated.stderr.includes("context manifest missing marker Loaded Context"));

  run.artifacts = [goodContextManifest(root, run.id)];
  writeJson(registryPath, registry);
  validated = runControl(["validate-tracker"], { env });
  assert.equal(validated.status, 0, validated.stderr);
});

test("tracker validation rejects edit-intent project runs that skip intake", () => {
  const root = makeTrackerRoot();
  const { env, result } = startFixtureRun(root, {
    title: "I will make an edit to my earthquake proj",
    currentSkill: "implement",
    nextAction: "Ask what edit the user is planning.",
  });
  assert.equal(result.status, 0, result.stderr);

  const validated = runControl(["validate-tracker"], { env });
  assert.notEqual(validated.status, 0);
  assert(validated.stderr.includes("workflow intake requires context manifest"));
});

test("tracker validation rejects active intake runs that never enter grilling", () => {
  const root = makeTrackerRoot();
  const { env, result } = startFixtureRun(root, {
    title: "Workflow intake with first grilling question",
    currentSkill: "workflow_intake",
    nextAction: "Ask the first context-aware grilling question.",
  });
  assert.equal(result.status, 0, result.stderr);
  const runId = result.stdout.trim();
  const registryPath = path.join(root, "ops/registry/workflow-runs.json");
  const registry = JSON.parse(fs.readFileSync(registryPath, "utf8"));
  const run = registry.workflow_runs[0];
  const manifestPath = goodContextManifest(root, runId);
  run.context_manifest_path = manifestPath;
  run.artifacts = [manifestPath];
  writeJson(registryPath, registry);

  let validated = runControl(["validate-tracker"], { env });
  assert.notEqual(validated.status, 0);
  assert(validated.stderr.includes("workflow_intake with context manifest must checkpoint to grilling"));

  const checkpointed = runControl([
    "tracker-workflow-checkpoint",
    "--workflow-run-id", runId,
    "--current-skill", "grilling",
    "--next-action", "Ask one context-aware grilling question and wait for the answer.",
  ], { env });
  assert.equal(checkpointed.status, 0, checkpointed.stderr);
  const updated = JSON.parse(fs.readFileSync(registryPath, "utf8")).workflow_runs[0];
  assert.equal(updated.current_skill, "grilling");

  validated = runControl(["validate-tracker"], { env });
  assert.equal(validated.status, 0, validated.stderr);
});

test("tracker workflow update rejects unknown runs and invalid statuses before mutation", () => {
  const root = makeTrackerRoot();
  const { env, result } = startFixtureRun(root);
  assert.equal(result.status, 0, result.stderr);
  const registryPath = path.join(root, "ops/registry/workflow-runs.json");
  const before = fs.readFileSync(registryPath, "utf8");
  const invalidStatus = runControl([
    "tracker-workflow-close",
    "--workflow-run-id", result.stdout.trim(),
    "--status", "done-ish",
    "--next-action", "Should fail.",
  ], { env });
  assert.notEqual(invalidStatus.status, 0);
  assert(invalidStatus.stderr.includes("invalid status done-ish"));
  assert.equal(fs.readFileSync(registryPath, "utf8"), before);

  const unknown = runControl([
    "tracker-workflow-checkpoint",
    "--workflow-run-id", "missing-run",
    "--next-action", "Should fail.",
  ], { env });
  assert.notEqual(unknown.status, 0);
  assert(unknown.stderr.includes("unknown workflow_run_id missing-run"));
  assert.equal(fs.readFileSync(registryPath, "utf8"), before);
});
