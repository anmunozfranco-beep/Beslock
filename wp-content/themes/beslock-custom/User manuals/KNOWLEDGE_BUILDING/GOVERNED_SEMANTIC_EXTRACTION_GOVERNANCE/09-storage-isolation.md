# 09-storage-isolation

Extraction artifacts are isolated under semantic-extraction-runtime/. The runtime NEVER writes into publication-composition-runtime, visual-publication-builds, visual-generation-runtime, knowledge-core, governance, runtime-implementation, runtime-manifests payloads, OEM source assets, or live publications.
