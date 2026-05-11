# Production Dashboard

## System metrics
- Products in scope: 6
- Planned image slots: 66
- Product visual profiles completed: 6/6
- Product status trackers completed: 6/6
- Product validation checklists completed: 6/6
- Product-local canonical prompt packs completed: 4/6
- Product-local canonical matrices completed: 4/6
- Shared prompt modules completed: yes
- Shared interaction modules completed: yes
- Actual generated assets committed in this system: 0

## Current operational interpretation
The repo now has the minimum control surfaces needed to run image production deliberately instead of treating it as scattered prompt writing.

## Product migration index

| Product | Migration state | Canonical product-local files | Notes |
|---|---|---|---|
| e-Orbit | canonical | prompt pack + matrix + tracker + validation | reference implementation and first pilot slice |
| e-Nova | canonical | prompt pack + matrix + tracker + validation | product-truth override for knob geometry |
| e-Touch | canonical | prompt pack + matrix + tracker + validation | handle-led product with no keypad slab |
| e-Flex | canonical | prompt pack + matrix + tracker + validation | long-plate lever lock with handle-face sensor |
| e-Prime | scaffolding only | tracker + validation | still depends on root-level flat prompt docs |
| e-Shield | scaffolding only | tracker + validation | still depends on root-level flat prompt docs |

## Canonical rule
When a product is marked `canonical`, new visual production work should start from the files inside `visual-system/products/<slug>/`.
When a product is marked `scaffolding only`, the product has validation and tracking in place but still depends on the legacy root-level prompt pack and matrix.

## Immediate next production steps
1. Canonize e-Prime and e-Shield to finish the product-local migration.
2. Run the first end-to-end generation pilot with e-Orbit slots 1, 2, 5, 7, and 8.
3. Publish generated outputs into each product `generated/` folder only after validation passes.
