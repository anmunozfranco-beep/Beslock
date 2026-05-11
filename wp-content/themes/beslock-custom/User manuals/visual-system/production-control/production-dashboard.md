# Production Dashboard

## System metrics
- Products in scope: 6
- Planned image slots: 66
- Product visual profiles completed: 6/6
- Product status trackers completed: 6/6
- Product validation checklists completed: 6/6
- Product-local canonical prompt packs completed: 6/6
- Product-local canonical matrices completed: 6/6
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
| e-Prime | canonical | prompt pack + matrix + tracker + validation | slim long-plate lock with hub-ring sensor |
| e-Shield | canonical | prompt pack + matrix + tracker + validation | split-body rim-lock with handle-free exterior slab |

## Canonical rule
When a product is marked `canonical`, new visual production work should start from the files inside `visual-system/products/<slug>/`.
All six products are now canonical.

## Immediate next production steps
1. Run the first end-to-end generation pilot with e-Orbit slots 1, 2, 5, 7, and 8.
2. Start creating selected outputs in each product `generated/` folder only after validation passes.
3. Replace AI support imagery with real captures where the product or app truth requires it.
