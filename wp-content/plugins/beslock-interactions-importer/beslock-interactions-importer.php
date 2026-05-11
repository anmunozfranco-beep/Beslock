<?php
/*
Plugin Name: Beslock Interactions Importer
Description: Importa interactions.json a comments y comment meta con overwrite obligatorio por producto para el Stage 1.
Version: 1.0.0
Author: Beslock
*/

if ( ! defined( 'ABSPATH' ) ) {
  exit;
}

if ( ! defined( 'BESLOCK_INTERACTIONS_IMPORTER_VERSION' ) ) {
  define( 'BESLOCK_INTERACTIONS_IMPORTER_VERSION', '1.0.0' );
}

add_action( 'admin_menu', 'beslock_interactions_importer_register_menu' );

function beslock_interactions_importer_register_menu() {
  add_management_page(
    __( 'Beslock Interactions Import', 'beslock' ),
    __( 'Interactions Import', 'beslock' ),
    'manage_options',
    'beslock-interactions-import',
    'beslock_interactions_importer_render_page'
  );
}

function beslock_interactions_importer_render_page() {
  if ( ! current_user_can( 'manage_options' ) ) {
    wp_die( esc_html__( 'Acceso denegado.', 'beslock' ) );
  }

  $result = null;
  $error_message = '';

  if ( isset( $_POST['beslock_interactions_import_submit'] ) ) {
    check_admin_referer( 'beslock_interactions_import_action', 'beslock_interactions_import_nonce' );

    $result = beslock_interactions_importer_run_import();
    if ( is_wp_error( $result ) ) {
      $error_message = $result->get_error_message();
      $result = null;
    }
  }

  $snapshot_path = beslock_interactions_importer_get_snapshot_path();
  ?>
  <div class="wrap">
    <h1><?php echo esc_html__( 'Beslock Interactions Import', 'beslock' ); ?></h1>

    <?php if ( '' !== $error_message ) : ?>
      <div class="notice notice-error"><p><?php echo esc_html( $error_message ); ?></p></div>
    <?php endif; ?>

    <?php if ( is_array( $result ) ) : ?>
      <div class="notice notice-success">
        <p><?php echo esc_html__( 'Importación completada.', 'beslock' ); ?></p>
      </div>
      <ul>
        <li><?php echo esc_html( sprintf( __( 'Interacciones creadas: %d', 'beslock' ), intval( $result['created'] ) ) ); ?></li>
        <li><?php echo esc_html( sprintf( __( 'Interacciones eliminadas por overwrite: %d', 'beslock' ), intval( $result['deleted'] ) ) ); ?></li>
        <li><?php echo esc_html( sprintf( __( 'Productos afectados: %d', 'beslock' ), intval( $result['products'] ) ) ); ?></li>
      </ul>
    <?php endif; ?>

    <p><?php echo esc_html__( 'Lee el snapshot interactions.json del tema activo y reemplaza las interacciones de los productos incluidos en el archivo.', 'beslock' ); ?></p>
    <p><code><?php echo esc_html( $snapshot_path ); ?></code></p>
    <p><strong><?php echo esc_html__( 'Advertencia:', 'beslock' ); ?></strong> <?php echo esc_html__( 'el overwrite elimina las interacciones actuales de los productos presentes en el snapshot antes de restaurar el contenido.', 'beslock' ); ?></p>

    <form method="post">
      <?php wp_nonce_field( 'beslock_interactions_import_action', 'beslock_interactions_import_nonce' ); ?>
      <p>
        <button type="submit" name="beslock_interactions_import_submit" class="button button-primary">
          <?php echo esc_html__( 'Importar interactions.json', 'beslock' ); ?>
        </button>
      </p>
    </form>
  </div>
  <?php
}

