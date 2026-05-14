/* findings.js — deterministic presentation-layer derivation for the reviewer
   workspace. No inference, no probabilistic logic, no network calls, no FS
   writes. Pure functions of:
     - workflow.file (name, size, last_modified)
     - workflow.summary (reviewer-authored counts)
     - OC.ReviewerWorkflow.ANALYZE_STEPS / ACCEPT_STEPS (existing dispatch maps)

   Constitutional layer 38, schema executable-operational-bindings/1.0.
   NO new runtime, dispatch, schema, or governance family.
*/
(function (global) {
  'use strict';
  const OC = global.OC = global.OC || {};

  // Known product slugs from the existing manual corpus. Pure lookup table —
  // not inference. If none match the file path we render "unspecified".
  const KNOWN_PRODUCTS = Object.freeze([
    'e-flex', 'e-nova', 'e-orbit', 'e-prime', 'e-shield', 'e-touch'
  ]);

  // Extension → evidence-kind classification. Deterministic, exhaustive over
  // the operational evidence set; falls back to "generic-binary".
  const EVIDENCE_BY_EXT = Object.freeze({
    pdf:  { kind: 'pdf-document',     domains: ['text', 'structured'],     ocr: 'recommended' },
    txt:  { kind: 'plain-text',       domains: ['text'],                   ocr: 'not-required' },
    md:   { kind: 'markdown-text',    domains: ['text', 'structured'],     ocr: 'not-required' },
    html: { kind: 'html-text',        domains: ['text', 'structured'],     ocr: 'not-required' },
    json: { kind: 'structured-data',  domains: ['structured'],             ocr: 'not-required' },
    yaml: { kind: 'structured-data',  domains: ['structured'],             ocr: 'not-required' },
    yml:  { kind: 'structured-data',  domains: ['structured'],             ocr: 'not-required' },
    csv:  { kind: 'tabular-data',     domains: ['structured', 'parameters'], ocr: 'not-required' },
    xls:  { kind: 'tabular-data',     domains: ['structured', 'parameters'], ocr: 'not-required' },
    xlsx: { kind: 'tabular-data',     domains: ['structured', 'parameters'], ocr: 'not-required' },
    doc:  { kind: 'word-document',    domains: ['text', 'structured'],     ocr: 'not-required' },
    docx: { kind: 'word-document',    domains: ['text', 'structured'],     ocr: 'not-required' },
    png:  { kind: 'image',            domains: ['visual'],                 ocr: 'required' },
    jpg:  { kind: 'image',            domains: ['visual'],                 ocr: 'required' },
    jpeg: { kind: 'image',            domains: ['visual'],                 ocr: 'required' },
    gif:  { kind: 'image',            domains: ['visual'],                 ocr: 'required' },
    webp: { kind: 'image',            domains: ['visual'],                 ocr: 'required' },
    svg:  { kind: 'vector-image',     domains: ['visual', 'structured'],   ocr: 'not-required' },
    mp4:  { kind: 'video',            domains: ['visual', 'procedure'],    ocr: 'frame-required' },
    mov:  { kind: 'video',            domains: ['visual', 'procedure'],    ocr: 'frame-required' },
    webm: { kind: 'video',            domains: ['visual', 'procedure'],    ocr: 'frame-required' },
    zip:  { kind: 'archive',          domains: ['multi-evidence'],         ocr: 'depends-on-contents' }
  });

  function extOf(name) {
    if (!name) return '';
    const i = name.lastIndexOf('.');
    if (i < 0) return '';
    return name.slice(i + 1).toLowerCase();
  }

  function evidenceFor(file) {
    const ev = EVIDENCE_BY_EXT[extOf(file && file.name)];
    return ev || { kind: 'generic-binary', domains: ['unclassified'], ocr: 'not-required' };
  }

  function inferredProduct(file) {
    const hay = ((file && file.name) || '').toLowerCase();
    for (let i = 0; i < KNOWN_PRODUCTS.length; i++) {
      if (hay.indexOf(KNOWN_PRODUCTS[i]) >= 0) return KNOWN_PRODUCTS[i];
    }
    return 'unspecified';
  }

  function fmtBytes(n) {
    if (!n) return '—';
    if (n < 1024) return n + ' B';
    if (n < 1024 * 1024) return (n / 1024).toFixed(1) + ' KB';
    return (n / (1024 * 1024)).toFixed(2) + ' MB';
  }

  function reviewerActions(wf) {
    const out = [];
    if (!wf) {
      out.push('Select a source file');
      out.push('Click Analyze to orchestrate Phase 52/54/55 dispatches');
      return out;
    }
    if (wf.status === 'analyzed') {
      out.push('Verify or adjust reviewer-authored counts below');
      out.push('Write a one-line acceptance conclusion');
      out.push('Click Accept (Phase 52/54/55/56/58/59 dispatches)');
      out.push('Or Re-analyze to supersede with a new lineage entry');
    }
    if (wf.status === 'accepted') {
      out.push('Export bundle and pipe through tools/governed_fs_executor.py');
      out.push('Optionally Re-analyze to supersede via prior_workflow_id');
    }
    return out;
  }

  function uniquePhases(steps) {
    const seen = {};
    const out = [];
    steps.forEach(function (s) { if (!seen[s.phase]) { seen[s.phase] = true; out.push(s.phase); } });
    return out;
  }

  // --- Findings: reviewer-readable rows derived from the workflow ------------
  // Each row: { label, kind, value?, values?, editable?, hint? }
  // editable.summary_key -> backed by reviewer-authored summary number.
  function deriveFindings(wf) {
    const file = (wf && wf.file) || null;
    const summary = (wf && wf.summary) || {};
    const ev = evidenceFor(file);
    const product = inferredProduct(file);

    return [
      { stage: 'intake', label: 'Source file',           kind: 'text',
        value: file ? file.name : '—',
        hint: file ? (fmtBytes(file.size) + ' · last modified ' +
          (file.last_modified ? new Date(file.last_modified).toISOString().slice(0, 19).replace('T', ' ') : '—')) : null },
      { stage: 'intake', label: 'Evidence kind',         kind: 'badge', value: ev.kind },
      { stage: 'intake', label: 'Inferred product',      kind: 'badge', value: product,
        hint: product === 'unspecified' ? 'No known product slug found in filename — set explicitly downstream.' : null },
      { stage: 'metadata', label: 'Semantic domains',    kind: 'list',  values: ev.domains.slice() },
      { stage: 'metadata', label: 'OCR requirements',    kind: 'badge', value: ev.ocr },
      { stage: 'ocr', label: 'Procedural candidates',    kind: 'number',
        value: summary.procedures_detected || 0,
        editable: { summary_key: 'procedures_detected', min: 0, step: 1 } },
      { stage: 'semantic', label: 'Warning groups',      kind: 'number',
        value: summary.warning_groups || 0,
        editable: { summary_key: 'warning_groups', min: 0, step: 1 } },
      { stage: 'semantic', label: 'Troubleshooting groups', kind: 'number',
        value: summary.troubleshooting_groups || 0,
        editable: { summary_key: 'troubleshooting_groups', min: 0, step: 1 } },
      { stage: 'ocr', label: 'Visual-support requirements', kind: 'number',
        value: summary.visual_support_requirements || 0,
        editable: { summary_key: 'visual_support_requirements', min: 0, step: 1 } },
      { stage: 'synthesis', label: 'Prompt packages',    kind: 'number',
        value: summary.prompt_packages || 0,
        editable: { summary_key: 'prompt_packages', min: 0, step: 1 } },
      { stage: 'convergence', label: 'Canonical candidates',  kind: 'list',
        values: ['extraction-candidate (P52)', 'cross-evidence-fusion (P55)', 'canonical-entity-consolidation (P55)'] },
      { stage: 'convergence', label: 'Downstream impacts',    kind: 'list',
        values: ['manual synthesis (P54)', 'visual-support detection (P54)', 'prompt packaging (P54)',
                 'lifecycle transition (P52)', 'export-runtime record (P54)', 'export stabilization (P55)'] },
      { stage: 'synthesis', label: 'Export implications',     kind: 'text',
        value: ((summary.prompt_packages || 0) > 0)
          ? 'Prompt packages will be emitted under export-runtime-record (P54).'
          : 'Standard manual export envelopes only; no prompt packages declared.' },
      { stage: 'synthesis', label: 'Reviewer-required actions', kind: 'list', values: reviewerActions(wf) }
    ];
  }

  // --- Runtime implications: where this resource lands after Accept ----------
  function deriveImplications(wf) {
    const file = (wf && wf.file) || null;
    const ev = evidenceFor(file);
    const product = inferredProduct(file);
    const RW = OC.ReviewerWorkflow;
    const analyzeKinds = (RW && RW.ANALYZE_STEPS ? RW.ANALYZE_STEPS : []).map(function (s) { return s.kind; });
    const acceptKinds  = (RW && RW.ACCEPT_STEPS  ? RW.ACCEPT_STEPS  : []).map(function (s) { return s.kind; });
    const phases = uniquePhases([].concat(
      RW && RW.ANALYZE_STEPS ? RW.ANALYZE_STEPS : [],
      RW && RW.ACCEPT_STEPS  ? RW.ACCEPT_STEPS  : []
    ));

    const targetTree = product === 'unspecified'
      ? 'runtime-implementation/runtime/<product-to-be-set>/manuals/'
      : 'runtime-implementation/runtime/' + product + '/manuals/';

    const exportReadiness = !wf
      ? 'Pending — no workflow yet.'
      : (wf.status === 'analyzed'
          ? 'Pending Accept; envelopes drafted, no export commit yet.'
          : 'Export-ready; pipe bundle through tools/governed_fs_executor.py.');

    return [
      { stage: 'implications', label: 'Target runtime tree',     kind: 'text',  value: targetTree },
      { stage: 'implications', label: 'Target semantic area',    kind: 'list',  values: ev.domains.slice() },
      { stage: 'implications', label: 'Expected generated entities', kind: 'list', values: analyzeKinds.concat(acceptKinds) },
      { stage: 'implications', label: 'Downstream phases affected',  kind: 'list',
        values: phases.map(function (p) { return 'Phase ' + p; }) },
      { stage: 'implications', label: 'Export readiness',        kind: 'text',  value: exportReadiness },
      { stage: 'implications', label: 'Lineage policy',          kind: 'text',
        value: 'Append-only; Re-analyze creates a successor with prior_workflow_id pointer; nothing is overwritten.' },
      { stage: 'implications', label: 'Reviewer authority',      kind: 'text',
        value: 'Required at Analyze and Accept; runtime fails closed if attribution is missing.' }
    ];
  }

  function derive(wf) {
    return { findings: deriveFindings(wf), implications: deriveImplications(wf) };
  }

  OC.ReviewerFindings = Object.freeze({
    KNOWN_PRODUCTS: KNOWN_PRODUCTS,
    EVIDENCE_BY_EXT: EVIDENCE_BY_EXT,
    evidenceFor: evidenceFor,
    inferredProduct: inferredProduct,
    deriveFindings: deriveFindings,
    deriveImplications: deriveImplications,
    derive: derive
  });
})(typeof window !== 'undefined' ? window : globalThis);
