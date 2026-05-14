# Operational Flow Testing

Real `unittest` suite covering config, provenance, retrieval, assembly,
safety, supervision, flows, and observability.

Implementation: [test_flows.py](test_flows.py).

## Run

```bash
.venv/bin/python -m unittest discover -s runtime-implementation/testing -p "test_*.py" -v
# or via CLI
.venv/bin/python runtime-implementation/cli.py test
```
