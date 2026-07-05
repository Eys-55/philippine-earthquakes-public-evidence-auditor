# Philippines Earthquake Public Evidence Auditor README Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Turn the main `README.md` into a polished operator README for the Philippines Earthquake Public Evidence Auditor and add one abstract generated header image.

**Architecture:** This is a documentation and asset change only. The README presents the current earthquake auditor as the main public-facing workflow, while raw internal slug/path details stay in a lower maintainer section. No workflow logic, validators, schemas, skill behavior, or lane directory names should change.

**Tech Stack:** Markdown, one generated PNG asset, existing Python validators, image inspection, `git diff --check`.

---

## ECC Guardrails

- Treat the README as the integrated output for the current auditor.
- Do not add new earthquake, legal, engineering, safety, or compliance facts unless they are already represented in existing V2 skill/data/status artifacts or explicitly cited.
- Every claim about what the auditor can prove must stay source-bounded and workflow-level.
- Do not state or imply that the auditor certifies safety, compliance, earthquake safety, or fitness for occupancy.
- Keep raw `-v2` path names out of the title, opening summary, and top public-facing explanation. Raw path names are allowed only in lower operator/maintainer path sections and command blocks.
- Preserve V1 as valid maintainer context. Do not describe it as obsolete, broken, deprecated, or replaced.
- Do not edit validators, schemas, skill logic, or lane directories.
- Do not stage unrelated workflow-catalog files.

### Task 1: Commit This Corrected Plan Before Execution

**Files:**
- Stage: `docs/plans/2026-07-05-earthquake-auditor-readme-implementation-plan.md`

**Step 1: Validate the plan document**

Run:

```bash
python3 scripts/validate_progress_docs.py
git diff --check
```

Expected: both pass.

**Step 2: Stage only the implementation plan**

Run:

```bash
git add docs/plans/2026-07-05-earthquake-auditor-readme-implementation-plan.md
git status --short
```

Expected: the implementation plan is staged. Existing unrelated workflow-catalog
files remain untracked and unstaged.

**Step 3: Commit the corrected plan**

Run:

```bash
git commit -m "docs: plan earthquake auditor readme polish"
```

Expected: commit succeeds before README/image implementation starts.

### Task 2: Generate The Header Image

**Files:**
- Create: `assets/philippines-earthquake-public-evidence-auditor-header.png`
- Create directory if missing: `assets/`

**Step 1: Create the assets directory**

Run:

```bash
mkdir -p assets
```

Expected: command exits 0.

**Step 2: Generate the header artwork**

Use GPT image generation with this prompt:

```text
Abstract professional banner artwork for a Philippines earthquake public evidence auditor: layered Philippine urban buildings and civic infrastructure silhouettes, subtle seismic wave lines and fault geometry, translucent public records and engineering document sheets, evidence trail motifs, restrained technical palette of charcoal, blue-gray, warm paper white, small amber and red signal accents, clean editorial composition, no text, no logos, no disaster rubble, no people, wide header image.
```

Required image constraints:

- artwork only;
- no readable text;
- no logos;
- no people;
- no disaster-rubble imagery;
- wide banner composition suitable for a README header.

**Step 3: Save the generated image**

Save the selected PNG as:

```text
assets/philippines-earthquake-public-evidence-auditor-header.png
```

**Step 4: Verify the asset exists**

Run:

```bash
test -s assets/philippines-earthquake-public-evidence-auditor-header.png
```

Expected: command exits 0.

**Step 5: Visually inspect the image**

Open or view the image and confirm:

- no readable text;
- no logos;
- no people;
- no disaster rubble or sensational damage imagery;
- abstract buildings, seismic/document motifs, and banner composition are visible.

If the image fails any item, regenerate or choose a different image before
continuing.

### Task 3: Rewrite The README Hero And Opening

**Files:**
- Modify: `README.md`

**Step 1: Add the image at the top**

Insert this at the first line of `README.md`:

```markdown
![Abstract seismic evidence banner](assets/philippines-earthquake-public-evidence-auditor-header.png)
```

**Step 2: Replace the workspace-first title**

Replace:

```markdown
# Market Research Agent Workspace
```

With:

```markdown
# Philippines Earthquake Public Evidence Auditor
```

**Step 3: Add the operator summary**

Use this summary directly below the title:

```markdown
A Codex/ECC workflow for checking what public evidence exists about a specific
Philippine building's earthquake-related records. It does not certify safety,
compliance, or fitness for occupancy. It locks the exact building first, narrows
the question to one of four earthquake evidence lanes, then produces a
source-bounded packet with unresolved gaps preserved.
```

**Step 4: Preserve workspace context lower down**

Move the current workspace-introduction idea into a later `Workspace Notes`
section. Do not delete the fact that this is an ECC-aligned multi-lane workspace;
just stop making that the public-facing opening.

### Task 4: Add Operator Sections For The Current Auditor

**Files:**
- Modify: `README.md`

**Step 1: Add `What It Audits`**

Add this section near the top:

```markdown
## What It Audits

This workflow only searches four earthquake evidence lanes:

1. NSCP / seismic design evidence
2. OBO structural permit or review evidence
3. Latest post-earthquake tag / status
4. Latest clearance after damage or tag
```

**Step 2: Add `How The Workflow Runs`**

Add:

```markdown
## How The Workflow Runs

1. Gate 1 confirms the exact building, branch, tenant, wing, or complex.
2. Gate 2 locks one of the four earthquake evidence lanes.
3. Gate 3 builds an evidence packet with document inventory, evidence strength,
   source class, unresolved exceptions, manual request targets, and query log.
4. Gate 4 audits the packet for overclaims before anything is treated as a
   finding.
```

