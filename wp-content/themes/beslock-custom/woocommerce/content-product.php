<?php

declare(strict_types=1);

if (! defined('ABSPATH') || empty($product) || ! $product->is_visible()) {
    return;
}
?>
<li <?php wc_product_class('beslock-product-card', $product); ?> data-beslock-product-card>
    <a class="beslock-product-card__link" href="<?php the_permalink(); ?>">
        <?php do_action('woocommerce_before_shop_loop_item_title'); ?>
        <h2 class="beslock-product-card__title"><?php the_title(); ?></h2>
        <p class="beslock-product-card__meta"><?php echo wp_kses_post($product->get_price_html()); ?></p>
    </a>
</li>
