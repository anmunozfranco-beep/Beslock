import { expect, test } from '@playwright/test';

const viewports = [
  { name: 'tablet-portrait-800x1280', width: 800, height: 1280 },
  { name: 'tablet-landscape-1280x800', width: 1280, height: 800 },
  { name: 'ipad-portrait-768x1024', width: 768, height: 1024 },
  { name: 'ipad-landscape-1024x768', width: 1024, height: 768 },
];

async function waitForHomepageStable(page) {
  await page.goto('/', { waitUntil: 'networkidle' });
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

async function getHeroMetrics(page) {
  return page.evaluate(() => {
    const content = document.querySelector('.hero-slide.is-active .slide-content');
    const overlay = document.querySelector('.hero-slide.is-active .slide-overlay-frame');

    if (!content || !overlay) {
      return null;
    }

    const rect = (element) => {
      const box = element.getBoundingClientRect();
      return {
        left: box.left,
        right: box.right,
        top: box.top,
        bottom: box.bottom,
        width: box.width,
        height: box.height,
      };
    };

    return {
      viewportWidth: window.innerWidth,
      scrollWidth: document.documentElement.scrollWidth,
      content: rect(content),
      overlay: rect(overlay),
    };
  });
}

async function getGridMetrics(page) {
  return page.evaluate(() => {
    const cards = Array.from(document.querySelectorAll('.products-portfolio__grid .product-card'))
      .map((card) => {
        const rect = card.getBoundingClientRect();
        return {
          left: rect.left,
          right: rect.right,
          top: rect.top,
          bottom: rect.bottom,
          width: rect.width,
          height: rect.height,
          opacity: Number.parseFloat(window.getComputedStyle(card).opacity || '0'),
        };
      })
      .filter((card) => card.opacity > 0.5);

    return {
      viewportWidth: window.innerWidth,
      cards,
    };
  });
}

test.describe('Homepage tablet layout', () => {
  for (const viewport of viewports) {
    test(`keeps hero and products bounded at ${viewport.name}`, async ({ page }) => {
      await page.setViewportSize({ width: viewport.width, height: viewport.height });
      await waitForHomepageStable(page);

      const firstSlide = await getHeroMetrics(page);
      expect(firstSlide).not.toBeNull();
      expect(firstSlide.scrollWidth).toBeLessThanOrEqual(viewport.width + 1);
      expect(firstSlide.content.left).toBeGreaterThanOrEqual(16);
      expect(firstSlide.overlay.right).toBeLessThanOrEqual(viewport.width + 1);
      expect(firstSlide.content.right).toBeLessThanOrEqual(firstSlide.overlay.left - 8);

      const secondDot = page.locator('.hero-dot').nth(1);
      await expect(secondDot).toBeVisible();
      await secondDot.click({ force: true });
      await page.waitForTimeout(900);

      const secondSlide = await getHeroMetrics(page);
      expect(secondSlide).not.toBeNull();
      expect(secondSlide.scrollWidth).toBeLessThanOrEqual(viewport.width + 1);
      expect(secondSlide.content.left).toBeGreaterThanOrEqual(16);
      expect(secondSlide.overlay.right).toBeLessThanOrEqual(viewport.width + 1);
      expect(secondSlide.content.right).toBeLessThanOrEqual(secondSlide.overlay.left - 8);

      await page.locator('#productos').scrollIntoViewIfNeeded();
      await page.waitForTimeout(800);

      const grid = await getGridMetrics(page);
      expect(grid.cards.length).toBeGreaterThan(0);

      for (const card of grid.cards.slice(0, Math.min(grid.cards.length, 4))) {
        expect(card.left).toBeGreaterThanOrEqual(20);
        expect(card.right).toBeLessThanOrEqual(viewport.width - 20);
      }
    });
  }
});
