<?php
/*
Plugin Name: Beslock Interactions Exporter
Description: Exporta las interacciones de productos a interactions.json usando comments y comment meta bajo el schema de Stage 1.
Version: 1.0.0
Author: Beslock
*/

if ( ! defined( 'ABSPATH' ) ) {
  exit;
}

if ( ! defined( 'BESLOCK_INTERACTIONS_EXPORTER_VERSION' ) ) {
  define( 'BESLOCK_INTERACTIONS_EXPORTER_VERSION', '1.0.0' );
}

add_action( 'admin_menu', 'beslock_interactions_exporter_register_menu' );

function beslock_interactions_exporter_register_menu() {
  add_management_page(
    __( 'Beslock Interactions Export', 'beslock' ),
    __( 'Interactions Export', 'beslock' ),
    'manage_options',
    'beslock-interactions-export',
    'beslock_interactions_exporter_render_page'
  );
}

function beslock_interactions_exporter_render_page() {
  if ( ! current_user_can( 'manage_options' ) ) {
    wp_die( esc_html__( 'Acceso denegado.', 'beslock' ) );
  }

  $result = null;
  $error_message = '';

  if ( isset( $_POST['beslock_interactions_export_submit'] ) ) {
    check_admin_referer( 'beslock_interactions_export_action', 'beslock_interactions_export_nonce' );

    $result = beslock_interactions_exporter_run_export();
    if ( is_wp_error( $result ) ) {
      $error_message = $result->get_error_message();
      $result = null;
    }
  }

  $snapshot_path = beslock_interactions_exporter_get_snapshot_path();
  ?>
  <div class="wrap">
    <h1><?php echo esc_html__( 'Beslock Interactions Export', 'beslock' ); ?></h1>

    <?php if ( '' !== $error_message ) : ?>
      <div class="notice notice-error"><p><?php echo esc_html( $error_message ); ?></p></div>
    <?php endif; ?>

    <?php if ( is_array( $result ) ) : ?>
      <div class="notice notice-success">
        <p><?php echo esc_html__( 'Exportación completada.', 'beslock' ); ?></p>
      </div>
      <p><?php echo esc_html( sprintf( __( 'Interacciones exportadas: %d', 'beslock' ), intval( $result['count'] ) ) ); ?></p>
      <p><?php echo esc_html( sprintf( __( 'Archivo generado: %s', 'beslock' ), $result['path'] ) ); ?></p>
      <ul>
        <li><?php echo esc_html( sprintf( __( 'Reviews: %d', 'beslock' ), intval( $result['types']['review'] ?? 0 ) ) ); ?></li>
        <li><?php echo esc_html( sprintf( __( 'Questions: %d', 'beslock' ), intval( $result['types']['question'] ?? 0 ) ) ); ?></li>
        <li><?php echo esc_html( sprintf( __( 'Replies: %d', 'beslock' ), intval( $result['types']['reply'] ?? 0 ) ) ); ?></li>
      </ul>
      <?php if ( ! empty( $result['skipped'] ) ) : ?>
        <p><?php echo esc_html( sprintf( __( 'Interacciones omitidas: %d', 'beslock' ), count( $result['skipped'] ) ) ); ?></p>
      <?php endif; ?>
    <?php endif; ?>

    <p><?php echo esc_html__( 'Genera el snapshot Stage 1 en la carpeta interactions del tema activo.', 'beslock' ); ?></p>
    <p><code><?php echo esc_html( $snapshot_path ); ?></code></p>

    <form method="post">
      <?php wp_nonce_field( 'beslock_interactions_export_action', 'beslock_interactions_export_nonce' ); ?>
      <p>
        <button type="submit" name="beslock_interactions_export_submit" class="button button-primary">
          <?php echo esc_html__( 'Exportar interactions.json', 'beslock' ); ?>
        </button>
      </p>
    </form>
  </div>
  <?php
}

