import { chromium } from '@playwright/test';
import fs from 'node:fs/promises';
import path from 'node:path';

const baseURL = process.env.PW_BASE_URL || 'http://localhost:8080';
const label = process.env.PW_AUDIT_LABEL || 'audit';
const outputRoot = path.resolve('test-results/playwright', `homepage-tablet-${label}`);

const viewports = [
  { name: 'tablet-portrait-800x1280', width: 800, height: 1280 },
  { name: 'tablet-landscape-1280x800', width: 1280, height: 800 },
  { name: 'ipad-portrait-768x1024', width: 768, height: 1024 },
  { name: 'ipad-landscape-1024x768', width: 1024, height: 768 },
  { name: 'mobile-390x844', width: 390, height: 844 },
  { name: 'desktop-1600x900', width: 1600, height: 900 },
];

async function waitForHomepageStable(page) {
  await page.goto(baseURL, { waitUntil: 'networkidle' });
  await page.waitForTimeout(2200);

  await page.evaluate(() => {
    window.scrollTo({ top: 0, behavior: 'instant' });
  });

  const loader = page.locator('#beslockLoader');
  if (await loader.count()) {
    try {
      await loader.waitFor({ state: 'hidden', timeout: 8000 });
    } catch {}
  }

  const hero = page.locator('.beslock-hero');
  if (await hero.count()) {
    try {
      await page.waitForFunction(() => {
        const node = document.querySelector('.beslock-hero');
        return !node || node.classList.contains('ready') || node.dataset.startupState === 'ready';
      }, { timeout: 8000 });
    } catch {}
  }

  await page.waitForTimeout(500);

  await page.evaluate(() => {
    document.querySelectorAll('.section-reveal').forEach((node) => node.classList.add('is-active'));
    document.querySelectorAll('.product-card').forEach((node) => node.classList.add('is-motion-visible'));
  });

  await page.waitForTimeout(750);
}

async function collectMetrics(page, viewport) {
  return page.evaluate(({ width, height }) => {
    const selectors = [
      'body',
      '#main-content',
      '.beslock-hero',
      '.hero-viewport',
      '.hero-slide.is-active .slide-content',
      '.hero-slide.is-active .slide-overlay-frame',
      '.products-portfolio',
      '.products-portfolio__grid',
      '.header .header__bar',
      '.u-container',
    ];

    const rectFor = (selector) => {
      const element = document.querySelector(selector);
      if (!element) return null;
      const rect = element.getBoundingClientRect();
      return {
        selector,
        left: Number(rect.left.toFixed(2)),
        right: Number(rect.right.toFixed(2)),
        top: Number(rect.top.toFixed(2)),
        bottom: Number(rect.bottom.toFixed(2)),
        width: Number(rect.width.toFixed(2)),
        height: Number(rect.height.toFixed(2)),
      };
    };

    const overflowCandidates = Array.from(document.querySelectorAll('body *'))
      .map((element) => {
        if (element.closest('.manuals-drawer, .support-drawer, #mobileDrawer')) {
          return null;
        }

        const rect = element.getBoundingClientRect();
        const computed = window.getComputedStyle(element);
        const overflowRight = rect.right - window.innerWidth;
        const overflowLeft = 0 - rect.left;

        if (overflowRight <= 1 && overflowLeft <= 1) {
          return null;
        }

        if (computed.position === 'fixed' && rect.width >= window.innerWidth - 1) {
          return null;
        }

        return {
          tag: element.tagName.toLowerCase(),
          className: element.className || '',
          id: element.id || '',
          left: Number(rect.left.toFixed(2)),
          right: Number(rect.right.toFixed(2)),
          width: Number(rect.width.toFixed(2)),
          overflowRight: Number(overflowRight.toFixed(2)),
          overflowLeft: Number(overflowLeft.toFixed(2)),
        };
      })
      .filter(Boolean)
      .sort((a, b) => Math.max(b.overflowRight, b.overflowLeft) - Math.max(a.overflowRight, a.overflowLeft))
      .slice(0, 12);

    return {
      viewport: { width, height },
      windowInnerWidth: window.innerWidth,
      windowInnerHeight: window.innerHeight,
      documentScrollWidth: document.documentElement.scrollWidth,
      bodyScrollWidth: document.body.scrollWidth,
      hasHorizontalOverflow: document.documentElement.scrollWidth > window.innerWidth + 1,
      sections: selectors.map(rectFor).filter(Boolean),
      overflowCandidates,
    };
  }, viewport);
}

async function main() {
  await fs.mkdir(outputRoot, { recursive: true });

  const browser = await chromium.launch({ headless: true });

  try {
    const summary = [];

    for (const viewport of viewports) {
      const context = await browser.newContext({
        viewport: { width: viewport.width, height: viewport.height },
        deviceScaleFactor: 1,
      });
      const page = await context.newPage();

      await waitForHomepageStable(page);

      const metrics = await collectMetrics(page, viewport);
      const screenshotPath = path.join(outputRoot, `${viewport.name}.png`);
      const metricsPath = path.join(outputRoot, `${viewport.name}.json`);

      await page.screenshot({ path: screenshotPath, fullPage: true });
      await fs.writeFile(metricsPath, JSON.stringify(metrics, null, 2));

      summary.push({
        viewport: viewport.name,
        hasHorizontalOverflow: metrics.hasHorizontalOverflow,
        documentScrollWidth: metrics.documentScrollWidth,
        innerWidth: metrics.windowInnerWidth,
        overflowCandidates: metrics.overflowCandidates.length,
      });

      await context.close();
    }

    await fs.writeFile(path.join(outputRoot, 'summary.json'), JSON.stringify(summary, null, 2));
    console.log(JSON.stringify({ outputRoot, summary }, null, 2));
  } finally {
    await browser.close();
  }
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
