# Non-Mutation Doctrine

This layer writes only governance documents. It reads no per-product knowledge-core
JSON. It writes no source-of-truth artefact. It modifies no runtime code. The 19/19
runtime test invariant must remain green after every build of this layer.
