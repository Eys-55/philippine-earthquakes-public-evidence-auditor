# Building Code Auditor Agent Loop

Date: 2026-07-05

This note captures the ECC loop pattern for the Philippines Building Code
Evidence Auditor. It is a learning artifact, not the final Gate 3 packet schema.

## ECC Loop Shape

An agent loop is not just repeated tool use. In ECC terms, it is:

1. a locked objective;
2. small agent-sized work units;
3. a measurable eval gate after each unit;
4. a stop condition before the loop can overclaim, churn, or spend without
   progress;
5. a handoff artifact that preserves what happened and what the next operator
   can safely assume.

For this repo, the loop must preserve the auditor boundary: it gathers public
evidence and manual-request leads. It does not certify building-code compliance,
structural safety, earthquake safety, fire safety, or fitness for occupancy.

## Loop Type

Use the ECC `sequential` loop as the default.

Use parallel agents only inside one loop turn when source lanes are independent,
for example permit/OBO, incident/news, standards/process, contractor/developer,
and reviewer lanes. Integration remains sequential because the packet needs one
consistent identity, subscope, timeframe, confidence label, and overclaim
boundary.

Do not use an open-ended infinite loop for this workflow. Research can always
continue, so the loop needs explicit stop rules.

## Loop Contract

Objective:

- Produce a source-attributed public-evidence packet for one confirmed
  Philippine building, establishment, mall, hotel, or facility.

Do not own:

- engineering certification;
- legal compliance finding;
- official permit verification unless the actual official record is public;
- claims of current safety or fitness for occupancy;
- third-party writes, signups, paid requests, or credentialed systems.

Inputs:

- confirmed Gate 1 place packet;
- locked Gate 2 audit scope;
- `target_subscope`;
- `timeframe`;
- source-reality matrix;
- NSCP evidence map when structural-code questions are in scope.

Outputs:

- raw source findings by lane;
- integrated public-evidence packet;
- source URL list;
- confidence and source-reality labels;
- manual request checklist;
- overclaim boundary;
- validation result.

## Loop Steps

### 1. Discover Current State

Read the confirmed place packet, locked scope, source-reality matrix, and any
target-specific method file such as the NSCP evidence map.

Stop if:

- the exact place is not confirmed;
- the target is a complex but the subscope is missing;
- the user asks a compliance or safety question without allowing caveated
  evidence-only output.

### 2. Plan Source Lanes

Choose only the lanes needed for the locked scope.

Common lanes:

- identity and alias lane;
- permit, occupancy, OBO, and BFP route lane;
- incident, damage, closure, repair, retrofit, and inspection lane;
- contractor, professional, developer, and operator lane;
- standards and process context lane;
- manual request lane;
- reviewer and overclaim lane.

Each lane must have one done condition. Example: "searched official/LGU/company
and reputable news sources for post-earthquake closure or inspection evidence,
then classified source reality."

### 3. Run Lane Agents

Each lane returns a structured result:

- `lane`;
- `query_log`;
- `best_sources`;
- `what_was_found`;
- `what_was_not_found`;
- `source_reality_status`;
- `confidence`;
- `manual_follow_up_needed`;
- `overclaim_risk`.

Raw lane outputs should be preserved before integration.

### 4. Integrate Packet

Merge lane outputs into one packet only after identity, subscope, and timeframe
are consistent.

The integrator must keep these separate:

- standards context;
- target-specific records;
- indirect company or news evidence;
- weak leads;
- missing evidence;
- manual request routes.

### 5. Run Eval Gate

A packet is not done until it passes:

- every material claim has a source URL;
- no source is used beyond what it can prove;
- missing public evidence is not treated as noncompliance;
- reopening, booking, mall hours, or social posts are not treated as safety or
  compliance proof;
- NSCP/structural-code claims use `not_assessable_from_public_web` unless a
  target-tied official or professional document exists;
- manual follow-up names the correct custodian and document types;
- the packet includes `target_subscope`, `timeframe`, `source_reality_status`,
  `manual_request_targets`, and `overclaim_boundary`.

### 6. Decide Continue, Stop, Or Escalate

Continue only if the failed gate identifies a new, bounded work unit.

Stop when:

- the packet passes validation;
- the next step is a manual OBO/BFP/operator/professional request;
- the exact target or timeframe is ambiguous;
- three consecutive searches produce no new source type;
- the remaining question requires professional inspection, legal advice, or
  non-public records.

Escalate to the user when:

- the target could mean multiple buildings, wings, tenants, or complexes;
- source evidence conflicts on the identity or event;
- the user wants a conclusion stronger than the evidence supports.

## Minimal Pseudocode

```text
while packet_not_validated:
  read confirmed_place, locked_scope, source_reality
  if missing identity/subscope/timeframe:
    ask one blocking question
    stop

  choose lanes for locked_scope
  run independent lane searches
  preserve raw lane findings
  integrate packet
  run overclaim and citation eval

  if eval passes:
    publish packet and handoff
    stop

  if failure is manual-record-only or professional-review-only:
    publish manual request checklist
    stop

  if failure is bounded and new:
    run next smallest lane repair
  else:
    freeze loop and hand off blocker
    stop
```

## First Concrete Build Target

The first real loop artifact should be Gate 3:

- `data/building-code-auditor/evidence-packet-schema.json`
- `scripts/validate_building_code_packet.py`
- one sample packet under `reports/`

The sample should use a target where the evidence matrix is clearest. Based on
the Gate 2 learning run, Robinsons GenSan is the strongest first sample because
it has public incident evidence and partial public permit/occupancy fields from
a company filing. It still must not be treated as proof of current NSCP
compliance or structural safety.

## Failure Modes To Watch

- loop churn: repeated searches with no new source type;
- source drift: social or news snippets becoming the main support for serious
  claims;
- scope creep: disaster-risk context blending back into the deprecated assessor;
- standards overclaim: generic PD 1096 or NSCP context becoming target-specific
  compliance;
- integration loss: raw lane findings disappear after the final report;
- manual-record denial: the loop keeps searching when the right answer is an
  OBO, BFP, operator, or professional request.
