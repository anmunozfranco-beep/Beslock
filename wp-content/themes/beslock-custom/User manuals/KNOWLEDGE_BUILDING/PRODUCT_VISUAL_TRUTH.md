# PRODUCT VISUAL TRUTH

Status: Active governance.
Scope: Visual identity preservation for every BESLOCK product.
Authority: Overrides any other visual-generation guidance for matters of product identity.
Companion documents: `COMFY_GENERATION_GOVERNANCE.md`, `PROVENANCE_AND_LINEAGE.md`, `PHASE_1_IMPLEMENTATION.md`.

---

## 1. Critical context

Each BESLOCK product currently has **exactly one** real PNG product image:

```
ext-images/<slug>/source-of-truth/product-images/<Product>.png
```

That PNG is the **absolute visual source of truth** for the product. There is no second canonical image. There is no "alternate angle" canonical. There is no rendered-from-CAD canonical. The single PNG governs.

Every other visual artifact — cutouts, masks, conditioning assets, OEM diagram captures, generated support visuals, rendered scenes — is a **derivative**. Derivatives may not redefine the product.

Compatibility PNGs at the `ext-images/` root (e.g. `e-Flex.png`, `e-Nova.png`) are legacy, not canonical, and are scheduled for retirement once each nucleus owns its canonical PNG.

---

## 2. What is the canonical PNG

The canonical PNG is the editorial/photographic representation chosen as the product's visual record. It governs:

- **Silhouette** — the outer boundary of the product as seen.
- **Geometry** — proportions, dimensions ratios, edge curvature, panel transitions.
- **Materials and finishes** — visible surface treatments, gloss/matte, glass/metal/polymer regions.
- **Sensor layout** — visible sensor positions (touch, fingerprint, RFID antenna location, IR, microphone).
- **Control layout** — visible buttons, keypad grid, knob, lever, dial positions.
- **UI layout** — visible screen positions, indicator LED positions, label positions.
- **Handle / lever** — handle geometry, mounting orientation, finish.
- **Exterior/interior identity** — the side depicted is the side governed; opposite-side claims require explicit OEM evidence.

If a property is visible in the canonical PNG, the canonical PNG governs that property. Period.

---

## 3. Immutable visual attributes

The following attributes are **immutable**. No generation, transformation, or stylization may alter them:

1. Silhouette (outer boundary).
2. Component count and component positions visible in the canonical PNG.
3. Sensor positions and sensor count.
4. Keypad grid layout (row/column count, key spacing).
5. Screen position, size, and aspect ratio.
6. Indicator LED positions.
7. Handle/lever geometry and mounting orientation.
8. Visible mounting hardware positions (screws, bezels, gaskets).
9. Material identity per visible region (glass region stays glass; metal region stays metal).
10. Brand marks, logos, certifications visible in the canonical PNG (kept exactly as depicted; never invented).

Tolerances (used by visual QA in `COMFY_GENERATION_GOVERNANCE.md` §8):
- Position drift: ≤ 4 px on a normalized 1024-px reference.
- Rotation drift: ≤ 1°.
- Scale drift: ≤ 1%.
- Material region drift: 0 px (regions may not bleed across boundaries).

---

## 4. Geometry preservation rules

- Geometry is anchored from the canonical PNG to a per-product anchor map at `ext-images/<slug>/visual-system/anchors/`.
- Anchor maps record normalized coordinates (0–1) for each tracked component, sensor, control, screen, indicator, handle, and mounting point.
- Every visual constraint (`KNOWLEDGE_SCHEMA.md` §3.11) references an anchor entry.
- Generated outputs are validated against the anchor map. Outputs that violate tolerances are rejected.

Allowed geometry operations:
- Crop to a region defined by the anchor map.
- Re-light without changing geometry.
- Re-background without changing geometry.

Forbidden geometry operations:
- "Cleaning up" the silhouette.
- Straightening curves.
- Repositioning a sensor "for clarity".
- Replacing a handle with a different style.
- Adding a port, button, or indicator that is not in the canonical PNG.

---

## 5. Sensor preservation rules

- Sensor identity, count, and position are immutable.
- A sensor visible in the canonical PNG must appear in every rendered view that includes its region.
- A sensor not visible in the canonical PNG must not appear, even if "common" for similar products.
- Sensor labels (e.g. fingerprint icon) are kept exactly as depicted; they may not be redrawn in a different style.

---

## 6. UI-layout preservation

