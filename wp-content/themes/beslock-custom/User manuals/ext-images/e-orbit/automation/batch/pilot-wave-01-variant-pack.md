# e-Orbit Pilot Wave 01 Variant Pack

## Purpose
This file turns the first e-Orbit pilot into a generator-ready external batch.

Use it when no raw variants exist yet and the next real step is to create them outside the repository.

## What this file assumes
- The repository remains the source of truth for prompts, validation, and status.
- The actual generation happens in an external tool.
- The canonical visual anchor is `../../source-of-truth/product-images/e-Orbit.png`.
- The instructional context is grounded in:
  - `../../publishing/web/manuals/e-Orbit user manual - image-ready.md`
  - `../../source-of-truth/manuals/e-Orbit app manual.md`

## Shared run settings
- Generate exactly 3 variants per slot.
- Keep the same model family and similar sampling settings within each slot.
- Use image conditioning when the tool supports it, especially for slots 1, 2, and 5.
- Keep denoising or transformation strength low enough to preserve the e-Orbit silhouette.
- Do not let readable fake UI or QR content carry technical meaning.
- Log raw outputs locally as `stable-filename__v01`, `__v02`, and `__v03` before any selection.

## Pilot slots
- Slot 1 / IMG-001 / `e-orbit-hero-main`
- Slot 2 / IMG-002 / `e-orbit-installed-context`
- Slot 5 / IMG-005 / `e-orbit-fingerprint-use`
- Slot 7 / IMG-007 / `e-orbit-app-add-device`
- Slot 8 / IMG-008 / `e-orbit-link-qr`

## Slot 1: e-orbit-hero-main
Manual anchor: product overview and installed identity.
Reference mode: image-to-image recommended.
Aspect: 16:9 horizontal.
Use the base negative prompt from `../../visual-system/prompts/ai-image-prompts.md` plus these additions:
- generic keypad lock silhouette
- front-panel fingerprint sensor
- missing upper sensor cluster
- merged display and handle
- rim-lock box geometry

### Variant A
e-Orbit installed on a real residential door, tall integrated smart lock with a strong vertical black body, visible upper sensor or camera cluster, separate glossy front panel, distinct keypad zone, sculpted exterior handle with fingerprint sensor near the top of the handle, calm indoor lighting, controlled reflections, clean documentary composition for a help center hero image, high definition, realistic materials, no advertising styling

### Variant B
e-Orbit shown in a slightly angled three-quarter installed view on a residential entry door, tall monolithic smart lock body fully readable, upper sensor cluster visible, front display and keypad distinct from the handle, handle geometry preserved, neutral daylight, clean wall and door frame context, technical documentary photo, restrained reflections, realistic black finishes

### Variant C
wide documentary hero of e-Orbit installed in a real apartment or house entrance, lock remains the clear subject while the surrounding door context stays subtle, tall vertical body preserved, upper sensor cluster visible, keypad and handle separated, fingerprint sensor remains on the upper exterior handle, realistic black surfaces with readable reflections, practical help-center framing

## Slot 2: e-orbit-installed-context
Manual anchor: first-use context from the image-ready manual section "Primeros pasos".
Reference mode: image-to-image recommended.
Aspect: 4:3 horizontal.
Use the base negative prompt from `../../visual-system/prompts/ai-image-prompts.md` plus these additions:
- generic simplified smart lock
- knob lock silhouette
- hidden upper sensor cluster
- cropped handle zone
- dark unreadable front panel

### Variant A
e-Orbit already installed and ready for first use on a real home door, tall lock body clearly visible in context, upper sensor cluster present, front keypad area and exterior handle remain distinct, tidy domestic environment, neutral natural light, realistic documentary image for getting-started guidance, balanced reflections on black surfaces

### Variant B
realistic installed-context scene of e-Orbit on a residential door with enough surrounding frame to communicate normal use, tall vertical body preserved, upper front sensor cluster visible, keypad readable as a zone but not as fake text, exterior handle clearly separate, calm documentary style, technically useful composition

### Variant C
e-Orbit shown in a practical first-steps environment with door, jamb, and interior context lightly visible, the lock remains clearly identifiable as a tall integrated smart lock, upper sensor cluster visible, keypad and handle remain separate functional zones, neutral lighting, credible black finishes, understated technical documentation look

