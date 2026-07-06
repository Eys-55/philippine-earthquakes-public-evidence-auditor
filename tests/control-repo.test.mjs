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
  assert(dashboard.summary.active_projects >= 1);
  assert(Array.isArray(dashboard.workflow_runs));
  assert(page.includes("../data/tracker-dashboard.json"));
});