function beslock_interactions_exporter_run_export() {
  $snapshot_path = beslock_interactions_exporter_get_snapshot_path();
  $snapshot_dir = dirname( $snapshot_path );

  if ( ! wp_mkdir_p( $snapshot_dir ) ) {
    return new WP_Error( 'beslock_interactions_exporter_directory', __( 'No se pudo crear la carpeta interactions.', 'beslock' ) );
  }

  $comments = get_comments(
    array(
      'status'  => 'all',
      'orderby' => 'comment_date_gmt',
      'order'   => 'ASC',
      'number'  => 0,
      'post_type' => 'product',
    )
  );

  $payload = array(
    'schema_version' => '1.0',
    'exported_at'    => gmdate( 'Y-m-d\TH:i:s\Z' ),
    'source'         => array(
      'site_url' => home_url(),
      'platform' => 'wordpress-woocommerce',
      'theme'    => get_stylesheet() ? get_stylesheet() : 'beslock-custom',
    ),
    'interactions'   => array(),
  );

  $types = array(
    'review'   => 0,
    'question' => 0,
    'reply'    => 0,
  );
  $skipped = array();

  if ( is_array( $comments ) ) {
    foreach ( $comments as $comment ) {
      $interaction = beslock_interactions_exporter_build_interaction( $comment );

      if ( is_wp_error( $interaction ) ) {
        $skipped[] = array(
          'comment_id' => absint( $comment->comment_ID ?? 0 ),
          'reason'     => $interaction->get_error_message(),
        );
        continue;
      }

      if ( null === $interaction ) {
        continue;
      }

      $payload['interactions'][] = $interaction;

      if ( isset( $types[ $interaction['interaction_type'] ] ) ) {
        $types[ $interaction['interaction_type'] ]++;
      }
    }
  }

  $encoded = wp_json_encode( $payload, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE );
  if ( ! is_string( $encoded ) || '' === $encoded ) {
    return new WP_Error( 'beslock_interactions_exporter_encode', __( 'No se pudo serializar el snapshot de interacciones.', 'beslock' ) );
  }

  if ( false === file_put_contents( $snapshot_path, $encoded . PHP_EOL ) ) {
    return new WP_Error( 'beslock_interactions_exporter_write', __( 'No se pudo escribir interactions.json.', 'beslock' ) );
  }

  return array(
    'count'   => count( $payload['interactions'] ),
    'path'    => $snapshot_path,
    'types'   => $types,
    'skipped' => $skipped,
  );
}

function beslock_interactions_exporter_build_interaction( $comment ) {
  if ( ! is_object( $comment ) || empty( $comment->comment_ID ) ) {
    return null;
  }

  if ( ! beslock_interactions_exporter_is_exportable_comment( $comment ) ) {
    return null;
  }

  $interaction_type = beslock_interactions_exporter_get_interaction_type( $comment );
  $rating = absint( get_comment_meta( $comment->comment_ID, 'rating', true ) );

  if ( 'review' === $interaction_type && ( $rating < 1 || $rating > 5 ) ) {
    return new WP_Error( 'beslock_interactions_exporter_invalid_rating', __( 'Review sin rating válido.', 'beslock' ) );
  }

  if ( 'reply' === $interaction_type && empty( $comment->comment_parent ) ) {
    return new WP_Error( 'beslock_interactions_exporter_reply_parent', __( 'Reply sin parent.', 'beslock' ) );
  }

  $product_data = beslock_interactions_exporter_get_product_data( absint( $comment->comment_post_ID ), absint( $comment->comment_ID ) );
  if ( is_wp_error( $product_data ) ) {
    return $product_data;
  }

  $interaction_id = beslock_interactions_exporter_get_original_interaction_id( absint( $comment->comment_ID ) );
  $parent_interaction_id = beslock_interactions_exporter_get_original_parent_interaction_id( $comment );

  $author_name  = trim( wp_strip_all_tags( (string) $comment->comment_author ) );
  $author_email = sanitize_email( (string) $comment->comment_author_email );

  if ( '' === $author_name && '' === $author_email ) {
    return new WP_Error( 'beslock_interactions_exporter_author', __( 'Interacción sin nombre ni correo.', 'beslock' ) );
  }

  $status = beslock_interactions_exporter_map_comment_status( $comment->comment_approved ?? '0' );
  $created_at = beslock_interactions_exporter_format_mysql_gmt_to_iso(
    $comment->comment_date_gmt ?? '',
    $comment->comment_date ?? ''
  );

  $interaction = array(
    'interaction_id'   => $interaction_id,
    'interaction_type' => $interaction_type,
    'product'          => $product_data,
    'author'           => array(
      'name'         => $author_name,
      'email'        => $author_email,
      'display_name' => '' !== $author_name ? $author_name : $author_email,
    ),
    'content'          => array(
      'title' => '',
      'body'  => trim( (string) $comment->comment_content ),
    ),
    'status'           => $status,
    'thread'           => array(
      'parent_interaction_id' => $parent_interaction_id,
      'is_admin_response'     => ! empty( get_comment_meta( $comment->comment_ID, 'is_admin_response', true ) ),
    ),
    'timestamps'       => array(
      'created_at' => $created_at,
      'updated_at' => $created_at,
    ),
  );

  if ( 'review' === $interaction_type ) {
    $interaction['rating'] = $rating;
  }

  return $interaction;
}

