import assert from 'node:assert/strict';
import { chromium } from '@playwright/test';

const baseURL = process.env.PW_BASE_URL || 'http://localhost:8080';
const viewport = { width: 815, height: 885 };
const targetSlideIndex = 3; // e-Shield
const targetGuideLeftRatio = 0.6965;
const ratioTolerance = 0.003;
const bleedTolerancePx = 0.35;

async function waitForHomepageStable(page) {
  await page.goto(baseURL, { waitUntil: 'networkidle' });
  await page.waitForTimeout(2200);

  const loader = page.locator('#beslockLoader');
  if (await loader.count()) {
    try {
      await loader.waitFor({ state: 'hidden', timeout: 8000 });
    } catch {}
  }

  await page.evaluate(() => {
    window.scrollTo({ top: 0, behavior: 'instant' });
    document.querySelectorAll('.section-reveal').forEach((node) => node.classList.add('is-active'));
    document.querySelectorAll('.product-card').forEach((node) => node.classList.add('is-motion-visible'));
  });

  await page.waitForTimeout(900);
}

async function main() {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport });

  try {
    await waitForHomepageStable(page);

    await page.locator('.hero-dot').nth(targetSlideIndex).click({ force: true });
    await page.waitForTimeout(1200);

    const metrics = await page.evaluate(() => {
      const hero = document.querySelector('.beslock-hero');
      const inner = document.querySelector('.hero-slide.is-active .slide-inner');
      const frame = document.querySelector('.hero-slide.is-active .slide-overlay-frame');

      if (!hero || !inner || !frame) {
        return null;
      }

      const heroRect = hero.getBoundingClientRect();
      const innerRect = inner.getBoundingClientRect();
      const frameRect = frame.getBoundingClientRect();
      const pseudo = getComputedStyle(inner, '::after');
      const pseudoLeft = Number.parseFloat(pseudo.left || '0');
      const pseudoRight = Number.parseFloat(pseudo.right || '0');

      return {
        viewportWidth: window.innerWidth,
        heroWidth: heroRect.width,
        pseudoLeft,
        pseudoRight,
        guideLeftRatio: pseudoLeft / heroRect.width,
        expectedBleedPx: window.innerWidth * 0.005,
        actualBleedPx: Math.abs(pseudoRight),
        frameLeftDelta: Math.abs(frameRect.left - (innerRect.left + pseudoLeft)),
        frameRightDelta: Math.abs(frameRect.right - (innerRect.right + Math.abs(pseudoRight))),
      };
    });

    assert(metrics, 'No se pudieron medir hero, slide-inner o overlay-frame.');

    assert(
      Math.abs(metrics.guideLeftRatio - targetGuideLeftRatio) <= ratioTolerance,
      `Guide left ratio fuera de tolerancia. Esperado ~${targetGuideLeftRatio}, recibido ${metrics.guideLeftRatio}.`,
    );

    assert(
      Math.abs(metrics.actualBleedPx - metrics.expectedBleedPx) <= bleedTolerancePx,
      `Guide bleed fuera de tolerancia. Esperado ~${metrics.expectedBleedPx}px, recibido ${metrics.actualBleedPx}px.`,
    );

    assert(
      metrics.frameLeftDelta <= 1.5,
      `Overlay frame left no coincide con la guía. Delta ${metrics.frameLeftDelta}px.`,
    );

    assert(
      metrics.frameRightDelta <= 1.5,
      `Overlay frame right no coincide con la guía. Delta ${metrics.frameRightDelta}px.`,
    );

    await page.locator('#beslockHero').screenshot({
      path: 'test-results/manual/hero-guide-audit-815x885-slide-4.png',
    });

    console.log(JSON.stringify(metrics, null, 2));
  } finally {
    await browser.close();
  }
}

await main();