function beslock_interactions_importer_run_import() {
  $snapshot = beslock_interactions_importer_load_snapshot();
  if ( is_wp_error( $snapshot ) ) {
    return $snapshot;
  }

  $prepared = beslock_interactions_importer_prepare_interactions( $snapshot['interactions'] );
  if ( is_wp_error( $prepared ) ) {
    return $prepared;
  }

  if ( empty( $prepared ) ) {
    return new WP_Error( 'beslock_interactions_importer_empty', __( 'El snapshot no contiene interacciones importables.', 'beslock' ) );
  }

  $product_ids = array_values( array_unique( array_map( 'intval', wp_list_pluck( $prepared, 'resolved_product_id' ) ) ) );
  $deleted = beslock_interactions_importer_delete_existing_interactions( $product_ids );
  if ( is_wp_error( $deleted ) ) {
    return $deleted;
  }

  $created = 0;
  $inserted_map = array();
  $remaining = $prepared;

  while ( ! empty( $remaining ) ) {
    $progress = false;
    $next_pass = array();

    foreach ( $remaining as $interaction ) {
      if ( 'reply' === $interaction['interaction_type'] ) {
        $parent_snapshot_id = $interaction['thread']['parent_interaction_id'];
        if ( ! isset( $inserted_map[ $parent_snapshot_id ] ) ) {
          $next_pass[] = $interaction;
          continue;
        }
      }

      $comment_id = beslock_interactions_importer_insert_interaction( $interaction, $inserted_map );
      if ( is_wp_error( $comment_id ) ) {
        return $comment_id;
      }

      $inserted_map[ $interaction['interaction_id'] ] = $comment_id;
      $created++;
      $progress = true;
    }

    if ( ! $progress ) {
      return new WP_Error( 'beslock_interactions_importer_parent_cycle', __( 'No se pudieron resolver las relaciones padre/hijo del snapshot.', 'beslock' ) );
    }

    $remaining = $next_pass;
  }

  foreach ( $product_ids as $product_id ) {
    beslock_interactions_importer_refresh_product_rating_meta( $product_id );
  }

  return array(
    'created'  => $created,
    'deleted'  => $deleted,
    'products' => count( $product_ids ),
  );
}

function beslock_interactions_importer_load_snapshot() {
  $snapshot_path = beslock_interactions_importer_get_snapshot_path();
  if ( ! file_exists( $snapshot_path ) ) {
    return new WP_Error( 'beslock_interactions_importer_missing_snapshot', __( 'No existe interactions.json en la carpeta esperada.', 'beslock' ) );
  }

  $raw = file_get_contents( $snapshot_path );
  if ( false === $raw || '' === trim( $raw ) ) {
    return new WP_Error( 'beslock_interactions_importer_empty_snapshot', __( 'El archivo interactions.json está vacío.', 'beslock' ) );
  }

  $decoded = json_decode( $raw, true );
  if ( ! is_array( $decoded ) ) {
    return new WP_Error( 'beslock_interactions_importer_invalid_json', __( 'interactions.json no contiene un JSON válido.', 'beslock' ) );
  }

  if ( empty( $decoded['schema_version'] ) || '1.0' !== (string) $decoded['schema_version'] ) {
    return new WP_Error( 'beslock_interactions_importer_schema', __( 'El snapshot no corresponde al schema_version 1.0.', 'beslock' ) );
  }

  if ( empty( $decoded['interactions'] ) || ! is_array( $decoded['interactions'] ) ) {
    return new WP_Error( 'beslock_interactions_importer_interactions', __( 'El snapshot no contiene el arreglo interactions.', 'beslock' ) );
  }

  return $decoded;
}

