# Staged Realization Strategy

Five sequential stages from prototype to controlled production. Each stage has explicit supervision posture, evidence requirements, and exit decision.

## Stages

- `prototype` → exit_to: assisted-runtime
- `assisted-runtime` → exit_to: supervised-runtime
- `supervised-runtime` → exit_to: operational-pilot
- `operational-pilot` → exit_to: controlled-production
- `controlled-production` → exit_to: (no further stage; remains under continuous governance)

## Rules

- Stages are sequential; no skipping a stage that produced state.
- Each stage has explicit supervision posture and evidence requirements.
- Promotion to the next stage requires a documented exit decision with provenance.
- Demotion (to a prior stage) is always allowed and is the safe response to incidents.
- Controlled production remains under continuous governance; it is never a terminal stage of governance.
