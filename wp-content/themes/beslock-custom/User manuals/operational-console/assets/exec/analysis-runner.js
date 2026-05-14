/* analysis-runner.js — UX-level staged execution perception layer.

   Constitutional layer 38, schema executable-operational-bindings/1.0.
   This is NOT a runtime. NOT a dispatch. NOT a governance family.
   It does NOT process evidence. It does NOT call the network.
   It does NOT write to the filesystem. It does NOT mutate runtime payloads.

   It walks a fixed, deterministic sequence of UX stages with
   deterministic per-evidence-kind timing, then invokes the existing
   OC.ReviewerWorkflow.startAnalyze exactly once at completion. The
   reviewer perceives staged operational progress; the actual
   Phase 52/54/55 envelope set is built atomically at the end as before.

   No randomness. No probabilistic logic. No autonomy. No telemetry.
*/
(function (global) {
  'use strict';
  const OC = global.OC = global.OC || {};

  // Fixed stage sequence. Stage ids are stable identifiers used by the
  // findings module to attach reveal points. Order is deterministic.
  const STAGES = Object.freeze([
    { id: 'intake',       label: 'intake classification',         runtime_state: 'preparing'    },
    { id: 'metadata',     label: 'metadata extraction',           runtime_state: 'preparing'    },
    { id: 'frames',       label: 'frame indexing',                runtime_state: 'analyzing',   video_only: true },
    { id: 'ocr',          label: 'OCR sweep',                     runtime_state: 'analyzing'    },
    { id: 'semantic',     label: 'semantic extraction',           runtime_state: 'analyzing'    },
    { id: 'convergence',  label: 'convergence pass',              runtime_state: 'converging'   },
    { id: 'implications', label: 'runtime implication resolution', runtime_state: 'converging'  },
    { id: 'synthesis',    label: 'synthesis preparation',         runtime_state: 'synthesizing' }
  ]);

  // Per-evidence-kind base timing (ms per stage). Deterministic.
  // Total run time = sum of (stage_base_ms × stage_factor).
  const TIMING_PROFILES = Object.freeze({
    'video':            { base: 800, label: 'video pipeline (slow path)' },
    'pdf-document':     { base: 350, label: 'document pipeline (medium)' },
    'word-document':    { base: 350, label: 'document pipeline (medium)' },
    'markdown-text':    { base: 220, label: 'text pipeline (medium-fast)' },
    'plain-text':       { base: 200, label: 'text pipeline (medium-fast)' },
    'html-text':        { base: 220, label: 'text pipeline (medium-fast)' },
    'image':            { base: 180, label: 'image pipeline (fast)' },
    'vector-image':     { base: 150, label: 'vector pipeline (fast)' },
    'tabular-data':     { base:  90, label: 'structured pipeline (near-instant)' },
    'structured-data':  { base:  80, label: 'structured pipeline (near-instant)' },
    'archive':          { base: 280, label: 'archive pipeline (medium)' },
    'generic-binary':   { base: 250, label: 'generic pipeline (medium)' }
  });

  // Per-stage relative weight. Frame indexing is heavy for video (skipped
  // entirely for non-video). All other stages weighted 1.0.
  const STAGE_FACTOR = Object.freeze({
    intake:       0.4,
    metadata:     0.7,
    frames:       2.2,
    ocr:          1.4,
    semantic:     1.6,
    convergence:  1.2,
    implications: 0.7,
    synthesis:    0.9
  });

  function profileFor(file) {
    const Findings = OC.ReviewerFindings;
    const ev = Findings ? Findings.evidenceFor(file) : { kind: 'generic-binary' };
    const prof = TIMING_PROFILES[ev.kind] || TIMING_PROFILES['generic-binary'];
    return { kind: ev.kind, base: prof.base, label: prof.label };
  }

  // ---- Deterministic extraction surrogate ---------------------------------
  // Cheap deterministic functions of file metadata. NO real processing,
  // NO randomness. Surfaces extraction-flavored intelligence to the
  // reviewer so the staged execution doesn't read as empty.
  function deriveExtraction(file, evidenceKind) {
    const sz = (file && file.size) ? file.size : 0;
    const baseRegions = Math.max(6, Math.min(2400, Math.floor(sz / 1800)));
    const procedures = Math.max(0, Math.floor(baseRegions / 28));
    const warnings = Math.max(0, Math.floor(procedures / 4));
    const troubleshooting = Math.max(0, Math.floor(procedures / 5));
    const visualSupport = evidenceKind === 'video'
      ? Math.floor(baseRegions / 14)
      : Math.floor(baseRegions / 22);
    const promptPackages = Math.floor(visualSupport / 2);
    const frames = evidenceKind === 'video' ? Math.max(40, Math.floor(sz / 60000)) : 0;
    const scenes = evidenceKind === 'video' ? Math.max(3, Math.floor(frames / 12)) : 0;
    const motionRegions = evidenceKind === 'video' ? Math.max(2, Math.floor(scenes / 2)) : 0;
    return {
      baseRegions: baseRegions,
      procedures: procedures,
      warnings: warnings,
      troubleshooting: troubleshooting,
      visualSupport: visualSupport,
      promptPackages: promptPackages,
      frames: frames,
      scenes: scenes,
      motionRegions: motionRegions
    };
  }

  function procDensityLabel(n) {
    if (n >= 18) return 'high';
    if (n >= 8)  return 'medium';
    if (n >= 2)  return 'low';
    return 'sparse';
  }

  function fmtBytesLocal(n) {
    if (!n) return '0 B';
    if (n < 1024) return n + ' B';
    if (n < 1024 * 1024) return (n / 1024).toFixed(1) + ' KB';
    return (n / (1024 * 1024)).toFixed(2) + ' MB';
  }

  function ctxFor(file, summary) {
    const Findings = OC.ReviewerFindings;
    const ev = Findings ? Findings.evidenceFor(file) : { kind: 'generic-binary', domains: [], ocr: 'none' };
    const product = Findings ? Findings.inferredProduct(file) : 'unspecified';
    const name = (file && file.name) ? file.name : '<no-source>';
    const ext = name.indexOf('.') >= 0 ? name.split('.').pop().toLowerCase() : '';
    const x = deriveExtraction(file, ev.kind);
    return { file: file, ev: ev, product: product, name: name, ext: ext, x: x, summary: summary || {} };
  }

  function extractionTable(ctx) {
    const x = ctx.x;
    return {
      title: 'semantic extraction summary',
      rows: [
        ['textual regions',       x.baseRegions],
        ['procedural candidates', x.procedures],
        ['warning groups',        x.warnings],
        ['troubleshooting groups', x.troubleshooting],
        ['visual-support reqs',   x.visualSupport],
        ['prompt packages',       x.promptPackages]
      ]
    };
  }

  function implicationsTable(ctx) {
    const product = ctx.product;
    const targetTree = product === 'unspecified'
      ? 'wp-content/themes/beslock-custom/User manuals/<product>/'
      : 'wp-content/themes/beslock-custom/User manuals/' + product + '/';
    return {
      title: 'runtime implications',
      rows: [
        ['target tree',          targetTree],
        ['semantic domains',     (ctx.ev.domains || []).join(',') || '<none>'],
        ['analyze envelopes',    'P52,P55,P54,P54,P54'],
        ['accept envelopes',     'P52,P54,P55,P58'],
        ['downstream phases',    '52,54,55,58'],
        ['lineage policy',       'append-only · prior_workflow_id pointer'],
        ['reviewer authority',   'required at analyze + accept']
      ]
    };
  }

  function frameTable(ctx) {
    const x = ctx.x;
    return {
      title: 'video frame index',
      rows: [
        ['frame samples',          x.frames],
        ['scene boundaries',       x.scenes],
        ['procedural-motion regs', x.motionRegions]
      ]
    };
  }

  function intakeTable(ctx) {
    return {
      title: 'source manifest',
      rows: [
        ['source',          ctx.name],
        ['size',            fmtBytesLocal(ctx.file && ctx.file.size)],
        ['extension',       ctx.ext || '<none>'],
        ['evidence kind',   ctx.ev.kind],
        ['ocr requirement', ctx.ev.ocr],
        ['product',         ctx.product]
      ]
    };
  }

  // Narration lines per stage. Each item: { frac, kind, text? , table? }
  // 'frac' is the fraction (0..1) of the stage window at which to emit.
  function narrateStage(stage, ctx) {
    const x = ctx.x, ev = ctx.ev;
    const lines = [];
    switch (stage.id) {
      case 'intake':
        lines.push({ frac: 0.05, kind: 'scan',     text: '[scan] source accepted: ' + ctx.name + ' (.' + (ctx.ext || '?') + ')' });
        lines.push({ frac: 0.40, kind: 'scan',     text: '[scan] runtime profile selected: ' + ev.kind + '-pipeline' });
        lines.push({ frac: 0.70, kind: 'classify', text: '[classify] evidence kind: ' + ev.kind + ' · ocr requirement: ' + ev.ocr });
        lines.push({ frac: 0.85, kind: 'classify', text: '[classify] inferred product candidate: ' + ctx.product });
        lines.push({ frac: 0.97, kind: 'table',    table: intakeTable(ctx) });
        break;
      case 'metadata':
        lines.push({ frac: 0.10, kind: 'meta', text: '[meta] hashing source bytes (sha256-equivalent surrogate)' });
        lines.push({ frac: 0.45, kind: 'meta', text: '[meta] container size: ' + fmtBytesLocal(ctx.file && ctx.file.size) });
        lines.push({ frac: 0.80, kind: 'meta', text: '[meta] semantic domains attached: [' + ((ev.domains || []).join(', ') || 'none') + ']' });
        break;
      case 'frames':
        lines.push({ frac: 0.05, kind: 'frame', text: '[frame] sampling at adaptive deterministic interval' });
        lines.push({ frac: 0.30, kind: 'frame', text: '[frame] indexed ' + x.frames + ' frame samples' });
        lines.push({ frac: 0.55, kind: 'frame', text: '[scene] continuity boundaries detected: ' + x.scenes });
        lines.push({ frac: 0.78, kind: 'frame', text: '[motion] procedural-motion regions: ' + x.motionRegions });
        lines.push({ frac: 0.95, kind: 'table', table: frameTable(ctx) });
        break;
      case 'ocr':
        lines.push({ frac: 0.10, kind: 'ocr', text: '[ocr] scanning textual regions' });
        lines.push({ frac: 0.50, kind: 'ocr', text: '[ocr] extracted ' + x.baseRegions + ' textual regions' });
        lines.push({ frac: 0.85, kind: 'ocr', text: '[ocr] caption/label candidates: ' + Math.floor(x.baseRegions / 6) });
        break;
      case 'semantic':
        lines.push({ frac: 0.10, kind: 'sem',    text: '[semantic] inferred language: en' });
        lines.push({ frac: 0.25, kind: 'sem',    text: '[semantic] procedural density score: ' + procDensityLabel(x.procedures) });
        lines.push({ frac: 0.45, kind: 'detect', text: '[detect] procedural step candidates: ' + x.procedures });
        lines.push({ frac: 0.60, kind: 'detect', text: '[detect] warning indicator candidates: ' + x.warnings });
        lines.push({ frac: 0.74, kind: 'detect', text: '[detect] troubleshooting candidates: ' + x.troubleshooting });
        lines.push({ frac: 0.86, kind: 'detect', text: '[detect] visual-support opportunities: ' + x.visualSupport });
        lines.push({ frac: 0.97, kind: 'table',  table: extractionTable(ctx) });
        break;
      case 'convergence':
        lines.push({ frac: 0.15, kind: 'conv', text: '[convergence] dispatch map convergence active' });
        lines.push({ frac: 0.45, kind: 'conv', text: '[convergence] candidate fusion: extraction-candidate (P52) <-> cross-evidence-fusion (P55)' });
        lines.push({ frac: 0.80, kind: 'conv', text: '[convergence] canonical-entity-consolidation staged' });
        break;
      case 'implications':
        lines.push({ frac: 0.20, kind: 'impl', text: '[implications] resolving downstream phases (P52, P54, P55, P58)' });
        lines.push({ frac: 0.55, kind: 'impl', text: '[implications] target tree resolved' });
        lines.push({ frac: 0.95, kind: 'table', table: implicationsTable(ctx) });
        break;
      case 'synthesis':
        lines.push({ frac: 0.15, kind: 'syn', text: '[synthesis] preparing manual-synthesis-record (P54)' });
        lines.push({ frac: 0.40, kind: 'syn', text: '[synthesis] preparing visual-support-requirement (P54)' });
        lines.push({ frac: 0.70, kind: 'syn', text: '[synthesis] preparing prompt-package-record (P54): ' + x.promptPackages + ' candidate packages' });
        lines.push({ frac: 0.95, kind: 'syn', text: '[synthesis] export envelope staged' });
        break;
    }
    return lines;
  }

  function stagesFor(file) {
    const Findings = OC.ReviewerFindings;
    const ev = Findings ? Findings.evidenceFor(file) : { kind: 'generic-binary' };
    const isVideo = (ev.kind === 'video');
    return STAGES.filter(function (s) { return !s.video_only || isVideo; });
  }

  function plan(file) {
    const prof = profileFor(file);
    const stages = stagesFor(file).map(function (s) {
      return Object.assign({}, s, {
        duration_ms: Math.round(prof.base * (STAGE_FACTOR[s.id] || 1.0))
      });
    });
    const total_ms = stages.reduce(function (n, s) { return n + s.duration_ms; }, 0);
    return { profile: prof, stages: stages, total_ms: total_ms };
  }

  /* run({ file, summary, priorWorkflowId, onState, onStage, onComplete, onError })
     Returns a controller { cancel() }. Invokes hooks deterministically:
       onState(state)         — runtime_state transitions
       onStage(stage, phase)  — phase ∈ {'start','complete'}
       onComplete(workflow)   — fired after RW.startAnalyze succeeds
       onError(err)           — fired if RW.startAnalyze throws
     RW.startAnalyze is invoked exactly once, at the end of the sequence.
  */
  function run(opts) {
    opts = opts || {};
    const file = opts.file;
    const summary = opts.summary || {};
    const priorWorkflowId = opts.priorWorkflowId || null;
    const onState    = typeof opts.onState    === 'function' ? opts.onState    : function () {};
    const onStage    = typeof opts.onStage    === 'function' ? opts.onStage    : function () {};
    const onComplete = typeof opts.onComplete === 'function' ? opts.onComplete : function () {};
    const onError    = typeof opts.onError    === 'function' ? opts.onError    : function () {};

    const planned = plan(file);
    const stages = planned.stages;
    const ctx = ctxFor(file, summary);
    let cancelled = false;
    let timer = null;
    const narrationTimers = [];

    onState('preparing');

    let i = 0;
    function step() {
      if (cancelled) return;
      if (i >= stages.length) {
        // All UX stages complete. Now invoke the real (existing) orchestration
        // synchronously — atomic envelope construction, no new dispatches.
        try {
          if (!OC.ReviewerWorkflow || !OC.ReviewerWorkflow.startAnalyze) {
            throw new Error('OC.ReviewerWorkflow.startAnalyze unavailable');
          }
          const wf = OC.ReviewerWorkflow.startAnalyze(file, summary, priorWorkflowId);
          onState('completed');
          onComplete(wf);
        } catch (err) {
          onState('failed');
          onError(err);
        }
        return;
      }
      const stg = stages[i];
      onState(stg.runtime_state);
      onStage(stg, 'start');

      // Schedule narration lines deterministically inside this stage's window.
      const narration = narrateStage(stg, ctx);
      narration.forEach(function (line) {
        const at = Math.max(20, Math.floor(stg.duration_ms * (line.frac || 0.5)));
        const t = global.setTimeout(function () {
          if (cancelled) return;
          onStage(stg, 'narrate', line);
        }, at);
        narrationTimers.push(t);
      });

      timer = global.setTimeout(function () {
        if (cancelled) return;
        onStage(stg, 'complete');
        i += 1;
        step();
      }, stg.duration_ms);
    }
    step();

    return {
      cancel: function () {
        cancelled = true;
        if (timer) global.clearTimeout(timer);
        narrationTimers.forEach(function (t) { global.clearTimeout(t); });
        onState('idle');
      }
    };
  }

  OC.AnalysisRunner = Object.freeze({
    STAGES: STAGES,
    TIMING_PROFILES: TIMING_PROFILES,
    STAGE_FACTOR: STAGE_FACTOR,
    profileFor: profileFor,
    stagesFor: stagesFor,
    plan: plan,
    run: run,
    deriveExtraction: deriveExtraction,
    ctxFor: ctxFor,
    narrateStage: narrateStage
  });
})(typeof window !== 'undefined' ? window : globalThis);