function beslock_interactions_importer_prepare_interactions( $items ) {
  $prepared = array();
  $seen_ids = array();

  foreach ( $items as $index => $item ) {
    if ( ! is_array( $item ) ) {
      return new WP_Error( 'beslock_interactions_importer_item', sprintf( __( 'La interacción #%d no es un objeto válido.', 'beslock' ), intval( $index ) + 1 ) );
    }

    $interaction_id = isset( $item['interaction_id'] ) ? absint( $item['interaction_id'] ) : 0;
    if ( $interaction_id <= 0 ) {
      return new WP_Error( 'beslock_interactions_importer_interaction_id', sprintf( __( 'La interacción #%d no tiene interaction_id válido.', 'beslock' ), intval( $index ) + 1 ) );
    }

    if ( isset( $seen_ids[ $interaction_id ] ) ) {
      return new WP_Error( 'beslock_interactions_importer_duplicate_id', sprintf( __( 'interaction_id duplicado en el snapshot: %d.', 'beslock' ), $interaction_id ) );
    }
    $seen_ids[ $interaction_id ] = true;

    $interaction_type = isset( $item['interaction_type'] ) ? sanitize_key( (string) $item['interaction_type'] ) : '';
    if ( ! in_array( $interaction_type, array( 'review', 'question', 'reply' ), true ) ) {
      return new WP_Error( 'beslock_interactions_importer_type', sprintf( __( 'interaction_type inválido para la interacción %d.', 'beslock' ), $interaction_id ) );
    }

    $author = isset( $item['author'] ) && is_array( $item['author'] ) ? $item['author'] : array();
    $author_name = isset( $author['name'] ) ? sanitize_text_field( (string) $author['name'] ) : '';
    $author_email = isset( $author['email'] ) ? sanitize_email( (string) $author['email'] ) : '';
    if ( '' === $author_name && '' === $author_email ) {
      return new WP_Error( 'beslock_interactions_importer_author', sprintf( __( 'La interacción %d no tiene nombre ni correo.', 'beslock' ), $interaction_id ) );
    }

    $content = isset( $item['content'] ) && is_array( $item['content'] ) ? $item['content'] : array();
    $body = isset( $content['body'] ) ? trim( (string) $content['body'] ) : '';
    if ( '' === $body ) {
      return new WP_Error( 'beslock_interactions_importer_body', sprintf( __( 'La interacción %d no tiene contenido.', 'beslock' ), $interaction_id ) );
    }

    $status = isset( $item['status'] ) ? sanitize_key( (string) $item['status'] ) : 'pending';
    if ( ! in_array( $status, array( 'approved', 'pending', 'spam', 'trash' ), true ) ) {
      return new WP_Error( 'beslock_interactions_importer_status', sprintf( __( 'La interacción %d tiene un status inválido.', 'beslock' ), $interaction_id ) );
    }

    $thread = isset( $item['thread'] ) && is_array( $item['thread'] ) ? $item['thread'] : array();
    $parent_interaction_id = isset( $thread['parent_interaction_id'] ) && null !== $thread['parent_interaction_id']
      ? absint( $thread['parent_interaction_id'] )
      : null;
    $is_admin_response = ! empty( $thread['is_admin_response'] );

    if ( 'reply' === $interaction_type && empty( $parent_interaction_id ) ) {
      return new WP_Error( 'beslock_interactions_importer_reply_parent', sprintf( __( 'La reply %d no tiene parent_interaction_id.', 'beslock' ), $interaction_id ) );
    }

    if ( 'review' === $interaction_type ) {
      $rating = isset( $item['rating'] ) ? absint( $item['rating'] ) : 0;
      if ( $rating < 1 || $rating > 5 ) {
        return new WP_Error( 'beslock_interactions_importer_rating', sprintf( __( 'La review %d no tiene rating válido.', 'beslock' ), $interaction_id ) );
      }
    } else {
      $rating = 0;
    }

    $timestamps = isset( $item['timestamps'] ) && is_array( $item['timestamps'] ) ? $item['timestamps'] : array();
    $created_at = isset( $timestamps['created_at'] ) ? (string) $timestamps['created_at'] : '';
    $created_timestamp = strtotime( $created_at );
    if ( false === $created_timestamp ) {
      return new WP_Error( 'beslock_interactions_importer_timestamp', sprintf( __( 'La interacción %d tiene created_at inválido.', 'beslock' ), $interaction_id ) );
    }

    $product = isset( $item['product'] ) && is_array( $item['product'] ) ? $item['product'] : array();
    $resolved_product_id = beslock_interactions_importer_resolve_product_id( $product );
    if ( is_wp_error( $resolved_product_id ) ) {
      return new WP_Error( 'beslock_interactions_importer_product', sprintf( __( 'No se pudo resolver el producto para la interacción %d: %s', 'beslock' ), $interaction_id, $resolved_product_id->get_error_message() ) );
    }

    $prepared[] = array(
      'interaction_id'      => $interaction_id,
      'interaction_type'    => $interaction_type,
      'original_product_id' => isset( $product['product_id'] ) ? absint( $product['product_id'] ) : 0,
      'resolved_product_id' => $resolved_product_id,
      'author'              => array(
        'name'         => $author_name,
        'email'        => $author_email,
        'display_name' => '' !== $author_name ? $author_name : $author_email,
      ),
      'content'             => array(
        'title' => '',
        'body'  => $body,
      ),
      'status'              => $status,
      'thread'              => array(
        'parent_interaction_id' => $parent_interaction_id,
        'is_admin_response'     => $is_admin_response,
      ),
      'timestamps'          => array(
        'created_at' => gmdate( 'Y-m-d\TH:i:s\Z', $created_timestamp ),
      ),
      'rating'              => $rating,
    );
  }

  foreach ( $prepared as $interaction ) {
    if ( 'reply' === $interaction['interaction_type'] && ! isset( $seen_ids[ $interaction['thread']['parent_interaction_id'] ] ) ) {
      return new WP_Error( 'beslock_interactions_importer_missing_parent', sprintf( __( 'La reply %d referencia un parent inexistente.', 'beslock' ), $interaction['interaction_id'] ) );
    }
  }

  usort(
    $prepared,
    static function( $left, $right ) {
      $left_is_reply = 'reply' === $left['interaction_type'];
      $right_is_reply = 'reply' === $right['interaction_type'];
      if ( $left_is_reply !== $right_is_reply ) {
        return $left_is_reply ? 1 : -1;
      }

      return $left['interaction_id'] <=> $right['interaction_id'];
    }
  );

  return $prepared;
}

