import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
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

function runControl(command) {
  return spawnSync("node", ["scripts/control-repo.mjs", ...command], {
    cwd: ROOT,
    encoding: "utf8",
  });
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

test("tracker dashboard export is consumable by Astro page", () => {
  const result = runControl(["export-tracker-ui-data", "--output", "tracker-ui/src/data/tracker-dashboard.json"]);
  assert.equal(result.status, 0, result.stderr);
  const dashboard = JSON.parse(read("tracker-ui/src/data/tracker-dashboard.json"));
  const page = read("tracker-ui/src/pages/index.astro");

  assert.equal(dashboard.kind, "tracker_astro_monitor_dashboard");
  assert(dashboard.summary.tracked_skills >= 1);
  assert(Array.isArray(dashboard.tracked_skills));
  assert(dashboard.tracked_skills.every((skill) => skill.path.startsWith("skills/")));
  assert(dashboard.summary.active_projects >= 1);
  assert(Array.isArray(dashboard.workflow_runs));
  assert(dashboard.workflow_runs.every((run) => run.skill_id && run.skill_path));
  assert(page.includes("../data/tracker-dashboard.json"));
  assert(page.includes("Skills Being Built"));
  assert(page.includes("Skill Runs"));
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
