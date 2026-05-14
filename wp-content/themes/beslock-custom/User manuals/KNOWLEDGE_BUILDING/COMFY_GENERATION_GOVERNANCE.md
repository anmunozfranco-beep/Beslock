# COMFY GENERATION GOVERNANCE

Status: Active governance.
Scope: All visual generation in the BESLOCK Product Knowledge Core.
Authority: This document overrides any other visual-generation guidance in the repository.

---

## 1. Comfy-only policy

ComfyUI is the **only** authorized visual orchestration engine in this project.

- All product visuals, support visuals, derivative renders, and conditioning-driven outputs are produced through ComfyUI.
- No other generation engine, web UI, ad-hoc API call, or one-off script is permitted to produce visuals that are promoted into a product nucleus.
- Quick local previews and exploratory experiments are allowed, but their outputs may not enter `publishing/`, `visual-system/qa/selected-assets/`, or any nucleus location that implies approval.

Authoritative tooling:
- `visual_generation.py` — the runner that exports/runs/scores/writes back through ComfyUI.
- `tools/comfy/workflow_api.json.json` — the current approved baseline workflow JSON.
- `ext-images/<slug>/automation/orchestrators/orchestration-manifest.json` — per-product orchestration policy.

---

## 2. Workflow JSON governance

Every ComfyUI workflow used by the project must be:
1. **Registered** in the shared workflow registry under `tools/comfy/`.
2. **Versioned** with a stable identifier (e.g. `workflow-id@semver`).
3. **Hashed** (content hash of the JSON) and the hash recorded in the registry entry.
4. **Approved** with an explicit reviewer and approval timestamp.
5. **Documented** with: purpose, accepted inputs, expected outputs, required conditioning, and known limitations.

Rules:
- Anonymous or unregistered workflows may not be executed against canonical PNGs.
- A workflow change is a new version, not an in-place mutation. The previous version is retained for reproducibility.
- A workflow may be deprecated but not silently deleted while any nucleus run record references it.
- The double-extension filename `tools/comfy/workflow_api.json.json` is a known historical artifact and must be normalized in the registry; do not silently rename it without updating every reference.

---

## 3. Reproducibility requirements

Every approved generation run must record enough information to reproduce the result bit-for-bit (subject to engine determinism):

- product slug
- canonical PNG path and content hash
- workflow registry ID and version
- workflow content hash
- prompt contract (positive, negative, conditioning prompts)
- seed
- sampler, steps, CFG, scheduler, model name and hash
- ControlNet/IPAdapter inputs (paths + hashes)
- output paths
- approval state and reviewer
- timestamp

Rules:
- Run records live in `ext-images/<slug>/automation/runs/`.
- A run that cannot be described in the schema above must not be approved.
- Re-running an approved record must reproduce the same selected output, or the discrepancy must be recorded.

---

## 4. Prompt lineage

Prompts are knowledge artifacts and must be versioned.

- Product-specific prompts live in `ext-images/<slug>/visual-system/prompts/`.
- Shared prompt snippets (e.g. studio lighting clauses, anti-text guards) live in shared prompt components and are referenced by ID.
- Every approved run records the resolved prompt text and the IDs of any shared snippets used.
- Prompt edits are versioned. The previous prompt is retained for any run record that references it.
- Prompts may not silently embed product identity from another product. Cross-product prompt copy-paste is forbidden.

---

## 5. Conditioning governance

All generation that affects product identity must be conditioned on the canonical PNG or on derivatives of it.

- Conditioning inputs (cutouts, masks, depth, normal, line art, IPAdapter references) live in `ext-images/<slug>/visual-system/conditioning/`.
- Each conditioning input declares: source canonical PNG, derivation method, content hash.
- A conditioning input derived from another product's PNG is forbidden.
- Conditioning inputs are regenerated when the canonical PNG is replaced.

---

## 6. ControlNet / IPAdapter strategy

- ControlNet preprocessors (depth, normal, canny, line art, segmentation) are applied to the canonical PNG or to its component cutouts.
- IPAdapter reference images are limited to: the canonical PNG, OEM visual evidence registered in `source-of-truth/visual-evidence/`, or approved support visuals from the same product.
- Mixing IPAdapter references across products is forbidden.
- Style references that are not product-specific (e.g. lighting moodboards) live in shared visual rules and must be marked as identity-neutral.
- Conditioning strength, weight schedules, and start/end percentages are part of the run record.

---

## 7. Visual provenance

Every approved support visual carries:
- product slug
- source canonical PNG (path + hash)
- workflow registry entry (ID + version + hash)
- run record reference
- conditioning asset references
- approval state
- target delivery surface (web, PDF, support, onboarding, etc.)

Provenance is stored in `ext-images/<slug>/visual-system/qa/selected-assets/` (or equivalent register) and indexed in the lineage manifest.

A visual without complete provenance may not be cited by any delivery surface.

---

## 8. Visual QA rules

Every candidate output passes through QA before approval. QA checks:

- Identity preservation: silhouette, geometry, materials, exterior/interior identity match the canonical PNG.
- Sensor and control layout match the anchor map.
- Visible UI matches the declared UI constraints.
- No invented components, ports, indicators, or surfaces.
- No invented text, logos, or brand marks.
- Hands, fingers, and human elements (if present) pass realism gates.
- Background and environment match the brief; identity-neutral where required.
- Output resolution, color space, and aspect ratio match the delivery target.

QA outcomes:
- `approved` — promoted to selected-assets and eligible for delivery.
- `rejected` — retained in run records with rejection reason.
- `rework` — fed back into prompt/conditioning iteration with notes.

QA records are part of provenance.

---

## 9. Hallucination prevention rules

- The canonical PNG is the truth. Any output that contradicts the canonical PNG is rejected.
- The OEM evidence set bounds the procedural visual context. Outputs may not invent procedures, gestures, or interactions absent from OEM evidence.
- Generated text inside images is forbidden unless it is explicitly conditioned from declared UI strings in `structured-knowledge/`.
- Generated logos, brand marks, certifications, and stamps are forbidden unless they exist in the canonical PNG or registered OEM evidence.
- Generated wiring diagrams, electrical schematics, and topology drawings are forbidden as truth; they must be authored from `structured-knowledge/` and may only be visually illustrated, not invented.
- When in doubt, the output is rejected. There is no "creative license" mode for product truth.

---

## 10. Product identity preservation rules

- Silhouette, geometry, materials, finishes, sensor positions, control positions, exterior/interior surfaces, and visible UI are owned by the canonical PNG.
- An approved support visual must be recognizable as the same product as the canonical PNG.
- Color, lighting, and background may vary across delivery surfaces; identity may not.
- Cropping and component close-ups are allowed, but they must trace back to a region of the canonical PNG via the anchor map.
- A generated "variant" that diverges from the canonical PNG is not the product. It is a rejected candidate.
- If the physical product genuinely changes (new revision), the canonical PNG is replaced via the lineage process in `PHASE_1_IMPLEMENTATION.md` §7. There is no quiet drift.

---

## 11. Authority

This document supersedes any prior ad-hoc visual generation guidance in summary documents at the repository root. ComfyUI-only is non-negotiable for any visual that enters a product nucleus.