function beslock_interactions_importer_resolve_product_id( $product ) {
  static $cache = array();

  $product = is_array( $product ) ? $product : array();
  $sku = isset( $product['sku'] ) ? trim( (string) $product['sku'] ) : '';
  $slug = isset( $product['slug'] ) ? sanitize_title( (string) $product['slug'] ) : '';
  $name = isset( $product['name'] ) ? trim( wp_strip_all_tags( (string) $product['name'] ) ) : '';

  $cache_key = md5( wp_json_encode( array( $sku, $slug, $name ) ) );
  if ( isset( $cache[ $cache_key ] ) ) {
    return $cache[ $cache_key ];
  }

  if ( '' !== $sku ) {
    $products = get_posts(
      array(
        'post_type'      => 'product',
        'post_status'    => array( 'publish', 'private', 'draft', 'pending', 'future' ),
        'posts_per_page' => 1,
        'fields'         => 'ids',
        'meta_key'       => '_sku',
        'meta_value'     => $sku,
      )
    );
    if ( ! empty( $products ) ) {
      $cache[ $cache_key ] = absint( $products[0] );
      return $cache[ $cache_key ];
    }
  }

  if ( '' !== $slug ) {
    $post = get_page_by_path( $slug, OBJECT, 'product' );
    if ( $post && ! empty( $post->ID ) ) {
      $cache[ $cache_key ] = absint( $post->ID );
      return $cache[ $cache_key ];
    }

    $products = get_posts(
      array(
        'post_type'      => 'product',
        'post_status'    => array( 'publish', 'private', 'draft', 'pending', 'future' ),
        'name'           => $slug,
        'posts_per_page' => 1,
        'fields'         => 'ids',
      )
    );
    if ( ! empty( $products ) ) {
      $cache[ $cache_key ] = absint( $products[0] );
      return $cache[ $cache_key ];
    }
  }

  if ( '' !== $name ) {
    global $wpdb;
    $product_id = $wpdb->get_var(
      $wpdb->prepare(
        "SELECT ID FROM {$wpdb->posts} WHERE post_type = 'product' AND post_status IN ('publish','private','draft','pending','future') AND post_title = %s LIMIT 1",
        $name
      )
    );

    if ( $product_id ) {
      $cache[ $cache_key ] = absint( $product_id );
      return $cache[ $cache_key ];
    }
  }

  $cache[ $cache_key ] = new WP_Error( 'beslock_interactions_importer_product_lookup', __( 'sin coincidencia por sku, slug ni nombre', 'beslock' ) );
  return $cache[ $cache_key ];
}

function beslock_interactions_importer_delete_existing_interactions( $product_ids ) {
  $deleted = 0;

  foreach ( $product_ids as $product_id ) {
    $comments = get_comments(
      array(
        'post_id'  => absint( $product_id ),
        'status'   => 'all',
        'orderby'  => 'comment_ID',
        'order'    => 'DESC',
        'number'   => 0,
      )
    );

    if ( ! is_array( $comments ) ) {
      continue;
    }

    foreach ( $comments as $comment ) {
      if ( in_array( (string) $comment->comment_type, array( 'pingback', 'trackback' ), true ) ) {
        continue;
      }

      if ( wp_delete_comment( $comment->comment_ID, true ) ) {
        $deleted++;
      }
    }
  }

  return $deleted;
}

