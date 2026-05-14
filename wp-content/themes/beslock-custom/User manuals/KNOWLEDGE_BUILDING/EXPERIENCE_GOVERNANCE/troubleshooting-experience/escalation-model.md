# Troubleshooting escalation model

_Schema: `experience-governance/1.0` · escalation model · generated 2026-05-13T17:27:13Z._

## Tiers

| Tier | Label | Scope |
|---|---|---|
| 0 | Self-observation | User notices and classifies a symptom. |
| 1 | Guided self-recovery | Documented recovery procedures (battery-replacement, emergency-power, re-pairing). |
| 2 | Soft reset / reconfig | Unpair + re-pair, re-enroll credentials, network change. |
| 3 | Factory reset | Last-resort local recovery; data-loss accepted. |
| 4 | Support contact | Asynchronous support channel; logs collected. |
| 5 | Field service / RMA | Hardware fault confirmed; physical exchange or technician dispatch. |

## Symptom → tier coverage

| Symptom | Tiers in play |
|---|---|
| `symptom.power` | 1, 2, 4, 5 |
| `symptom.connectivity` | 1, 2, 3, 4 |
| `symptom.credential-failure` | 1, 2, 3 |
| `symptom.mechanical` | 4, 5 |
| `symptom.firmware` | 2, 3, 4 |
| `symptom.lockout` | 1, 2, 3, 4, 5 |

## Escalation rules

1. Symptom triage starts at the lowest tier the symptom maps to.
2. A user MUST be allowed to skip up to two tiers if they explicitly opt in
   (e.g. "I have already replaced batteries").
3. Skipping into Tier 3 (factory-reset) requires acknowledgement of data
   loss.
4. Skipping into Tier 4–5 requires symptom evidence (logs / observed
   behaviour).
5. A failed Tier-N procedure SHOULD propose Tier-N+1 with rationale.

## Recovery prioritization

- Power and lockout symptoms outrank everything else; the surface MUST
  surface battery and emergency-power guidance immediately when those
  symptoms are present.
- Connectivity symptoms allow longer self-diagnosis loops before escalation.
- Mechanical symptoms escalate fast (Tier 4 within two failed Tier-1
  attempts).

## Companion file

- [`escalation-model.json`](escalation-model.json)
