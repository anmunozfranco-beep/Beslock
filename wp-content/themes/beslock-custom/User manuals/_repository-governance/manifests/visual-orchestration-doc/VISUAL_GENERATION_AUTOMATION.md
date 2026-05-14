# Visual Generation Automation

This repository now includes `visual_generation.py`, a Python CLI for the first visual-system automation stages:

1. export canonical prompts and job metadata to JSON manifests
2. render or submit Comfy Cloud workflow variants from those manifests
3. score downloaded candidates with basic local quality heuristics
4. prepare controlled product-reference packs for hybrid workflows
5. composite exact product cutouts over generated backgrounds

## Prerequisites

- Activate the repository virtual environment or use the configured interpreter in `.venv/`.
- For scoring, ensure `Pillow` is installed in the active environment.
- For live Comfy Cloud execution, use a Creator or Pro Comfy Cloud plan, create an API key at `https://platform.comfy.org/profile/api-keys`, and make it available as `COMFY_CLOUD_API_KEY`.
- `visual_generation.py` also loads repository-root `.env.local` automatically if present. Use that file for local secrets; do not put `COMFY_CLOUD_API_KEY` in the tracked `.env` used by the Docker stack.

## Export Manifests

Export one product:

```bash
.venv/bin/python visual_generation.py export --product e-orbit
```

Export all canonical products:

```bash
.venv/bin/python visual_generation.py export
```

Default output location:

```text
output/visual-generation/manifests/
```

Each manifest includes:

- product reference paths
- manual JSON context
- strict image intent derived from manual sections plus prompt-pack contract fields
- per-slot prompt, negative prompt, class, priority, and status
- derived dimensions from the canonical format field

## Strict Image Intent Layer

Manifest export is now expected to derive each job from two sources at once:

1. the authored slot prompt in the product prompt pack
2. the closest matching sections in `generated_manuals/<product>/manual.json`

Each exported job can now carry these prompt-contract fields:

- `visual_mode`
- `product_slice`
- `instructional_goal`
- `text_truth_policy`
- `overlay_plan`
- `manual_section_hints`
- `manual_keywords`

Those fields are resolved into:

- `image_intent`
- `manual_graphics_lane`
- stricter generated prompt and negative prompt contracts
- editorial follow-up tasks for non-photographic manual graphics

Recommended usage:

- use `visual_mode: schematic-outline` when the graphic should read as contextual line work rather than realism
- use `product_slice` when only the panel, handle sensor, battery area, or another local zone should be shown
- use `text_truth_policy: keypad-numerals-visible` when a real keypad or integrated numeral surface must show its printed numbers clearly as part of the hardware
- use `text_truth_policy: no-readable-ui` whenever generated menus, digits, or labels must not become technical proof
- use `manual_section_hints` and `manual_keywords` to force export to anchor the prompt to the right manual sections

## Dry Run Workflow Rendering

Use `--dry-run` to validate prompt injection and workflow mutation without calling Comfy Cloud:

```bash
.venv/bin/python visual_generation.py run \
  --manifest output/visual-generation/manifests/e-orbit-generation-manifest.json \
  --workflow path/to/workflow_api.json \
  --job e-orbit-hero-main \
  --variant-count 3 \
  --positive-node 10 \
  --negative-node 11 \
  --seed-node 12 \
  --reference-image-node 13 \
  --width-node 14 \
  --height-node 14 \
  --filename-prefix-node 16 \
  --dry-run
```

This writes:

- `run-summary.json`
- one rendered workflow JSON per candidate variant
- one job record per candidate variant

Default run root:

```text
output/visual-generation/runs/<product-slug>/<timestamp>/
```

## Live Comfy Cloud Execution

Once the workflow node mapping is correct, remove `--dry-run` and optionally add `--wait`:

This repository does not ship a production Comfy workflow JSON. You must provide your own exported API-format workflow file via `--workflow`.

To obtain the two missing inputs for a real run:

- Workflow JSON: open your workflow in ComfyUI and export it with the frontend's `Save (API Format)` option. Comfy Cloud accepts that API-format graph at `POST /api/prompt`.
- Cloud API key: log in at `https://platform.comfy.org/login`, open `https://platform.comfy.org/profile/api-keys`, click `+ New`, name the key, click `Generate`, and save it immediately. Comfy only shows the value once.

Recommended local secret file:

```bash
cat > .env.local <<'EOF'
COMFY_CLOUD_API_KEY=replace-with-your-key
EOF
```

