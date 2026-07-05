# Philippines Earthquake Public Evidence Auditor README Design

## Goal

Rewrite the main `README.md` into a polished operator README for the current
Philippines Earthquake Public Evidence Auditor, with one abstract generated
header image.

## Audience

The README is primarily for developers and operators who already understand
Codex/ECC-style workflows, but do not know the earthquake public-evidence domain.
It should explain the workflow's domain boundaries, evidence rules, validators,
and operating paths without becoming marketing copy.

## Public-Facing Name

Use `Philippines Earthquake Public Evidence Auditor` as the visible product
name. Do not present the top-level README as a V1/V2 comparison. The internal
slug can remain `philippines-building-code-evidence-auditor-v2`, but the public
README should treat this as the current primary auditor.

## README Structure

1. Header image: abstract artwork only, no text.
2. Product title and short operator summary.
3. `What It Audits`: the four permanent earthquake evidence lanes.
4. `How The Workflow Runs`: Gate 1 through Gate 4.
5. `Evidence Rules`: official/professional evidence separated from weak leads.
6. `No-Evidence Semantics`: first two lanes mean no public evidence found; last
   two lanes mean no public answer found.
7. `Run The Validators`: exact commands for V1 preservation and current auditor
   checks.
8. `Repo Map`: primary paths for the current auditor.
9. `Workspace Notes`: lower-priority maintainer context about other lanes.

## Header Image Direction

Generate one abstract artwork banner with no readable text, no logos, no people,
and no disaster-rubble imagery.

Visual elements:

- abstract Philippine urban building silhouettes;
- subtle seismic wave lines or fault-line geometry;
- translucent public-record, engineering-document, or evidence-sheet motifs;
- restrained technical palette: charcoal, blue-gray, warm paper white, and small
  amber/red signal accents;
- professional operator feel rather than a disaster-awareness poster.

Target file:

`assets/philippines-earthquake-public-evidence-auditor-header.png`

Prompt draft:

```text
Abstract professional banner artwork for a Philippines earthquake public evidence auditor: layered Philippine urban buildings and civic infrastructure silhouettes, subtle seismic wave lines and fault geometry, translucent public records and engineering document sheets, evidence trail motifs, restrained technical palette of charcoal, blue-gray, warm paper white, small amber and red signal accents, clean editorial composition, no text, no logos, no disaster rubble, no people, wide header image.
```

## Content Style

Use direct, technical, evidence-first writing. The README should not claim the
auditor determines safety, compliance, or fitness for occupancy. It should teach
developers how to operate the workflow and why the boundaries exist.

Opening summary target:

```markdown
# Philippines Earthquake Public Evidence Auditor

A Codex/ECC workflow for checking what public evidence exists about a specific
Philippine building's earthquake-related records. It does not certify safety,
compliance, or fitness for occupancy. It locks the exact building first, narrows
the question to one of four earthquake evidence lanes, then produces a
source-bounded packet with unresolved gaps preserved.
```

## Implementation Boundaries

- Generate one header image.
- Save the image under `assets/`.
- Rewrite the main `README.md` so the current auditor is the public-facing
  focus.
- Keep workspace and legacy/internal lane details lower in the README as
  maintainer context.
- Do not rename directories.
- Do not change workflow behavior.
- Do not edit validators, schemas, or skill logic.
- Run docs/image checks plus the existing validator checks.

## Approval

Approved direction: operator README with abstract evidence banner, current
auditor presented as the main product, no public V2 framing in the top-level
story.