- Screen position, aspect ratio, and bezel are immutable.
- On-screen content is allowed to vary **only** when the displayed strings are sourced from declared UI strings in `structured-knowledge/` (see `KNOWLEDGE_SCHEMA.md` §3.4).
- Generated UI text is otherwise forbidden. Imagery may not invent menu items, status messages, or icons.
- Indicator LEDs may change color/state to depict an operational state declared in `structured-knowledge/` (`operational-state` entity), provided the LED position is unchanged.

---

## 7. Handle preservation

- Handle geometry, mounting orientation, and finish are immutable.
- Handle position relative to the body is immutable.
- Mirroring a handle (left-handed vs right-handed) is **not** a generation operation. If the product supports a mirrored install, a separate canonical PNG is required (see §13).
- Generated views that show the handle from a different angle must derive that angle from the canonical PNG via compositing or 3D-from-2D inference, not from invention.

---

## 8. Silhouette preservation

- The outer boundary of the product is sacred.
- Silhouette is extracted into a mask at `ext-images/<slug>/visual-system/anchors/silhouette.png` (or equivalent) and used as a mandatory ControlNet input for any generated view of the full product.
- A generated view that violates the silhouette mask is rejected.
- Silhouette tolerance: ≤ 2 px on a normalized 1024-px reference.

---

## 9. Material preservation

- Each visible region of the canonical PNG is classified by material in the anchor map.
- Generated outputs must respect the material classification per region.
- A region classified `glass-touch` may not render as `brushed-metal`, even under stylized lighting.
- Re-lighting that changes specular response is allowed; re-lighting that changes apparent material is rejected.

---

## 10. Rendering constraints

For every generated view of the product:

Required ControlNet/IPAdapter inputs:
- Silhouette mask (always).
- Depth map derived from canonical PNG (when full product or major components are shown).
- IPAdapter reference: the canonical PNG (always) or an approved support visual of the same product (never another product).

Required prompt clauses (anti-hallucination guards):
- Anti-text guard: "no text, no logos invented, no labels invented" (or registered shared snippet).
- Anti-extra-component guard: "no additional buttons, no additional sensors, no additional indicators".
- Material guard: per-region material declarations sourced from the anchor map.

Forbidden prompt clauses:
- "Reimagined", "redesigned", "modernized", "improved", "stylized variant".
- Any clause that invites identity drift.

---

## 11. What AI is allowed to modify

Allowed modifications (when generated through ComfyUI per `COMFY_GENERATION_GOVERNANCE.md`):

1. Lighting: studio, ambient, directional, time-of-day moods.
2. Background: solid color, gradient, environmental scene (without inventing product context).
3. Camera distance and framing within the canonical PNG region (zoom in to a component, frame a wider context).
4. Camera angle within tight bounds derived from the canonical PNG (small parallax shifts, never new sides).
5. Operational state depiction via indicator LED color/state (when sourced from `operational-state` entity).
6. On-screen UI content (when sourced from declared UI strings).
7. Hand/finger interactions for procedure illustration, when the product geometry remains intact.
8. Compositing into installation contexts (door, frame, wall) where the product itself is unchanged.

---

## 12. What AI is NOT allowed to modify

Explicitly forbidden modifications:

1. Silhouette.
2. Component geometry.
3. Component count.
4. Component position.
5. Sensor identity, count, or position.
6. Keypad grid.
7. Screen size, aspect ratio, or position.
8. Handle geometry, position, finish, or orientation.
9. Material identity per region.
10. Brand marks, logos, certifications (presence, absence, content, position).
11. Mounting hardware positions.
12. The "side" of the product depicted (front becomes back, exterior becomes interior).
13. Any feature not present in the canonical PNG.
14. Any text not sourced from declared UI strings in `structured-knowledge/`.

A generation that requires any of these modifications is the wrong tool. Use compositing (§13) or fall back to the real PNG (§14).

---

## 13. When compositing is required instead of generation

Use compositing (cutout + placement + relighting) instead of generation when:

1. The required view is a different side of the product not depicted in the canonical PNG.
2. The required view is an explicit hand-on-product interaction where the product must remain pixel-faithful.
3. The required view places the product into an installation context (door, frame, wall, environment).
4. The required view shows multiple products together (catalog grids, comparison shots).
5. The required view requires guaranteed brand/logo accuracy.
6. The visual is intended for legal, certification, or regulatory delivery.