**Step 3: Add `Evidence Rules`**

Explain that official/professional records are separated from operator claims,
news leads, process pages, and weak leads.

Include:

```markdown
Missing public evidence is not evidence of safety, non-safety, compliance,
noncompliance, clearance, no tag, no permit, or no review.
```

**Step 4: Add `No-Evidence Semantics`**

Add:

```markdown
## No-Evidence Semantics

For NSCP/seismic design evidence and OBO structural review evidence, a complete
but unsuccessful search means: `No public evidence found.`

For post-earthquake tag/status and clearance after damage or tag, a complete but
unsuccessful search means: `No public answer found.`
```

### Task 5: Reframe Repo Map And Workspace Notes

**Files:**
- Modify: `README.md`

**Step 1: Add a public-facing `Repo Map` with aliases first**

Use human-readable labels first. Do not make raw `-v2` slugs the visible concept.

```markdown
## Repo Map

- Current auditor skill: `skills/philippines-building-code-evidence-auditor-v2/SKILL.md`
- Current auditor data: `data/philippines-building-code-evidence-auditor-v2/`
- README design: `docs/plans/2026-07-05-earthquake-auditor-readme-design.md`
- Status lock: `docs/status/2026-07-05-philippines-building-code-evidence-auditor-v2-lock.md`
```

**Step 2: Keep raw lane history lower**

Keep the existing lane table, but move it below the current-auditor sections
under:

```markdown
## Workspace Notes
```

**Step 3: Add a maintainer paths subsection**

In `Workspace Notes`, raw V1/V2 wording is acceptable because it is maintainer
context. Use it only there.

**Step 4: Preserve V1 respectfully**

Keep the existing V1 lane information lower down as maintainer context. Do not
call V1 obsolete, broken, deprecated, or replaced.

### Task 6: Update Validator Commands In README

**Files:**
- Modify: `README.md`

**Step 1: Add `Run The Validators`**

Include the current auditor validation commands:

```bash
find data/philippines-building-code-evidence-auditor-v2 -name '*.json' -print0 | xargs -0 -n1 python3 -m json.tool >/tmp/building-code-v2-json-parse.txt
python3 scripts/validate_building_code_v2_identity_gate.py
python3 scripts/validate_building_code_v2_earthquake_scope_gate.py
python3 scripts/validate_building_code_v2_evidence_packet.py
python3 scripts/validate_building_code_v2_overclaim.py
python3 scripts/validate_progress_docs.py
git diff --check
```

**Step 2: Keep V1 preservation checks lower down**

Include the V1 validators in a maintainer subsection:

```bash
python3 scripts/validate_building_identity_gate.py
python3 scripts/validate_audit_scope_gate.py
python3 scripts/validate_audit_scope_source_reality.py
```

### Task 7: Verify README And Asset

**Files:**
- Check: `README.md`
- Check: `assets/philippines-earthquake-public-evidence-auditor-header.png`

**Step 1: Verify the image link points to an existing file**

Run:

```bash
test -s assets/philippines-earthquake-public-evidence-auditor-header.png
rg -n "philippines-earthquake-public-evidence-auditor-header.png" README.md
```

Expected: both commands pass; `rg` prints the README image reference.

**Step 2: Verify top-level README does not publicly frame the product as V2**

Run:

```bash
sed -n '1,120p' README.md | rg -n "V2|v2"
```

Expected: no matches in the first 120 lines. Raw `-v2` path names may appear
later in path and command sections.

**Step 3: Verify no forbidden safety claims were introduced**

Run:

```bash
rg -n "certif(y|ies)|earthquake-safe|is safe|fit for occupancy|compliant" README.md
```

Expected: the implementer must paste or summarize every match and confirm each
one is refusal, limitation, or negative-boundary language rather than a positive
claim.

**Step 4: Verify no uncited new domain facts were added**

Review the README diff. Confirm every earthquake/legal/engineering/source claim
is either:

- workflow-level and already represented in current auditor artifacts; or
- explicitly cited; or
- rewritten as a non-domain operational description.

### Task 8: Full Verification

**Files:**
- Check: all changed files

**Step 1: Run V2 JSON parsing and validators**

Run:

```bash
find data/philippines-building-code-evidence-auditor-v2 -name '*.json' -print0 | xargs -0 -n1 python3 -m json.tool >/tmp/building-code-v2-json-parse.txt
python3 scripts/validate_building_code_v2_identity_gate.py
python3 scripts/validate_building_code_v2_earthquake_scope_gate.py
python3 scripts/validate_building_code_v2_evidence_packet.py
python3 scripts/validate_building_code_v2_overclaim.py
```

Expected: all validators pass.

**Step 2: Run V1 preservation validators**

Run:

```bash
python3 scripts/validate_building_identity_gate.py
python3 scripts/validate_audit_scope_gate.py
python3 scripts/validate_audit_scope_source_reality.py
```

Expected: all validators pass.

**Step 3: Run docs and whitespace checks**

Run:

```bash
python3 scripts/validate_progress_docs.py
git diff --check
```

Expected: both pass.

### Task 9: Commit The README And Image

**Files:**
- Stage: `README.md`
- Stage: `assets/philippines-earthquake-public-evidence-auditor-header.png`

**Step 1: Review staged files**

Run:

```bash
git status --short
```

Expected: only README/header-image files from this implementation are staged for
the final implementation commit. Unrelated workflow-catalog files remain
untracked and unstaged.

**Step 2: Commit**

Run:

```bash
git add README.md assets/philippines-earthquake-public-evidence-auditor-header.png
git commit -m "docs: polish earthquake auditor readme"
```

Expected: commit succeeds.