function beslock_interactions_exporter_get_original_interaction_id( $comment_id ) {
  $comment_id = absint( $comment_id );
  if ( $comment_id <= 0 ) {
    return 0;
  }

  $original_interaction_id = absint( get_comment_meta( $comment_id, 'beslock_original_interaction_id', true ) );

  return $original_interaction_id > 0 ? $original_interaction_id : $comment_id;
}

function beslock_interactions_exporter_get_original_parent_interaction_id( $comment ) {
  if ( ! is_object( $comment ) || empty( $comment->comment_parent ) ) {
    return null;
  }

  $parent_comment_id = absint( $comment->comment_parent );
  $original_parent_interaction_id = beslock_interactions_exporter_get_original_interaction_id( $parent_comment_id );

  return $original_parent_interaction_id > 0 ? $original_parent_interaction_id : null;
}

function beslock_interactions_exporter_is_exportable_comment( $comment ) {
  if ( ! is_object( $comment ) ) {
    return false;
  }

  if ( empty( $comment->comment_post_ID ) || 'product' !== get_post_type( $comment->comment_post_ID ) ) {
    return false;
  }

  if ( in_array( (string) $comment->comment_type, array( 'pingback', 'trackback' ), true ) ) {
    return false;
  }

  if ( '' === trim( (string) $comment->comment_content ) ) {
    return false;
  }

  $interaction_type = beslock_interactions_exporter_get_interaction_type( $comment );

  return in_array( $interaction_type, array( 'review', 'question', 'reply' ), true );
}

function beslock_interactions_exporter_get_interaction_type( $comment ) {
  $interaction_type = sanitize_key( (string) get_comment_meta( $comment->comment_ID, 'interaction_type', true ) );
  if ( in_array( $interaction_type, array( 'review', 'question', 'reply' ), true ) ) {
    return $interaction_type;
  }

  $rating = absint( get_comment_meta( $comment->comment_ID, 'rating', true ) );
  if ( $rating > 0 ) {
    return 'review';
  }

  return '';
}

function beslock_interactions_exporter_get_product_data( $product_id, $comment_id = 0 ) {
  $product_id = absint( $product_id );
  if ( $product_id <= 0 || 'product' !== get_post_type( $product_id ) ) {
    return new WP_Error( 'beslock_interactions_exporter_product', __( 'No se pudo resolver el producto de la interacción.', 'beslock' ) );
  }

  $product = function_exists( 'wc_get_product' ) ? wc_get_product( $product_id ) : null;
  $slug = (string) get_post_field( 'post_name', $product_id );
  $name = wp_strip_all_tags( get_the_title( $product_id ) );
  $sku = '';

  if ( $product && is_a( $product, 'WC_Product' ) ) {
    $sku = (string) $product->get_sku();
  }

  if ( '' === $slug || '' === $name ) {
    return new WP_Error( 'beslock_interactions_exporter_product_fields', __( 'Producto sin slug o nombre exportable.', 'beslock' ) );
  }

  $original_product_id = absint( get_comment_meta( absint( $comment_id ), 'beslock_original_product_id', true ) );

  return array(
    'product_id' => $original_product_id > 0 ? $original_product_id : $product_id,
    'sku'        => $sku,
    'slug'       => $slug,
    'name'       => $name,
  );
}

function beslock_interactions_exporter_map_comment_status( $comment_approved ) {
  if ( '1' === (string) $comment_approved || 1 === $comment_approved ) {
    return 'approved';
  }

  if ( 'spam' === $comment_approved ) {
    return 'spam';
  }

  if ( 'trash' === $comment_approved ) {
    return 'trash';
  }

  return 'pending';
}

function beslock_interactions_exporter_format_mysql_gmt_to_iso( $mysql_gmt, $mysql_local = '' ) {
  $mysql_gmt = (string) $mysql_gmt;
  $mysql_local = (string) $mysql_local;

  if ( '' !== $mysql_gmt && '0000-00-00 00:00:00' !== $mysql_gmt ) {
    $timestamp = strtotime( $mysql_gmt . ' UTC' );
    if ( false !== $timestamp ) {
      return gmdate( 'Y-m-d\TH:i:s\Z', $timestamp );
    }
  }

  if ( '' !== $mysql_local && '0000-00-00 00:00:00' !== $mysql_local ) {
    $gmt = get_gmt_from_date( $mysql_local, 'Y-m-d H:i:s' );
    $timestamp = strtotime( $gmt . ' UTC' );
    if ( false !== $timestamp ) {
      return gmdate( 'Y-m-d\TH:i:s\Z', $timestamp );
    }
  }

  return gmdate( 'Y-m-d\TH:i:s\Z' );
}

function beslock_interactions_exporter_get_snapshot_path() {
  return trailingslashit( get_stylesheet_directory() ) . 'interactions/interactions.json';
}