```bash
.venv/bin/python visual_generation.py run \
  --manifest output/visual-generation/manifests/e-orbit-generation-manifest.json \
  --workflow path/to/workflow_api.json \
  --positive-node 10 \
  --negative-node 11 \
  --seed-node 12 \
  --reference-image-node 13 \
  --width-node 14 \
  --height-node 14 \
  --filename-prefix-node 16 \
  --variant-count 3 \
  --wait
```

Live mode will:

- upload the product reference image when `--reference-image-node` is set
- submit one workflow per candidate variant to `POST /api/prompt`
- optionally poll until completion
- download final outputs into the candidate folder

## Score Candidates

Score the latest run for the manifest product:

```bash
.venv/bin/python visual_generation.py score \
  --manifest output/visual-generation/manifests/e-orbit-generation-manifest.json
```

Or score a specific run:

```bash
.venv/bin/python visual_generation.py score \
  --manifest output/visual-generation/manifests/e-orbit-generation-manifest.json \
  --run-dir output/visual-generation/runs/e-orbit/20260511T211849Z
```

The scorer writes:

- `score-summary.json` at the run root
- `score-report.json` in each candidate folder

Current heuristics are intentionally narrow:

- aspect-ratio mismatch
- undersized outputs
- low edge energy as a blur proxy
- low contrast
- too dark or too bright
- exact duplicate detection by SHA-256

The scorer always leaves `requires_manual_truth_check: true` in the summary because product-truth validation is still human-gated.

## Prepare Controlled References

Use `prepare-reference` to isolate the exact product body from a clean source image and emit a reusable pack with:

- a transparent subject cutout
- a grayscale subject mask
- a centered transparent guide image
- a centered white-background guide image

Example for the exterior e-Orbit face:

```bash
.venv/bin/python visual_generation.py prepare-reference \
  --input "wp-content/themes/beslock-custom/User manuals/ext-images/e-orbit.webp" \
  --output-dir output/visual-generation/reference-prep/e-orbit-front \
  --crop-box 430,20,830,900 \
  --canvas-size 1024x1024
```

This is useful when the raw product reference contains multiple views or too much white margin and you need a tighter, geometry-preserving input for image-to-image or later compositing.

## Hybrid Composite Proofs

Use `composite` to overlay an exact prepared cutout over a generated environment, preserving product geometry while keeping generated lighting and setting context:

```bash
.venv/bin/python visual_generation.py composite \
  --background output/visual-generation/runs/e-orbit/<timestamp>/candidates/e-orbit-hero-main/v01/example.png \
  --foreground output/visual-generation/reference-prep/e-orbit-front/subject-cutout.png \
  --output output/visual-generation/composites/e-orbit/e-orbit-hero-main-hybrid.jpg \
  --fit-height-ratio 0.82 \
  --anchor bottom-center \
  --x-offset 32 \
  --y-offset -24
```

The hybrid composite is a repo-side proof path for technical-manual imagery when direct generation preserves scene quality but still drifts the lock geometry.

## Manual Graphics Briefs

Use `manual-graphics-brief` when a slot needs more than a raw prompt. This command packages the strict `image_intent`, the resolved prompt contract, the matched manual sections, and the expected editorial tasks into JSON and Markdown outputs.

Example:

```bash
.venv/bin/python visual_generation.py manual-graphics-brief \
  --manifest output/visual-generation/manifests/e-flex-generation-manifest.json \
  --job e-flex-language-settings \
  --run-dir output/visual-generation/runs/e-flex/<timestamp>
```

This is the intended lane for graphics where:

- the model should only generate the base visual
- the repo-side process still needs crops, callouts, replacements, or overlays
- the manual text must stay stricter than the generated pixels

## Write Back Tracker State

Once a run has been scored, sync the recommended variant back into the canonical markdown trackers:

```bash
.venv/bin/python visual_generation.py writeback \
  --manifest output/visual-generation/manifests/e-orbit-generation-manifest.json \
  --run-dir output/visual-generation/runs/e-orbit/<timestamp> \
  --dry-run
```

This updates:

- `image-production-status.md`
- `generated/selected-assets-register.md`

Default behavior:

- uses `score-summary.json` to mark the recommended winner as `selected`
- updates existing rows when present
- adds missing register rows when the job was not pre-listed
- leaves publication and human validation as separate later steps

You can also mark coverage without selecting a winner yet:

```bash
.venv/bin/python visual_generation.py writeback \
  --manifest output/visual-generation/manifests/e-orbit-generation-manifest.json \
  --run-dir output/visual-generation/runs/e-orbit/<timestamp> \
  --state generated \
  --dry-run
```

## Important Comfy Cloud Note

The Comfy Cloud docs state that API access requires a Creator or Pro subscription tier. Free and Standard do not include API access. `--dry-run` remains useful regardless because it validates the repo-side automation contract before any API call.