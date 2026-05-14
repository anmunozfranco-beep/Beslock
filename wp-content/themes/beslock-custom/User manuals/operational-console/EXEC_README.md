# Operational Console — executable layer (phase 45 / layer 38)

Open `exec.html` directly in a browser, or serve the repo root with:

```
python3 -m http.server 8000
```

and browse to `http://localhost:8000/wp-content/themes/beslock-custom/User%20manuals/operational-console/exec.html`.

The exec layer never makes a network call. It uses only `File`, `Blob`, `URL`, `localStorage` and SVG. All operator actions emit append-only draft manifests stored locally; promotion is out-of-band through reviewer governance.