Compositing pipeline (deterministic, ComfyUI-orchestrated):
- Source: canonical PNG.
- Cutout: from `visual-system/anchors/silhouette.png` (or a re-derivation).
- Background: shared identity-neutral environment or product-local installation context.
- Relighting: ComfyUI relighting node with the cutout mask; geometry untouched.
- Output sidecar provenance: identical to a generated visual (`PROVENANCE_AND_LINEAGE.md` §11.4) with `transformation_type: composite`.

Compositing is preferred over generation whenever both options are available.

---

## 14. When workflows must fall back to the real PNG

Mandatory fallback to the real PNG (no generation, no compositing alteration):

1. Hero / primary product imagery on web, PDF, and support surfaces.
2. Catalog imagery used for purchase decisions.
3. Specification-sheet imagery.
4. Any imagery cited as the "product image" in delivery contracts.
5. Any imagery rendered next to legal text, certifications, or warranty information.
6. Any imagery accompanying technical specifications where dimensional accuracy matters.
7. Any imagery used in onboarding flows where users must visually identify the product they own.

Fallback rule: if visual QA cannot certify a generated or composited output meets §3 tolerances, the canonical PNG is used directly. There is no degraded-quality fallback chain.

---

## 15. Hallucination prevention rules (visual)

This section restates and tightens `COMFY_GENERATION_GOVERNANCE.md` §9 in the context of visual truth.

- The canonical PNG is the truth oracle. Disagreement = rejection.
- Generated text inside images is forbidden unless sourced from declared UI strings.
- Generated logos, brand marks, certifications, and stamps are forbidden unless they exist in the canonical PNG or registered OEM evidence.
- Generated wiring diagrams, schematics, and topology drawings are forbidden as truth; they are authored from `structured-knowledge/` and may be illustrated, not invented.
- "Plausible" features (a missing port, a "natural" indicator) are not valid additions.
- Visual style consistency with the canonical PNG outranks visual style consistency with other generated outputs.
- When a generation is "almost right but the keypad is wrong", it is wrong.

---

## 16. Alignment with ComfyUI-only governance

This document operates entirely within the boundaries of `COMFY_GENERATION_GOVERNANCE.md`:

- All visual operations described here are ComfyUI-orchestrated.
- All run records conform to the schema in `COMFY_GENERATION_GOVERNANCE.md` §3 and `PROVENANCE_AND_LINEAGE.md` §7.
- All workflows used are registered in `tools/comfy/` per `COMFY_GENERATION_GOVERNANCE.md` §2.
- All conditioning inputs derive from the canonical PNG or from registered OEM visual evidence.

No ad-hoc image editor, no web-based generator, no one-off script may produce visuals that enter a product nucleus. Manual photo retouching of the canonical PNG itself is a deliberate replacement operation (`PROVENANCE_AND_LINEAGE.md` §13), not a routine edit.

---

## 17. Alignment with deterministic rendering philosophy

- Same canonical PNG + same workflow + same conditioning + same prompt + same seed → same output.
- Every approved output is reproducible from its run record.
- "Looks better today" is not a valid reason to replace an approved support visual; replacement requires a new run record and a recorded justification.
- Visual drift across product nuclei is forbidden; deterministic rendering is the mechanism that prevents it.

---

## 18. Operational priorities

The visual truth system optimizes for, in this order:

1. **Operational accuracy** — users must be able to identify the product they own.
2. **Onboarding clarity** — users must be able to follow procedures because the depicted product matches reality.
3. **Technical trustworthiness** — support, certification, and legal contexts require pixel-faithful imagery.
4. **Reproducibility** — every approved support visual must be re-derivable.
5. **Aesthetic quality** — pursued only after the four priorities above are satisfied.

Aesthetic quality never overrides identity preservation.

---

## 19. Conformance

A nucleus is visual-truth-conforming when:
1. The canonical PNG exists at the prescribed path.
2. The silhouette mask and anchor map exist under `visual-system/anchors/`.
3. Every approved support visual carries a provenance sidecar (`PROVENANCE_AND_LINEAGE.md` §11.4).
4. Every approved support visual references the canonical PNG as a parent.
5. No support visual depicts a feature absent from the canonical PNG.
6. No support visual contradicts the silhouette mask within tolerance.
7. Hero / catalog / spec imagery resolves to the canonical PNG, not to a generated derivative.

A non-conforming nucleus may not publish visuals to delivery surfaces.
