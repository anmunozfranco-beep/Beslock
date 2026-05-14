# Operational Rendering Principles

Rendering is deterministic given identical inputs and manifest. Identical inputs produce identical outputs across formats (within each format's lossless guarantees).

## Tenets

- determinism is a renderer requirement, not an aspiration
- lossy formats MUST disclose what is lost
- structured-runtime is source-of-truth; other formats derive from it
