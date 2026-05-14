# Deployment Composition Philosophy

Compositions are declared per environment and per trust zone.

## Principles

- Compositions are declared per environment and per trust zone.
- Compositions never silently include modules outside their authorization.
- Compositions emit manifests; manifests are the basis for replay.
- Compositions are revocable; rollback is a first-class composition action.
