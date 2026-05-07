<?php
// /wp-content/themes/beslock-custom/footer.php
// Footer minimal con logo blanco centrado.
// Incluye aqu��� los elementos que removimos del header: el script de sticky header,
// la sincronizaci���n de la variable CSS del logo (para que el footer calcule 40%),
// y la llamada a wp_footer() seguida de los cierres </body></html>.
?>
<footer class="site-footer">
  <div class="u-container" style="padding:2rem 0; text-align:center;">
    <img
      class="footer-logo"
      src="<?php echo esc_url( get_stylesheet_directory_uri() . '/assets/images/logo-white.png' ); ?>"
      alt="<?php echo esc_attr_x( 'Beslock logo blanco', 'alt text', 'beslock' ); ?>"
      loading="lazy"
    />
  </div>
</footer>

<?php wp_footer(); ?>

<!-- product-gallery-reel fetch+eval fallback DISABLED (was causing load issues). -->
<script>console && console.info && console.info('product-gallery-reel: fetch fallback disabled');</script>

</body>
</html>