## Slot 5: e-orbit-fingerprint-use
Manual anchor: fingerprint enrollment and fingerprint use.
Reference mode: image-to-image strongly recommended.
Aspect: 4:5 vertical.
Use the base negative prompt from `../../visual-system/prompts/ai-image-prompts.md` plus these additions:
- touching the front panel instead of the handle sensor
- fingerprint sensor moved to the panel center
- wrong handle shape
- cropped upper handle area
- glowing sci-fi sensor effect

### Variant A
close realistic documentary image of a person using the e-Orbit fingerprint sensor on the upper exterior handle, finger aligned naturally with the real sensor position, tall product body still partially visible, upper sensor cluster preserved, glossy black surfaces with controlled reflections, soft neutral background blur, high-definition help-center style

### Variant B
vertical close-up of e-Orbit fingerprint interaction on a real installed door, hand approaching the upper handle sensor naturally, the handle shape stays sculpted and distinct from the front panel, upper sensor cluster remains visible in frame, realistic skin, believable reflections, restrained documentary composition

### Variant C
instructional fingerprint-use scene for e-Orbit, emphasis on the correct handle-top sensor position while preserving enough of the lock body to keep model identity unmistakable, separate front panel and handle, realistic black finishes, neutral lighting, clean technical documentation framing

## Slot 7: e-orbit-app-add-device
Manual anchor: Smart Life app pairing flow.
Reference mode: image-to-image optional but recommended for product truth.
Aspect: 4:3 horizontal.
Use the base negative prompt from `../../visual-system/prompts/ai-image-prompts.md` plus these additions:
- phone-only composition
- fake readable app flow
- marketing lifestyle pose
- generic lock body
- missing handle sensor

### Variant A
adult user holding a smartphone near an installed e-Orbit smart lock during initial Smart Life pairing, lock clearly recognizable with tall body, upper sensor cluster, and distinct exterior handle, smartphone screen used only as contextual support, clean domestic setting, documentary technical photo, high definition, calm neutral light

### Variant B
realistic app-pairing scene with e-Orbit installed on a residential door and a smartphone held beside it, the phone remains secondary to the product, tall lock geometry preserved, upper sensor cluster visible, handle and front panel separated, understated help-center composition, soft natural light, no readable fake UI as technical proof

### Variant C
documentary image of Smart Life device-add flow for e-Orbit, user stands near the installed lock with phone in hand, product remains the primary subject, tall vertical body and upper sensor cluster visible, handle sensor still in the correct place, realistic home environment, restrained reflections, practical support-photo framing

## Slot 8: e-orbit-link-qr
Manual anchor: QR linking step where the phone presents a QR code to the lock camera.
Reference mode: image-to-image optional but recommended for product truth.
Aspect: 4:3 horizontal.
Use the base negative prompt from `../../visual-system/prompts/ai-image-prompts.md` plus these additions:
- readable scannable QR treated as proof
- fake app instructions carrying technical meaning
- generic keypad lock silhouette
- missing upper sensor cluster
- phone blocking the lock camera area

### Variant A
realistic QR-linking scene for e-Orbit, smartphone displays a generic non-readable QR-like pattern toward the lock, the upper sensor or camera cluster on the lock remains visible, tall body preserved, exterior handle distinct from the front panel, clean indoor environment, documentary support-photo style, neutral lighting

### Variant B
instructional app-linking image showing a user presenting a phone toward e-Orbit during QR pairing, phone screen stays contextual and not technically readable, lock remains clearly identifiable with tall black body, upper sensor cluster, distinct keypad zone, and separate exterior handle, calm technical documentation look

### Variant C
help-center style QR pairing scene with e-Orbit on a real door, the phone is angled toward the upper sensor cluster without hiding the product shape, tall vertical body preserved, handle and panel remain separate, reflections controlled on black surfaces, realistic domestic background, no promotional styling

## Selection rule after generation
- Keep all 15 raw variants outside Git.
- Review them against `../../visual-system/validations/visual-validation.md` and `../../../../visual-system/shared/generation-guides/review-checklist.md`.
- Log each winning raw filename in `../../metadata/traceability/selected-assets-register.md` before any stable asset is published.
- Do not move slot states beyond `planned` in Git until real outputs exist.

## Notes
- The app-facing slots must stay product-first. If the phone starts to dominate, reject the variant.
- The QR slot is only acceptable if the lock camera or upper sensor area remains readable as the receiving point.
- If any variant drifts into a generic lever lock family, discard it immediately.