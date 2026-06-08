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

async function expectParticleFeedback(page) {
  const flight = page.locator('.beslock-cart-flight');
  const headerCart = page.locator('[data-js="header-cart"]');
  const headerCount = page.locator('[data-js="header-cart"] .header__cart-count');

  await expect(flight).toBeVisible({ timeout: 5000 });
  await expect(page.locator('.beslock-cart-toast')).toHaveCount(0);
  await expect(page.locator('.is-cart-added')).toBeVisible({ timeout: 5000 });
  await expect(headerCart).toHaveClass(/is-cart-receiving/, { timeout: 5000 });
  await expect(headerCount).toHaveText('1', { timeout: 7000 });
  await expect(flight).toHaveCount(0, { timeout: 5000 });
}

test.describe('Add to cart feedback', () => {
  test('animates a particle from a product card cart icon to the header cart', async ({ page, request, baseURL }) => {
    const productId = await getProductId(request, baseURL, cartProductSlug);

    await page.goto('/', { waitUntil: 'networkidle' });

    const addButton = page.locator(`[data-js="product-card"][data-product-id="${productId}"] [data-js="product-card-add-to-cart"]`);
    await expect(addButton).toBeVisible();
    await addButton.click();

    await expectParticleFeedback(page);
  });

  test('uses the same particle feedback on the single product add-to-cart button', async ({ page }) => {
    await page.goto(`/producto/${cartProductSlug}/`, { waitUntil: 'networkidle' });

    const addButton = page.locator('form.cart .single_add_to_cart_button');
    await expect(addButton).toBeVisible();
    await expect(addButton).toContainText('Agregar al carrito');
    await addButton.click();

    await expectParticleFeedback(page);
  });

  test('buzzes the header cart while it has products', async ({ page }) => {
    await page.addInitScript(() => {
      window.BESLOCK_CART_BUZZ_DELAY = 1600;
    });

    await page.goto(`/producto/${cartProductSlug}/`, { waitUntil: 'networkidle' });

    const addButton = page.locator('form.cart .single_add_to_cart_button');
    const headerCart = page.locator('[data-js="header-cart"]');

    await expect(addButton).toBeVisible();
    await addButton.click();

    await expect(page.locator('[data-js="header-cart"] .header__cart-count')).toHaveText('1', { timeout: 7000 });
    await expect(headerCart).toHaveClass(/is-cart-buzzing/, { timeout: 5000 });
    await expect(headerCart).not.toHaveClass(/is-cart-buzzing/, { timeout: 2000 });
  });
});
