import { readdirSync, readFileSync, statSync } from 'node:fs';
import path from 'node:path';
import { spawnSync } from 'node:child_process';

const rootDir = process.cwd();
const themeDir = path.join(rootDir, 'wp-content/themes/beslock-custom');
const requestedChecks = new Set(process.argv.slice(2));
const runAll = requestedChecks.size === 0;

const checks = {
  structure: runAll || requestedChecks.has('structure'),
  php: runAll || requestedChecks.has('php'),
  media: runAll || requestedChecks.has('media'),
  bem: runAll || requestedChecks.has('bem'),
};

const ignoredDirs = new Set(['.git', 'node_modules', 'test-results', 'playwright-report']);
const failures = [];
const warnings = [];

function walk(dir) {
  const entries = readdirSync(dir, { withFileTypes: true });
  const files = [];

  for (const entry of entries) {
    if (ignoredDirs.has(entry.name)) continue;

    const fullPath = path.join(dir, entry.name);

    if (entry.isDirectory()) {
      files.push(...walk(fullPath));
    } else if (entry.isFile()) {
      files.push(fullPath);
    }
  }

  return files;
}

function relative(file) {
  return path.relative(rootDir, file);
}

function formatBytes(bytes) {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / 1024 / 1024).toFixed(2)} MB`;
}

function hasSiblingWebp(file) {
  const parsed = path.parse(file);
  const sibling = path.join(parsed.dir, `${parsed.name}.webp`);

  try {
    return statSync(sibling).isFile();
  } catch {
    return false;
  }
}

function fileExists(file) {
  try {
    return statSync(file).isFile();
  } catch {
    return false;
  }
}

function pathExists(item) {
  try {
    statSync(item);
    return true;
  } catch {
    return false;
  }
}

function runStructureAudit() {
  const legacyThemePaths = [
    'docs',
    'scripts',
    'dist',
    'interactions',
    'repo_portfolio',
    'import_logs',
    'products.json',
    'worldcities.csv',
    'assets/images/Clips_hero',
    'assets/images/Hero_develp',
  ];

  const requiredThemePaths = [
    'assets/images/hero/clips',
    'assets/images/hero/overlays',
    'assets/manuals/index.json',
    'data/products.json',
    'data/worldcities.csv',
    'data/interactions/interactions.json',
    'data/portfolio/products.json',
    'tools/recovery/README.md',
    'tools/recovery/portfolio/CSV_portfolio_generator.php',
    'tools/recovery/portfolio/fix-placeholder-images.php',
    'tools/recovery/plugins/beslock-portfolio-exporter/beslock-portfolio-exporter.php',
  ];

  for (const legacyPath of legacyThemePaths) {
    const absolutePath = path.join(themeDir, legacyPath);
    if (pathExists(absolutePath)) {
      failures.push(`Legacy theme path should stay out of the theme root: ${relative(absolutePath)}`);
    }
  }

  for (const requiredPath of requiredThemePaths) {
    const absolutePath = path.join(themeDir, requiredPath);
    if (!pathExists(absolutePath)) {
      failures.push(`Required theme structure path is missing: ${relative(absolutePath)}`);
    }
  }

  console.log('Structure audit: theme folders checked');
}

function hasVideoFallback(file) {
  const parsed = path.parse(file);
  const siblingWebm = path.join(parsed.dir, `${parsed.name}.webm`);
  const poster = path.join(parsed.dir, 'posters', `${parsed.name}.webp`);

  return fileExists(siblingWebm) || fileExists(poster);
}

function runPhpLint(files) {
  const phpFiles = files.filter((file) => file.endsWith('.php'));

  for (const file of phpFiles) {
    const result = spawnSync('php', ['-l', file], { encoding: 'utf8' });

    if (result.error) {
      failures.push(`PHP is not available for linting: ${result.error.message}`);
      return;
    }

    if (result.status !== 0) {
      failures.push(`PHP lint failed: ${relative(file)}\n${result.stdout}${result.stderr}`.trim());
    }
  }

  console.log(`PHP lint: ${phpFiles.length} files checked`);
}

function runMediaAudit(files) {
  const publicResidue = files.filter((file) => {
    const name = path.basename(file);
    const ext = path.extname(file).toLowerCase();

    return name === '.DS_Store' || ext === '.psd' || ext === '.bak' || ext === '.log';
  });

  for (const file of publicResidue) {
    failures.push(`Remove public residue file: ${relative(file)}`);
  }

  for (const file of files) {
    const ext = path.extname(file).toLowerCase();
    const stats = statSync(file);

    if (['.png', '.jpg', '.jpeg'].includes(ext) && stats.size > 500 * 1024 && !hasSiblingWebp(file)) {
      warnings.push(`Large raster without same-folder WebP alternative: ${relative(file)} (${formatBytes(stats.size)})`);
    }

    if (ext === '.mp4' && stats.size > 3 * 1024 * 1024 && !hasVideoFallback(file)) {
      warnings.push(`Large MP4 without WebM or poster fallback: ${relative(file)} (${formatBytes(stats.size)})`);
    }
  }

  console.log('Media audit: public assets checked');
}

function extractClassTokensFromPhp(files) {
  const tokens = new Set();
  const classAttribute = /class\s*=\s*(["'])(.*?)\1/gs;

  for (const file of files.filter((item) => item.endsWith('.php'))) {
    const contents = readFileSync(file, 'utf8');
    let match;

    while ((match = classAttribute.exec(contents))) {
      if (match[2].includes('<')) {
        continue;
      }

      for (const token of match[2].split(/\s+/).filter(Boolean)) {
        if (!token.includes('$')) {
          tokens.add(token);
        }
      }
    }
  }

  return [...tokens].sort();
}

function runBemAudit(files) {
  const tokens = extractClassTokensFromPhp(files);
  const invalid = [];
  const legacyPrefixes = new Map();
  const bemLike = /^[a-z][a-z0-9]*(?:-[a-z0-9]+)*(?:__(?:[a-z0-9]+-?)+)?(?:--(?:[a-z0-9]+-?)+)?$/;
  const allowed = /^(is-|has-|js-|u-|wp-|wc-|woocommerce|screen-reader-text|button$|required$|optional$|input-text$|form-row|bi$|bi-|attachment-|size-|backorder_notification$|remove_from_cart_button$|shipping_method$|shop_table|state_select$)/;
  const legacy = /^(pc-|btn-|slide-|hero-slide$|hero-dot$|hero-dots$|home-)/;

  for (const token of tokens) {
    if (token.includes('%')) {
      continue;
    }

    if (!bemLike.test(token) && !allowed.test(token)) {
      invalid.push(token);
    }

    if (legacy.test(token)) {
      const prefix = token.split('-')[0];
      legacyPrefixes.set(prefix, (legacyPrefixes.get(prefix) || 0) + 1);
    }
  }

  if (invalid.length > 0) {
    warnings.push(`Non-standard class tokens in PHP templates: ${invalid.slice(0, 30).join(', ')}`);
  }

  if (legacyPrefixes.size > 0) {
    const summary = [...legacyPrefixes.entries()]
      .map(([prefix, count]) => `${prefix}: ${count}`)
      .join(', ');
    warnings.push(`Legacy class aliases still present for compatibility: ${summary}`);
  }

  console.log(`BEM audit: ${tokens.length} template class tokens scanned`);
}

const files = walk(themeDir);

if (checks.structure) runStructureAudit();
if (checks.php) runPhpLint(files);
if (checks.media) runMediaAudit(files);
if (checks.bem) runBemAudit(files);

for (const warning of warnings) {
  console.warn(`Warning: ${warning}`);
}

if (failures.length > 0) {
  for (const failure of failures) {
    console.error(`Error: ${failure}`);
  }

  process.exit(1);
}

console.log('Theme validation passed');
