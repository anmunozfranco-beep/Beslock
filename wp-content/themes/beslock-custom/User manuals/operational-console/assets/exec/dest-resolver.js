// dest-resolver.js — deterministic destination proposal. Consumes the
// destination-resolution-rules.json table; never auto-commits.
(function () {
  if (!window.OC) window.OC = {};

  let _rules = null;

  async function ensureRules() {
    if (_rules) return _rules;
    _rules = await window.OC.FSBridge.loadRules('destination-resolution-rules');
    return _rules;
  }

  function _matches(rule, ctx) {
    const m = rule.match || {};
    for (const k of Object.keys(m)) {
      if (m[k] === '*') continue;
      if (ctx[k] !== m[k]) return false;
    }
    return true;
  }

  function _render(template, ctx) {
    return template
      .replace('{product}', ctx.product || '_unknown')
      .replace('{domain}', ctx.domain || '_unknown');
  }

  async function resolve(ctx) {
    const rules = await ensureRules();
    if (!rules || !rules.rules) {
      return { destination: null, rule_id: null, reasoning_chain: ['no rules loaded'] };
    }
    const reasoning = [];
    for (const rule of rules.rules) {
      if (_matches(rule, ctx)) {
        reasoning.push('matched ' + rule.id + ': ' + rule.reasoning);
        const dest = _render(rule.destination_template, ctx);
        const trustOk = !rule.trust_tier_required ||
                         (ctx.trust_tier === rule.trust_tier_required) ||
                         (ctx.trust_tier === 'tier-3-reviewer-attested');
        if (!trustOk) {
          reasoning.push('trust-tier mismatch: required ' + rule.trust_tier_required +
                         ', request carries ' + ctx.trust_tier + '. Falling back to staging.');
          continue;
        }
        return {
          destination: dest,
          rule_id: rule.id,
          trust_tier_required: rule.trust_tier_required,
          reasoning_chain: reasoning,
        };
      }
    }
    reasoning.push('no rule matched — fallback to staging/review-pending/_uncategorised/');
    return {
      destination: 'operational-console/staging/review-pending/_uncategorised/',
      rule_id: 'R-DEST-FALLBACK',
      trust_tier_required: 'tier-0-unvalidated',
      reasoning_chain: reasoning,
    };
  }

  function isForbidden(dest, rules) {
    if (!rules || !rules.forbidden_destinations) return false;
    for (const f of rules.forbidden_destinations) {
      if (dest && dest.indexOf(f) === 0) return true;
    }
    return false;
  }

  window.OC.DestResolver = { ensureRules: ensureRules, resolve: resolve, isForbidden: isForbidden };
})();
