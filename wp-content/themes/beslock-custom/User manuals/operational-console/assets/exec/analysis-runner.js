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
    let cancelled = false;
    let timer = null;

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
    run: run
  });
})(typeof window !== 'undefined' ? window : globalThis);
