/* exec/intake-engine.js — deterministic file -> intake-draft engine. Layer 38. */
(function () {
  "use strict";
  let RULES = null;
  let FORMATS = null;
  let CLASSES = null;
  let TIERS = null;

  const PRODUCT_SLUGS = ["e-orbit", "e-prime", "e-flex", "e-touch", "e-shield", "e-nova"];

  function loadTables() {
    return Promise.all([
      fetch("../execution-engine/format-classification-table.json").then(function (r) { return r.json(); }),
      fetch("../execution-engine/evidence-class-table.json").then(function (r) { return r.json(); }),
      fetch("../execution-engine/trust-tier-table.json").then(function (r) { return r.json(); }),
      fetch("../execution-engine/intake-inference-rules.json").then(function (r) { return r.json(); }),
    ]).then(function (arr) {
      FORMATS = arr[0]; CLASSES = arr[1]; TIERS = arr[2]; RULES = arr[3];
      return { FORMATS: FORMATS, CLASSES: CLASSES, TIERS: TIERS, RULES: RULES };
    });
  }

  function extOf(name) {
    const i = name.lastIndexOf(".");
    return i >= 0 ? name.slice(i).toLowerCase() : "";
  }

  function pickFormat(ext) {
    if (FORMATS && FORMATS.extensions && FORMATS.extensions[ext]) return FORMATS.extensions[ext];
    return FORMATS && FORMATS.fallback ? FORMATS.fallback : { format: "unknown", category: "unknown", default_evidence_class: "unclassified" };
  }

  function pickEvidenceDefault(name, fmtRow) {
    const lower = name.toLowerCase();
    let cls = fmtRow.default_evidence_class;
    let why = "R-EVD-1: format-table default";
    if (lower.indexOf("spec") !== -1 && fmtRow.category === "structured") {
      cls = "vendor-spec-sheet"; why = "R-EVD-2: filename contains 'spec'";
    } else if (lower.indexOf("manual") !== -1 && fmtRow.category === "document") {
      cls = "vendor-document"; why = "R-EVD-3: filename contains 'manual'";
    }
    return { evidence_class: cls, reason: why };
  }

  function pickTrustDefault(cls, name) {
    let tier = "tier-4";
    if (CLASSES && CLASSES.classes) {
      const row = CLASSES.classes.filter(function (c) { return c.id === cls; })[0];
      if (row) tier = row.trust_default;
    }
    let why = "R-TRS-1: evidence-class default";
    if (name.toLowerCase().indexOf("oem") !== -1) { tier = "tier-1"; why = "R-TRS-2: filename contains 'oem'"; }
    return { trust_tier: tier, reason: why };
  }

  function pickProduct(name) {
    const lower = name.toLowerCase();
    for (let i = 0; i < PRODUCT_SLUGS.length; i++) {
      if (lower.indexOf(PRODUCT_SLUGS[i]) !== -1) {
        return { product: PRODUCT_SLUGS[i], reason: "R-PRD-1: filename matches product slug '" + PRODUCT_SLUGS[i] + "'" };
      }
    }
    return { product: null, reason: "no product slug matched" };
  }

  function pickDomain(fmtRow) {
    if (fmtRow.category === "structured") return { domain: "specifications", reason: "R-DOM-1: format-category=structured" };
    if (fmtRow.category === "image")      return { domain: "visual-identity", reason: "R-DOM-2: format-category=image" };
    if (fmtRow.category === "document")   return { domain: "manuals",         reason: "format-category=document" };
    if (fmtRow.category === "video")      return { domain: "visual-identity", reason: "format-category=video" };
    if (fmtRow.category === "archive")    return { domain: "lineage",         reason: "format-category=archive" };
    return { domain: "unknown", reason: "no domain rule matched" };
  }

  function pickRouting(cls, product) {
    const tag = product || "<product>";
    if (cls === "vendor-document")   return { routing: "manuals/" + tag + "/", reason: "R-RTG-1" };
    if (cls === "vendor-spec-sheet") return { routing: "specs/" + tag + "/", reason: "R-RTG-2" };
    if (cls === "vendor-image")      return { routing: "visual-identity/" + tag + "/", reason: "R-RTG-3" };
    return { routing: "unrouted/", reason: "no routing rule matched" };
  }

  function affectedDomains(domain) {
    if (domain === "specifications")  return { affected: ["specifications", "publication"], reason: "R-AFX-1" };
    if (domain === "visual-identity") return { affected: ["visual-identity", "publication"], reason: "R-AFX-2" };
    if (domain === "manuals")         return { affected: ["semantic-domain", "publication", "linguistic"], reason: "manuals impact" };
    return { affected: [], reason: "no affected-domain rule matched" };
  }

  function infer(file) {
    const ext = extOf(file.name);
    const fmtRow = pickFormat(ext);
    const evd = pickEvidenceDefault(file.name, fmtRow);
    const trs = pickTrustDefault(evd.evidence_class, file.name);
    const prd = pickProduct(file.name);
    const dom = pickDomain(fmtRow);
    const rtg = pickRouting(evd.evidence_class, prd.product);
    const afx = affectedDomains(dom.domain);

    const meta = {
      filename: file.name,
      extension: ext,
      filesize_bytes: file.size,
      modified_iso: file.lastModified ? new Date(file.lastModified).toISOString() : null,
    };
    const inferred = {
      format: fmtRow.format,
      format_category: fmtRow.category,
      evidence_class: evd.evidence_class,
      trust_tier: trs.trust_tier,
      product: prd.product,
      domain: dom.domain,
      routing: rtg.routing,
      affected_domains: afx.affected,
    };
    const chain = [
      { rule: "R-FMT-1/2", evidence: "extension '" + ext + "' -> format '" + fmtRow.format + "' (category '" + fmtRow.category + "')" },
      { rule: evd.reason,  evidence: "evidence-class -> '" + evd.evidence_class + "'" },
      { rule: trs.reason,  evidence: "trust-tier -> '" + trs.trust_tier + "'" },
      { rule: prd.reason,  evidence: "product -> " + (prd.product || "(none)") },
      { rule: dom.reason,  evidence: "domain -> '" + dom.domain + "'" },
      { rule: rtg.reason,  evidence: "routing -> '" + rtg.routing + "'" },
      { rule: afx.reason,  evidence: "affected-domains -> [" + afx.affected.join(", ") + "]" },
    ];
    return { meta: meta, inferred: inferred, reasoning_chain: chain };
  }

  window.OC = window.OC || {};
  window.OC.IntakeEngine = { loadTables: loadTables, infer: infer };
})();
