/* exec/viz.js — vanilla SVG dependency / lifecycle visualisation. Layer 38. */
(function () {
  "use strict";

  function ensureMarker(svg) {
    const NS = "http://www.w3.org/2000/svg";
    let defs = svg.querySelector("defs");
    if (!defs) { defs = document.createElementNS(NS, "defs"); svg.appendChild(defs); }
    if (!svg.querySelector("#arrow")) {
      const m = document.createElementNS(NS, "marker");
      m.setAttribute("id", "arrow"); m.setAttribute("viewBox", "0 0 10 10");
      m.setAttribute("refX", "10"); m.setAttribute("refY", "5");
      m.setAttribute("markerWidth", "8"); m.setAttribute("markerHeight", "8");
      m.setAttribute("orient", "auto-start-reverse");
      const p = document.createElementNS(NS, "path");
      p.setAttribute("d", "M 0 0 L 10 5 L 0 10 z"); p.setAttribute("fill", "#5a86c7");
      m.appendChild(p); defs.appendChild(m);
    }
  }

  function renderGraph(svg, nodes, edges) {
    const NS = "http://www.w3.org/2000/svg";
    while (svg.firstChild) svg.removeChild(svg.firstChild);
    ensureMarker(svg);
    const w = svg.clientWidth || 600;
    const h = svg.clientHeight || 320;
    const cols = Math.max(1, Math.ceil(Math.sqrt(nodes.length)));
    const rows = Math.max(1, Math.ceil(nodes.length / cols));
    const dx = w / (cols + 1);
    const dy = h / (rows + 1);
    const pos = {};
    nodes.forEach(function (n, i) {
      const c = (i % cols) + 1, r = Math.floor(i / cols) + 1;
      pos[n.id] = { x: c * dx, y: r * dy };
    });
    edges.forEach(function (e) {
      const a = pos[e.from], b = pos[e.to];
      if (!a || !b) return;
      const line = document.createElementNS(NS, "line");
      line.setAttribute("x1", a.x); line.setAttribute("y1", a.y);
      line.setAttribute("x2", b.x); line.setAttribute("y2", b.y);
      line.setAttribute("class", "edge-line");
      svg.appendChild(line);
    });
    nodes.forEach(function (n) {
      const p = pos[n.id];
      const rect = document.createElementNS(NS, "rect");
      const lbl  = (n.label || n.id);
      const wpx  = Math.max(60, lbl.length * 6 + 12);
      rect.setAttribute("x", p.x - wpx / 2); rect.setAttribute("y", p.y - 14);
      rect.setAttribute("width", wpx); rect.setAttribute("height", 28);
      rect.setAttribute("rx", 4); rect.setAttribute("class", "node-rect");
      svg.appendChild(rect);
      const t = document.createElementNS(NS, "text");
      t.setAttribute("x", p.x); t.setAttribute("y", p.y + 4);
      t.setAttribute("text-anchor", "middle"); t.setAttribute("class", "node-text");
      t.textContent = lbl; svg.appendChild(t);
    });
  }

  window.OC = window.OC || {};
  window.OC.Viz = { renderGraph: renderGraph };
})();
