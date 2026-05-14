# Deterministic regression protection

Stability baselines record reviewer-authoritative canonical hashes for export, deployment, audit, and reproducibility artifacts. Regression scans re-derive current hashes against the baseline and report byte-divergence. Baselines and regression scans are append-only. Reviewer remains authoritative for any remediation decision; nothing is automated.
