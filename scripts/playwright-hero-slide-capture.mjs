import { chromium } from '@playwright/test';
import fs from 'node:fs/promises';
import path from 'node:path';

const baseURL = process.env.PW_BASE_URL || 'http://localhost:8080';
const viewportWidth = Number.parseInt(process.env.PW_VIEWPORT_WIDTH || '815', 10);
const viewportHeight = Number.parseInt(process.env.PW_VIEWPORT_HEIGHT || '885', 10);
const slideIndex = Number.parseInt(process.env.PW_SLIDE_INDEX || '2', 10);
const overlayIndex = Number.parseInt(process.env.PW_OVERLAY_INDEX || '0', 10);
const extraWaitMs = Number.parseInt(process.env.PW_EXTRA_WAIT_MS || '0', 10);
const label = process.env.PW_CAPTURE_LABEL || `slide-${slideIndex + 1}-${viewportWidth}x${viewportHeight}`;
const injectedCSS = process.env.PW_INJECT_CSS || '';
const outputDir = path.resolve('test-results/manual');
const screenshotPath = path.join(outputDir, `${label}.png`);
const metricsPath = path.join(outputDir, `${label}.json`);

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
  await fs.mkdir(outputDir, { recursive: true });

  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({
    viewport: { width: viewportWidth, height: viewportHeight },
    deviceScaleFactor: 1,
  });

  try {
    await waitForHomepageStable(page);

    const targetDot = page.locator('.hero-dot').nth(slideIndex);
    await targetDot.click({ force: true });
    await page.waitForTimeout(1200);

    if (extraWaitMs > 0) {
      await page.waitForTimeout(extraWaitMs);
    }

    if (injectedCSS) {
      await page.addStyleTag({ content: injectedCSS });
      await page.waitForTimeout(250);
    }

    const metrics = await page.evaluate(({ slideIndex: currentSlideIndex, overlayIndex: currentOverlayIndex }) => {
      const activeSlide = document.querySelector(`.hero-slides > .hero-slide[data-index="${currentSlideIndex}"]`);
      const overlays = activeSlide ? Array.from(activeSlide.querySelectorAll('.slide-overlay')) : [];
      const overlayFrames = activeSlide ? Array.from(activeSlide.querySelectorAll('.slide-overlay-frame')) : [];
      const overlay = overlays[currentOverlayIndex] ?? null;
      const overlayFrame = overlayFrames[currentOverlayIndex] ?? overlayFrames[0] ?? null;
      const content = activeSlide?.querySelector('.slide-content');
      const inner = activeSlide?.querySelector('.slide-inner');

      const rect = (element) => {
        if (!element) return null;
        const box = element.getBoundingClientRect();
        return {
          left: Number(box.left.toFixed(2)),
          right: Number(box.right.toFixed(2)),
          top: Number(box.top.toFixed(2)),
          bottom: Number(box.bottom.toFixed(2)),
          width: Number(box.width.toFixed(2)),
          height: Number(box.height.toFixed(2)),
        };
      };

      const stylesFor = (element) => {
        if (!element) return null;
        const styles = window.getComputedStyle(element);
        return {
          transform: styles.transform,
          transformOrigin: styles.transformOrigin,
          objectPosition: styles.objectPosition,
          opacity: styles.opacity,
          top: styles.top,
          left: styles.left,
          width: styles.width,
          height: styles.height,
        };
      };

      return {
        slideIndex: currentSlideIndex,
        activeSlideIndex: activeSlide?.getAttribute('data-index') ?? null,
        overlayIndex: currentOverlayIndex,
        viewport: { width: window.innerWidth, height: window.innerHeight },
        inner: rect(inner),
        overlayFrame: rect(overlayFrame),
        overlay: rect(overlay),
        content: rect(content),
        overlayStyles: stylesFor(overlay),
        overlayCustomProperties: overlay ? {
          focusScaleBase: window.getComputedStyle(overlay).getPropertyValue('--overlay-focus-scale-base').trim(),
          focusScaleActive: window.getComputedStyle(overlay).getPropertyValue('--overlay-focus-scale-active').trim(),
          overlayOffset: window.getComputedStyle(overlay).getPropertyValue('--overlay-offset').trim(),
          dataStart: overlay.getAttribute('data-start'),
          isVisible: overlay.classList.contains('overlay--visible'),
        } : null,
      };
    }, { slideIndex, overlayIndex });

    await page.locator('#beslockHero').screenshot({ path: screenshotPath });
    await fs.writeFile(metricsPath, JSON.stringify(metrics, null, 2));

    console.log(JSON.stringify({ screenshotPath, metricsPath, metrics }, null, 2));
  } finally {
    await browser.close();
  }
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
