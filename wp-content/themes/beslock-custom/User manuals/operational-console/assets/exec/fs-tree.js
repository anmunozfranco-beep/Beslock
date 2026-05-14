/* OC.FSTree — Phase 61: Scoped Local Runtime Tree Authorization

   Reviewer-authorized scoped local filesystem persistence ONLY.

   Doctrinal invariants enforced here:
     • The browser may only write inside an explicitly reviewer-authorized
       directory handle obtained through window.showDirectoryPicker().
     • All operations are append-only: never overwrite, never delete,
       never mutate the original source file.
     • Deterministic product-folder resolution (no inference, no LLM).
     • Fail-closed when no authorized tree is present.
     • No telemetry, no background syncing, no autonomous behaviour.

   Public surface:
     OC.FSTree.authorize()         -> Promise<boolean>
     OC.FSTree.restore()           -> Promise<boolean>
     OC.FSTree.release()           -> Promise<void>
     OC.FSTree.isAuthorized()      -> boolean
     OC.FSTree.rootName()          -> string|null
     OC.FSTree.isSupported()       -> boolean
     OC.FSTree.commitAccept(opts)  -> Promise<{written:[{path,bytes}]}>
        opts = { workflow, fileBlob, product, onLog(text) }
*/
(function (global) {
  'use strict';
  global.OC = global.OC || {};

  // ---- IndexedDB persistence of FileSystemDirectoryHandle ----------------
  const IDB_NAME = 'oc-fs-tree';
  const IDB_STORE = 'handles';
  const IDB_KEY = 'runtime-root';

  function idbOpen() {
    return new Promise(function (resolve, reject) {
      if (!global.indexedDB) return reject(new Error('IndexedDB unavailable'));
      const req = global.indexedDB.open(IDB_NAME, 1);
      req.onupgradeneeded = function () { req.result.createObjectStore(IDB_STORE); };
      req.onsuccess = function () { resolve(req.result); };
      req.onerror = function () { reject(req.error); };
    });
  }
  function idbPut(value) {
    return idbOpen().then(function (db) {
      return new Promise(function (resolve, reject) {
        const tx = db.transaction(IDB_STORE, 'readwrite');
        tx.objectStore(IDB_STORE).put(value, IDB_KEY);
        tx.oncomplete = function () { resolve(); };
        tx.onerror = function () { reject(tx.error); };
      });
    });
  }
  function idbGet() {
    return idbOpen().then(function (db) {
      return new Promise(function (resolve, reject) {
        const tx = db.transaction(IDB_STORE, 'readonly');
        const req = tx.objectStore(IDB_STORE).get(IDB_KEY);
        req.onsuccess = function () { resolve(req.result || null); };
        req.onerror = function () { reject(req.error); };
      });
    });
  }
  function idbDelete() {
    return idbOpen().then(function (db) {
      return new Promise(function (resolve, reject) {
        const tx = db.transaction(IDB_STORE, 'readwrite');
        tx.objectStore(IDB_STORE).delete(IDB_KEY);
        tx.oncomplete = function () { resolve(); };
        tx.onerror = function () { reject(tx.error); };
      });
    });
  }

  // ---- Module state -------------------------------------------------------
  let rootHandle = null; // FileSystemDirectoryHandle | null

  function isSupported() {
    return typeof global.showDirectoryPicker === 'function';
  }
  function isAuthorized() { return !!rootHandle; }
  function rootName() { return rootHandle ? rootHandle.name : null; }

  function ensureRWPermission(handle) {
    if (!handle.queryPermission) return Promise.resolve(true);
    return handle.queryPermission({ mode: 'readwrite' }).then(function (state) {
      if (state === 'granted') return true;
      return handle.requestPermission({ mode: 'readwrite' }).then(function (s) {
        return s === 'granted';
      });
    });
  }

  function authorize() {
    if (!isSupported()) {
      return Promise.reject(new Error('File System Access API unavailable in this browser'));
    }
    return global.showDirectoryPicker({ mode: 'readwrite' }).then(function (handle) {
      return ensureRWPermission(handle).then(function (ok) {
        if (!ok) throw new Error('readwrite permission denied');
        rootHandle = handle;
        return idbPut(handle).then(function () { return true; }).catch(function () {
          // Persistence failure is non-fatal; in-memory authorization remains valid.
          return true;
        });
      });
    });
  }

  function restore() {
    if (!isSupported()) return Promise.resolve(false);
    return idbGet().then(function (handle) {
      if (!handle) return false;
      return ensureRWPermission(handle).then(function (ok) {
        if (!ok) return false;
        rootHandle = handle;
        return true;
      }).catch(function () { return false; });
    }).catch(function () { return false; });
  }

  function release() {
    rootHandle = null;
    return idbDelete().catch(function () { /* tolerate */ });
  }

  // ---- Path helpers (deterministic, no inference) ------------------------
  function safeSegment(s) {
    return String(s || '').replace(/[^A-Za-z0-9._-]+/g, '_').replace(/^_+|_+$/g, '') || '_';
  }
  function tsCompact() {
    // 2026-05-15T12-34-56-789Z — filesystem-safe timestamp.
    return new Date().toISOString().replace(/[:.]/g, '-');
  }
  function tsIso() { return new Date().toISOString(); }

  function getDir(parent, name) {
    return parent.getDirectoryHandle(safeSegment(name), { create: true });
  }
  function ensurePath(root, segs) {
    return segs.reduce(function (p, s) {
      return p.then(function (dir) { return getDir(dir, s); });
    }, Promise.resolve(root));
  }

  // Append-only file create. If the target name already exists the writer
  // is appended-suffixed (__1, __2, …) so prior content is never overwritten.
  function createNewFile(dir, baseName) {
    const name = safeSegment(baseName);
    return dir.getFileHandle(name, { create: false })
      .then(function () {
        // Name collision → append numeric suffix.
        const dot = name.lastIndexOf('.');
        const stem = dot > 0 ? name.slice(0, dot) : name;
        const ext = dot > 0 ? name.slice(dot) : '';
        function tryNext(i) {
          const candidate = stem + '__' + i + ext;
          return dir.getFileHandle(candidate, { create: false })
            .then(function () { return tryNext(i + 1); })
            .catch(function () { return dir.getFileHandle(candidate, { create: true }); });
        }
        return tryNext(1);
      })
      .catch(function () {
        // Target does not exist — safe to create.
        return dir.getFileHandle(name, { create: true });
      });
  }

  function writeFile(dir, baseName, blobOrText) {
    return createNewFile(dir, baseName).then(function (fh) {
      return fh.createWritable().then(function (w) {
        return w.write(blobOrText).then(function () { return w.close(); }).then(function () {
          return { name: fh.name, bytes: blobOrText.size != null ? blobOrText.size :
            (typeof blobOrText === 'string' ? new Blob([blobOrText]).size : 0) };
        });
      });
    });
  }

  // ---- Accept commit -----------------------------------------------------
  // workflow: full reviewer-workflow object (already accept()-ed by RW)
  // fileBlob: the original File object (NEVER mutated, only read for copy)
  // product:  deterministic product slug (e.g. 'e-nova') from findings.inferredProduct
  // onLog:    function(text) → terminal narration sink
  function commitAccept(opts) {
    if (!isAuthorized()) {
      return Promise.reject(new Error('runtime tree not authorized'));
    }
    const wf = opts.workflow;
    const fileBlob = opts.fileBlob;
    const product = safeSegment(opts.product || 'unspecified');
    const onLog = typeof opts.onLog === 'function' ? opts.onLog : function () {};
    const wfid = safeSegment(wf.workflow_id);
    const wfidShort = wfid.slice(0, 18);
    const ts = tsCompact();
    const written = [];

    onLog('[fs] resolving product runtime folder: ' + product + '/');

    return ensurePath(rootHandle, [product, 'source-of-truth', 'manuals'])
      .then(function (manualsDir) {
        onLog('[fs] ensured ' + product + '/source-of-truth/manuals/');
        if (!fileBlob) {
          onLog('[fs] !! no source blob retained — skipping evidence copy');
          return null;
        }
        const safeName = safeSegment(fileBlob.name || (wf.file && wf.file.name) || 'evidence');
        const targetName = wfid + '__' + safeName;
        onLog('[fs] copying source evidence → manuals/' + targetName + ' (' + fileBlob.size + ' B)');
        return writeFile(manualsDir, targetName, fileBlob).then(function (rec) {
          written.push({ path: product + '/source-of-truth/manuals/' + rec.name, bytes: rec.bytes });
          onLog('[fs]   wrote ' + rec.bytes + ' B (append-only; original untouched)');
        });
      })
      .then(function () {
        onLog('[fs] creating lineage directory');
        return ensurePath(rootHandle, [product, 'lineage']);
      })
      .then(function (lineageDir) {
        const lineageRecord = {
          schema: 'reviewer-workflow-lineage/1.0',
          workflow_id: wf.workflow_id,
          prior_workflow_id: wf.prior_workflow_id || null,
          reviewer: wf.reviewer || null,
          status: wf.status,
          product: product,
          source_file: wf.file || null,
          proposed_at_iso: wf.proposed_at_iso || null,
          accepted_at_iso: wf.accepted_at_iso || tsIso(),
          committed_at_iso: tsIso(),
          append_only: true
        };
        const name = ts + '__' + wfidShort + '.json';
        onLog('[fs] writing lineage record → lineage/' + name);
        return writeFile(lineageDir, name, JSON.stringify(lineageRecord, null, 2))
          .then(function (rec) {
            written.push({ path: product + '/lineage/' + rec.name, bytes: rec.bytes });
          });
      })
      .then(function () {
        return ensurePath(rootHandle, [product, 'runtime', 'envelopes']);
      })
      .then(function (envDir) {
        const envs = [].concat(
          wf.workflow_envelope ? [wf.workflow_envelope] : [],
          wf.analyze_envelopes || [],
          wf.accept_envelopes || []
        );
        onLog('[fs] writing export envelopes (' + envs.length + ') → runtime/envelopes/');
        return envs.reduce(function (p, env, idx) {
          return p.then(function () {
            const kind = safeSegment((env && env.kind) || 'envelope');
            const name = ts + '__' + wfidShort + '__' + String(idx).padStart(2, '0') + '__' + kind + '.json';
            return writeFile(envDir, name, JSON.stringify(env, null, 2)).then(function (rec) {
              written.push({ path: product + '/runtime/envelopes/' + rec.name, bytes: rec.bytes });
            });
          });
        }, Promise.resolve());
      })
      .then(function () {
        return ensurePath(rootHandle, [product, 'manifests']);
      })
      .then(function (manDir) {
        const manifest = {
          schema: 'reviewer-workflow-manifest/1.0',
          workflow_id: wf.workflow_id,
          prior_workflow_id: wf.prior_workflow_id || null,
          reviewer: wf.reviewer || null,
          product: product,
          status: wf.status,
          summary: wf.summary || {},
          reviewer_conclusion: wf.reviewer_conclusion || null,
          source_file: wf.file || null,
          envelope_count: (wf.analyze_envelopes || []).length + (wf.accept_envelopes || []).length
            + (wf.workflow_envelope ? 1 : 0),
          written_paths: written.map(function (w) { return w.path; }),
          authorized_root: rootName(),
          committed_at_iso: tsIso(),
          append_only: true
        };
        const name = ts + '__' + wfidShort + '__manifest.json';
        onLog('[fs] writing manifest → manifests/' + name);
        return writeFile(manDir, name, JSON.stringify(manifest, null, 2)).then(function (rec) {
          written.push({ path: product + '/manifests/' + rec.name, bytes: rec.bytes });
        });
      })
      .then(function () {
        const total = written.reduce(function (a, w) { return a + (w.bytes || 0); }, 0);
        onLog('[fs] append-only commit complete (' + written.length + ' files, ' + total + ' B)');
        return { written: written };
      });
  }

  global.OC.FSTree = Object.freeze({
    authorize: authorize,
    restore: restore,
    release: release,
    isAuthorized: isAuthorized,
    rootName: rootName,
    isSupported: isSupported,
    commitAccept: commitAccept
  });
}(typeof window !== 'undefined' ? window : globalThis));
