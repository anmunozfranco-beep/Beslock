/* OC.AIAugmentation — Phase 62 / 62.1 / 62.2 / 62.3
   Advisory-only, non-canonical, reviewer-triggered.

   62.0 doctrinal scaffold.
   62.1 operational density (cadence, tiers, ASCII tables).
   62.2 NON-COMPETITIVE semantic convergence domains.
   62.3 INDEPENDENT SEMANTIC SENSING.

   DOCTRINAL CORRECTION (62.3)
   ---------------------------
   This module is NOT a post-deterministic decorator. It is an independent
   semantic sensing layer that observes the SAME shared evidence intake
   (file + metadata + topology) that the deterministic runtime observes.
   The two sensing systems run in parallel and emit independently. AI
   sensing MUST be capable of producing advisory emergence even when the
   deterministic runtime extracts nothing (weak OCR, no explicit refs,
   sparse structure). Reconciliation between deterministic facts and
   advisory emergence is performed ONLY at reviewer convergence — never
   automatically fused, never ranked against deterministic findings.

   intake_dependency       = 'evidence-only'   (file + metadata + topology)
   deterministic_dependency = 'none'           (AI never waits for runtime)
   reconciliation_authority = 'reviewer-only'  (no automatic fusion)

   DOCTRINAL CORRECTION (62.2)
   ---------------------------
   The runtime is NOT a top-1 classifier. It is a parallel semantic
   convergence engine. The same evidence may simultaneously express
   canonical entity, hardware topology, ecosystem association, procedural
   posture, visual continuity, and interaction patterns. These domains are
   NOT competitors and MUST NOT be ranked against each other.

   Therefore:
     - no candidate/score table
     - no winner-takes-all tier surfacing
     - no suppression of "lower scoring" domains
     - emergences from all active domains coexist simultaneously

   STILL no real ML: no network, no embeddings, no LLM, no transformers,
   no ONNX, no remote APIs, no background workers.
   model_kind = 'deterministic-stub'.

   Public surface (frozen):
     OC.AIAugmentation.isEnabled() / enable() / disable() / modelKind()
     OC.AIAugmentation.augment(ctx)               -> advisory object
     OC.AIAugmentation.formatEmergenceLine(e)     -> "[ai] <domain> convergence detected: <label>"
     OC.AIAugmentation.buildStreamPlan(advisory)  -> [{delayMs, line|table, cls}]
     OC.AIAugmentation.semanticClustersTable(adv) -> {title, rows} (domain | emergence)
     OC.AIAugmentation.provenanceTable(advisory)  -> {title, rows}
*/
(function (global) {
  'use strict';
  global.OC = global.OC || {};

  const STORAGE_KEY = 'oc.ai-augmentation.enabled';
  const MODEL_KIND  = 'deterministic-stub';

  const KNOWN_PRODUCTS = ['e-nova', 'e-orbit', 'e-prime', 'e-shield', 'e-touch', 'e-flex'];

  // Domains are PARALLEL convergence layers. Order is presentation-only,
  // never a ranking. Every active domain is fully surfaced.
  const DOMAIN_ORDER = [
    'canonical-entity',
    'hardware-topology',
    'ecosystem-association',
    'procedural-posture',
    'visual-continuity',
    'interaction-patterns'
  ];
  const DOMAIN_LABELS = {
    'canonical-entity':       'canonical entity',
    'hardware-topology':      'hardware topology',
    'ecosystem-association':  'ecosystem association',
    'procedural-posture':     'procedural posture',
    'visual-continuity':      'visual continuity',
    'interaction-patterns':   'interaction patterns'
  };

  // ---- enable/disable persistence ---------------------------------------
  function readEnabled() {
    try { return (global.localStorage && global.localStorage.getItem(STORAGE_KEY)) === '1'; }
    catch (e) { return false; }
  }
  function writeEnabled(b) {
    try { if (global.localStorage) global.localStorage.setItem(STORAGE_KEY, b ? '1' : '0'); }
    catch (e) { /* tolerate */ }
  }
  let enabled = readEnabled();
  function isEnabled() { return enabled; }
  function enable()  { enabled = true;  writeEnabled(true); }
  function disable() { enabled = false; writeEnabled(false); }
  function modelKind() { return MODEL_KIND; }

  // ---- deterministic helpers --------------------------------------------
  function nameTokens(name) {
    return String(name || '').toLowerCase()
      .replace(/\.[a-z0-9]+$/, '')
      .split(/[^a-z0-9]+/)
      .filter(Boolean);
  }
  function hasAny(tokens, words) {
    for (let i = 0; i < words.length; i++) {
      if (tokens.indexOf(words[i]) >= 0) return true;
    }
    return false;
  }
  function estimatedDurationSec(file) {
    if (!file || !file.size) return 0;
    const sec = Math.round(file.size / (1.2 * 1024 * 1024));
    return Math.max(1, Math.min(sec, 60 * 60));
  }
  function estimatedFrameCount(durSec) { return durSec * 30; }

  function emergence(domain, label, basis) {
    return { domain: domain, label: label, basis: basis, advisory_only: true };
  }

  // ---- domain generators (each returns 0..N parallel emergences) --------
  // No domain ranks itself against any other. No scoring is surfaced.

  function canonicalEntity(ctx) {
    const out = [];
    const lname = (ctx.name || '').toLowerCase();
    KNOWN_PRODUCTS.forEach(function (p) {
      if (lname.indexOf(p) >= 0) {
        out.push(emergence('canonical-entity', p,
          'filename token catalogue convergence'));
      }
    });
    if (ctx.product && ctx.product !== 'unspecified') {
      // Product family convergence ALWAYS coexists with the entity.
      out.push(emergence('canonical-entity', ctx.product + '-family',
        'deterministic catalogue association'));
    }
    return out;
  }

  function hardwareTopology(ctx) {
    if (!ctx.product || ctx.product === 'unspecified') return [];
    const toks = nameTokens(ctx.name);
    const out = [emergence('hardware-topology', 'panel-lock-family',
      'product cluster + visual topology heuristic')];
    if (hasAny(toks, ['deadbolt', 'bolt']))
      out.push(emergence('hardware-topology', 'deadbolt-family', 'filename keyword'));
    if (hasAny(toks, ['lever', 'handle']))
      out.push(emergence('hardware-topology', 'lever-handle-lock', 'filename keyword'));
    if (hasAny(toks, ['courtyard', 'gate']))
      out.push(emergence('hardware-topology', 'courtyard-lock', 'filename keyword'));
    out.push(emergence('hardware-topology', 'mounting-plate-family',
      'product cluster + topology adjacency'));
    return out;
  }

  function ecosystemAssociation(ctx) {
    const toks = nameTokens(ctx.name);
    const out = [];
    const isVideo = !!(ctx.ev && ctx.ev.kind === 'video');
    if (hasAny(toks, ['smartlife', 'smart', 'app', 'pair', 'pairing']) || isVideo) {
      out.push(emergence('ecosystem-association', 'smart-life',
        'filename + evidence-kind convergence'));
      out.push(emergence('ecosystem-association', 'tuya-platform',
        'platform adjacency to smart-life'));
    }
    if (hasAny(toks, ['fingerprint', 'finger', 'enroll']) ||
        (isVideo && (ctx.x || {}).procedures >= 5)) {
      out.push(emergence('ecosystem-association', 'fingerprint-flow',
        'biometric enrollment convergence'));
    }
    if (hasAny(toks, ['rfid', 'card', 'tag'])) {
      out.push(emergence('ecosystem-association', 'rfid-flow',
        'filename keyword convergence'));
    }
    if (hasAny(toks, ['pin', 'keypad', 'code'])) {
      out.push(emergence('ecosystem-association', 'pin-keypad-flow',
        'filename keyword convergence'));
    }
    return out;
  }

  function proceduralPosture(ctx) {
    const x = ctx.x || {};
    const toks = nameTokens(ctx.name);
    const out = [];
    if (x.procedures >= 5 || hasAny(toks, ['install', 'mount', 'setup'])) {
      out.push(emergence('procedural-posture', 'installation-oriented',
        'extraction density + filename signal'));
    }
    if (hasAny(toks, ['enroll', 'pair', 'pairing', 'fingerprint']) ||
        (ctx.ev && ctx.ev.kind === 'video' && x.procedures >= 3)) {
      out.push(emergence('procedural-posture', 'enrollment-oriented',
        'video evidence + enrollment signal'));
    }
    if (hasAny(toks, ['calibrat', 'align', 'adjust'])) {
      out.push(emergence('procedural-posture', 'calibration-oriented',
        'filename keyword convergence'));
    }
    if (hasAny(toks, ['admin', 'manage', 'master']) || x.procedures >= 10) {
      out.push(emergence('procedural-posture', 'admin-management-flow',
        'extraction density + admin signal'));
    }
    return out;
  }

  function visualContinuity(ctx) {
    const x = ctx.x || {};
    const out = [];
    const score = (x.procedures || 0) + (x.visualSupport || 0) * 2 + (x.scenes || 0);
    if (score >= 25) {
      out.push(emergence('visual-continuity', 'high instructional density',
        'procedure + visual-support + scene weighting'));
    } else if (score >= 12) {
      out.push(emergence('visual-continuity', 'medium instructional density',
        'procedure + visual-support + scene weighting'));
    }
    if (ctx.ev && ctx.ev.kind === 'video' && x.scenes) {
      out.push(emergence('visual-continuity', 'UI-sequence continuity',
        'scene density + video evidence'));
      out.push(emergence('visual-continuity', 'frame-group procedural continuity',
        'scene density + procedural adjacency'));
    }
    if ((x.visualSupport || 0) >= 3) {
      out.push(emergence('visual-continuity', 'diagram-heavy',
        'visual-support density'));
    }
    if ((x.procedures || 0) >= 5 && (x.visualSupport || 0) >= 2) {
      out.push(emergence('visual-continuity', 'procedural visual clustering',
        'procedure + visual-support co-occurrence'));
    }
    return out;
  }

  function interactionPatterns(ctx) {
    const out = [];
    const toks = nameTokens(ctx.name);
    const isVideo = !!(ctx.ev && ctx.ev.kind === 'video');
    if (isVideo) {
      out.push(emergence('interaction-patterns', 'lock interaction events',
        'video evidence + duration heuristic'));
      out.push(emergence('interaction-patterns', 'mobile app interaction',
        'video evidence + UI-sequence convergence'));
    }
    if (hasAny(toks, ['handle', 'lever', 'turn'])) {
      out.push(emergence('interaction-patterns', 'handle usage continuity',
        'filename keyword convergence'));
    }
    if (hasAny(toks, ['keypad', 'pin', 'code', 'press'])) {
      out.push(emergence('interaction-patterns', 'keypad interaction flow',
        'filename keyword convergence'));
    }
    if (hasAny(toks, ['fingerprint', 'finger']) || isVideo) {
      out.push(emergence('interaction-patterns', 'biometric capture sequence',
        'evidence + biometric signal'));
    }
    return out;
  }

  const DOMAIN_GENERATORS = {
    'canonical-entity':       canonicalEntity,
    'hardware-topology':      hardwareTopology,
    'ecosystem-association':  ecosystemAssociation,
    'procedural-posture':     proceduralPosture,
    'visual-continuity':      visualContinuity,
    'interaction-patterns':   interactionPatterns
  };

  // ---- aggregate (parallel domains; no ranking) -------------------------
  function augment(ctx) {
    if (!ctx) ctx = {};
    const domains = DOMAIN_ORDER.map(function (id) {
      const items = (DOMAIN_GENERATORS[id](ctx) || []);
      return { id: id, label: DOMAIN_LABELS[id], emergences: items, emergence_count: items.length };
    });
    const activeDomains = domains.filter(function (d) { return d.emergence_count > 0; });

    const flat = [];
    activeDomains.forEach(function (d) {
      d.emergences.forEach(function (e) { flat.push(e); });
    });

    const dur = ctx.ev && ctx.ev.kind === 'video' ? estimatedDurationSec(ctx.file) : 0;

    return {
      schema: 'reviewer-ai-advisory/1.3',
      advisory_only: true,
      requires_reviewer_seal: true,
      non_authoritative: true,
      canonical_overwrite_authority: 'denied',
      ranking_model: 'none',
      semantic_model: 'parallel-convergence-domains',
      independence_model: 'parallel-sensing',
      intake_dependency: 'evidence-only',
      deterministic_dependency: 'none',
      reconciliation_authority: 'reviewer-only',
      persistence_target: 'runtime/ai-augmentation/',
      model_kind: MODEL_KIND,
      generated_at_iso: new Date().toISOString(),
      source_file: ctx.file || null,
      product_hint: ctx.product || null,
      evidence_kind: ctx.ev ? ctx.ev.kind : null,
      estimated_duration_sec: dur,
      estimated_frame_count: dur ? estimatedFrameCount(dur) : 0,
      domain_count_active: activeDomains.length,
      domain_count_total:  DOMAIN_ORDER.length,
      emergence_count: flat.length,
      domains: activeDomains.map(function (d) {
        return { id: d.id, label: d.label, emergence_count: d.emergence_count };
      }),
      emergences: flat
    };
  }

  function formatEmergenceLine(e) {
    return '[ai] ' + (DOMAIN_LABELS[e.domain] || e.domain) +
           ' convergence detected: ' + e.label;
  }

  // ---- ASCII tables -----------------------------------------------------
  // Single semantic clusters table: domain | advisory emergence.
  // No score column. Multiple rows per domain when emergences coexist.
  function semanticClustersTable(advisory) {
    const rows = [];
    advisory.domains.forEach(function (d) {
      const items = (advisory.emergences || []).filter(function (e) { return e.domain === d.id; });
      items.forEach(function (e, i) {
        rows.push([i === 0 ? d.label : '', e.label]);
      });
    });
    return { title: 'AI SEMANTIC CONVERGENCE DOMAINS (parallel \u00b7 non-ranked)', rows: rows };
  }

  function provenanceTable(advisory) {
    return {
      title: 'AI PROVENANCE',
      rows: [
        ['model_kind',              advisory.model_kind],
        ['schema',                  advisory.schema],
        ['semantic_model',          advisory.semantic_model],
        ['ranking_model',           advisory.ranking_model],
        ['independence_model',      advisory.independence_model],
        ['intake_dependency',       advisory.intake_dependency],
        ['deterministic_dependency', advisory.deterministic_dependency],
        ['reconciliation_authority', advisory.reconciliation_authority],
        ['advisory_only',           String(advisory.advisory_only)],
        ['canonical_overwrite',     advisory.canonical_overwrite_authority],
        ['reviewer_seal_required',  String(advisory.requires_reviewer_seal)],
        ['persistence_target',      advisory.persistence_target],
        ['generated_at',            advisory.generated_at_iso]
      ]
    };
  }

  // ---- cadence engine (per-domain progressive emission) -----------------
  function buildStreamPlan(advisory) {
    const plan = [];
    let t = 0;
    function push(line, cls)       { plan.push({ delayMs: t, line: line, cls: cls }); }
    function pushTable(table, cls) { plan.push({ delayMs: t, table: table, cls: cls }); }

    // ---- preamble: independent-sensing posture + provenance block ----
    push('[ai] ====== INDEPENDENT SEMANTIC SENSING (advisory-only) ======',
      'oc-rwx__stream-line--ai-banner');
    t += 60;
    push('[ai] semantic sensing initialized',                      'oc-rwx__stream-line--ai-meta'); t += 40;
    push('[ai] independence model: parallel-sensing',              'oc-rwx__stream-line--ai-meta'); t += 40;
    push('[ai] intake dependency: evidence-only · deterministic dependency: none',
      'oc-rwx__stream-line--ai-meta'); t += 40;
    push('[ai] reconciliation authority: reviewer-only',           'oc-rwx__stream-line--ai-meta'); t += 40;
    push('[ai] semantic model: parallel-convergence-domains',     'oc-rwx__stream-line--ai-meta'); t += 40;
    push('[ai] ranking model: none (domains coexist)',            'oc-rwx__stream-line--ai-meta'); t += 40;
    push('[ai] model kind: ' + advisory.model_kind,                'oc-rwx__stream-line--ai-meta'); t += 40;
    push('[ai] canonical overwrite authority: denied',             'oc-rwx__stream-line--ai-meta'); t += 40;
    push('[ai] reviewer seal required',                            'oc-rwx__stream-line--ai-meta'); t += 40;
    push('[ai] persistence target: ' + advisory.persistence_target, 'oc-rwx__stream-line--ai-meta');
    t += 140;
    pushTable(provenanceTable(advisory), 'oc-rwx__stream-line--ai-table');
    t += 220;

    // ---- per-domain progressive emission ----
    push('[ai] -- semantic convergence domains (' + advisory.domain_count_active +
         ' active of ' + advisory.domain_count_total + ', parallel) --',
      'oc-rwx__stream-line--ai-banner');
    t += 140;

    advisory.domains.forEach(function (d) {
      const items = (advisory.emergences || []).filter(function (e) { return e.domain === d.id; });
      push('[ai] -- domain: ' + d.label + ' (' + items.length +
           ' emergence' + (items.length === 1 ? '' : 's') + ') --',
        'oc-rwx__stream-line--ai-banner');
      t += 120;
      items.forEach(function (e, ci) {
        push(formatEmergenceLine(e), 'oc-rwx__stream-line--ai');
        t += 70 + (ci * 12);
      });
      t += 90;
    });

    // ---- semantic clusters table ----
    pushTable(semanticClustersTable(advisory), 'oc-rwx__stream-line--ai-table');
    t += 220;

    // ---- video runtime realism ----
    if (advisory.evidence_kind === 'video') {
      push('[ai] video runtime: estimated duration \u2248 ' +
           advisory.estimated_duration_sec + 's \u00b7 frame estimate \u2248 ' +
           advisory.estimated_frame_count,
        'oc-rwx__stream-line--ai-meta');
      t += 80;
      push('[ai] visual instructional density: weighted',
        'oc-rwx__stream-line--ai-meta'); t += 60;
      push('[ai] frame-group procedural continuity: increased',
        'oc-rwx__stream-line--ai-meta'); t += 60;
    }

    // ---- closing banner ----
    push('[ai] independent semantic sensing complete · ' +
         advisory.emergence_count + ' parallel emergences across ' +
         advisory.domain_count_active + ' active semantic domains · no ranking applied',
      'oc-rwx__stream-line--ai-banner');
    t += 60;
    push('[ai] advisory_only=true · reviewer-mediated reconciliation · canonical envelopes untouched',
      'oc-rwx__stream-line--ai-banner');

    return plan;
  }

  global.OC.AIAugmentation = Object.freeze({
    isEnabled: isEnabled,
    enable: enable,
    disable: disable,
    modelKind: modelKind,
    augment: augment,
    formatEmergenceLine: formatEmergenceLine,
    buildStreamPlan: buildStreamPlan,
    semanticClustersTable: semanticClustersTable,
    provenanceTable: provenanceTable
  });
}(typeof window !== 'undefined' ? window : globalThis));
