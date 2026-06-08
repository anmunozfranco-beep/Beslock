import { expect, test } from '@playwright/test';

const cartProductSlug = process.env.PW_CART_PRODUCT_SLUG || 'e-prime';

async function getProductId(request, baseURL, slug) {
  const productsURL = new URL('/wp-json/wc/store/v1/products', baseURL);
  productsURL.searchParams.set('slug', slug);

  const response = await request.get(productsURL.toString());
  expect(response.ok()).toBeTruthy();

  const products = await response.json();
  expect(products.length, `Expected a published WooCommerce product with slug "${slug}".`).toBeGreaterThan(0);

  return products[0].id;
}

test.describe('Cart viewport', () => {
  test('keeps the footer below the initial cart viewport', async ({ page, request, baseURL }, testInfo) => {
    const productId = await getProductId(request, baseURL, cartProductSlug);

    await page.goto(`/?add-to-cart=${productId}`, { waitUntil: 'domcontentloaded' });
    await page.goto('/carrito/', { waitUntil: 'networkidle' });

    await expect(page.locator('.beslock-cart--checkout')).toBeVisible();
    await expect(page.locator('.site-footer')).toBeAttached();

    const metrics = await page.evaluate(() => {
      const rectFor = (selector) => {
        const element = document.querySelector(selector);
        if (!element) return null;
        const rect = element.getBoundingClientRect();
        return {
          top: rect.top,
          right: rect.right,
          bottom: rect.bottom,
          left: rect.left,
          width: rect.width,
          height: rect.height,
        };
      };

      const viewportHeight = window.innerHeight;
      const footer = rectFor('.site-footer');
      const cart = rectFor('.beslock-cart--checkout');
      const layout = rectFor('.beslock-cart__layout');

      return {
        viewportHeight,
        footer,
        cart,
        layout,
        footerVisiblePixels: footer
          ? Math.max(0, Math.min(viewportHeight, footer.bottom) - Math.max(0, footer.top))
          : null,
      };
    });

    await testInfo.attach('cart-viewport-metrics', {
      body: JSON.stringify(metrics, null, 2),
      contentType: 'application/json',
    });

    expect(metrics.footer).not.toBeNull();
    expect(metrics.cart).not.toBeNull();
    expect(metrics.layout).not.toBeNull();
    expect(metrics.footerVisiblePixels).toBeLessThanOrEqual(1);
    expect(metrics.footer.top).toBeGreaterThanOrEqual(metrics.viewportHeight - 1);
  });

  test('blocks checkout until the shipping address is confirmed', async ({ page, request, baseURL }) => {
    const productId = await getProductId(request, baseURL, cartProductSlug);

    await page.goto(`/?add-to-cart=${productId}`, { waitUntil: 'domcontentloaded' });
    await page.goto('/carrito/', { waitUntil: 'networkidle' });

    const blockedCheckout = page.locator('.beslock-cart__summary .beslock-checkout-button--disabled');
    await expect(blockedCheckout).toBeVisible();
    await expect(blockedCheckout).toHaveAttribute('aria-disabled', 'true');
    await expect(blockedCheckout).toContainText('Actualiza tu dirección');
    await expect(page.locator('.beslock-cart__summary .wc-proceed-to-checkout a.checkout-button')).toHaveCount(0);

    await page.goto('/finalizar-compra/', { waitUntil: 'domcontentloaded' });
    await expect(page).toHaveURL(/\/carrito\/?$/);
    await expect(page.locator('.woocommerce-error, .woocommerce-message, .woocommerce-info')).toContainText('Actualiza y confirma la dirección de envío');
  });
});
