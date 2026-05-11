# Production Workflow

## Workflow
1. Identify the manual page, filename, and image slot.
2. Read the product visual profile in `../../ext-images/<slug>/`.
3. Choose the correct realism class from `../visual-rules/realism-vs-schematic.md`.
4. Assemble the prompt from:
   - product visual profile
   - interaction type if needed
   - documentary style
   - lighting standard
   - realism rules
   - negative prompts
5. Generate 3 variants.
6. Review against the checklist and mark the state in `../../products/<slug>/image-production-status.md`.
7. Select one variant, refine only if the product truth still holds.
8. Approve for publication only after visual validation passes.

## State flow
`planned -> generating -> generated -> selected -> approved -> published`

Use `needs-rework`, `rejected`, and `replaced-by-real` when the straight path breaks.
