# Publication-Neutral Assemblies

## Rules

- Assemblies declare content + ordering + dependencies; never fonts, layouts, colours, page sizes.
- Assemblies do not embed binary media; they reference media descriptors via visual-intent.
- Assemblies do not embed UI components, widgets, scripts, or chatbot prompts.
- Assemblies do not embed channel-specific transformations (PDF page breaks, web heading levels, etc.).
- Channel adaptation is the responsibility of downstream renderers; the assembly remains canonical.

## Prohibited inline content

- PDF page-break directives
- HTML/CSS markup
- JavaScript
- chatbot prompt templates
- image binaries
- font files
- layout grids
- render-time hints
