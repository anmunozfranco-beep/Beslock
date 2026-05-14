# Linguistic renderers (publication-time only)

Four pure utility modules:

- `linguistic_normalizer.py` — OCR cleanup + OEM translation normalisation.
- `terminology_enforcer.py` — alias → canonical Colombian-Spanish term substitution.
- `readability_normalizer.py` — readability defect detector (does not rewrite).
- `warning_language_renderer.py` — Colombian-Spanish warning rendering (severity preserved).

Hard rules:

- pure functions; no file mutations; no knowledge-core access; no network.
- defects are surfaced, never silently fixed.
- NOT yet wired into `tools/publication_renderer.py` — wiring is the next executable track.