function beslock_interactions_importer_insert_interaction( $interaction, $inserted_map ) {
  $created_timestamp = strtotime( $interaction['timestamps']['created_at'] );
  $comment_date_gmt = gmdate( 'Y-m-d H:i:s', $created_timestamp );
  $comment_date = get_date_from_gmt( $comment_date_gmt, 'Y-m-d H:i:s' );

  $commentdata = array(
    'comment_post_ID'      => absint( $interaction['resolved_product_id'] ),
    'comment_author'       => $interaction['author']['name'],
    'comment_author_email' => $interaction['author']['email'],
    'comment_content'      => $interaction['content']['body'],
    'comment_type'         => '',
    'comment_parent'       => 'reply' === $interaction['interaction_type']
      ? absint( $inserted_map[ $interaction['thread']['parent_interaction_id'] ] )
      : 0,
    'comment_approved'     => beslock_interactions_importer_map_status_to_comment_approved( $interaction['status'] ),
    'comment_date'         => $comment_date,
    'comment_date_gmt'     => $comment_date_gmt,
    'comment_agent'        => 'beslock-stage1-importer',
  );

  $comment_id = wp_insert_comment( wp_slash( $commentdata ) );
  if ( ! $comment_id || is_wp_error( $comment_id ) ) {
    return new WP_Error( 'beslock_interactions_importer_insert', sprintf( __( 'No se pudo insertar la interacción %d.', 'beslock' ), $interaction['interaction_id'] ) );
  }

  update_comment_meta( $comment_id, 'interaction_type', $interaction['interaction_type'] );
  update_comment_meta( $comment_id, 'beslock_original_interaction_id', absint( $interaction['interaction_id'] ) );

  if ( ! empty( $interaction['original_product_id'] ) ) {
    update_comment_meta( $comment_id, 'beslock_original_product_id', absint( $interaction['original_product_id'] ) );
  }

  if ( 'review' === $interaction['interaction_type'] ) {
    update_comment_meta( $comment_id, 'rating', absint( $interaction['rating'] ) );
  }

  if ( 'reply' === $interaction['interaction_type'] && ! empty( $interaction['thread']['is_admin_response'] ) ) {
    update_comment_meta( $comment_id, 'is_admin_response', 1 );
  }

  if ( 'spam' === $interaction['status'] ) {
    wp_spam_comment( $comment_id );
  } elseif ( 'trash' === $interaction['status'] ) {
    wp_trash_comment( $comment_id );
  }

  return absint( $comment_id );
}

function beslock_interactions_importer_map_status_to_comment_approved( $status ) {
  if ( 'approved' === $status ) {
    return 1;
  }

  return 0;
}

function beslock_interactions_importer_refresh_product_rating_meta( $product_id ) {
  $comments = get_comments(
    array(
      'post_id' => absint( $product_id ),
      'status'  => 'approve',
      'number'  => 0,
    )
  );

  $rating_counts = array(
    1 => 0,
    2 => 0,
    3 => 0,
    4 => 0,
    5 => 0,
  );
  $review_count = 0;
  $rating_total = 0;

  if ( is_array( $comments ) ) {
    foreach ( $comments as $comment ) {
      if ( in_array( (string) $comment->comment_type, array( 'pingback', 'trackback' ), true ) ) {
        continue;
      }

      $interaction_type = sanitize_key( (string) get_comment_meta( $comment->comment_ID, 'interaction_type', true ) );
      $rating = absint( get_comment_meta( $comment->comment_ID, 'rating', true ) );

      if ( 'review' !== $interaction_type && $rating <= 0 ) {
        continue;
      }

      if ( $rating < 1 || $rating > 5 ) {
        continue;
      }

      $rating_counts[ $rating ]++;
      $review_count++;
      $rating_total += $rating;
    }
  }

  update_post_meta( $product_id, '_wc_rating_count', $rating_counts );
  update_post_meta( $product_id, '_wc_review_count', $review_count );
  update_post_meta( $product_id, '_wc_average_rating', $review_count > 0 ? number_format( $rating_total / $review_count, 2, '.', '' ) : '0' );

  if ( function_exists( 'wc_delete_product_transients' ) ) {
    wc_delete_product_transients( $product_id );
  }
}

function beslock_interactions_importer_get_snapshot_path() {
  return trailingslashit( get_stylesheet_directory() ) . 'interactions/interactions.json';
}
