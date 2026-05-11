<?php
if ( ! defined( 'ABSPATH' ) ) {
  exit;
}

if ( ! function_exists( 'beslock_get_product_interaction_mode' ) ) {
  function beslock_get_product_interaction_mode() {
    $mode = isset( $_POST['beslock_interaction_type'] ) ? sanitize_key( wp_unslash( $_POST['beslock_interaction_type'] ) ) : 'review';
    return in_array( $mode, array( 'review', 'question', 'reply' ), true ) ? $mode : 'review';
  }
}

if ( ! function_exists( 'beslock_get_product_interaction_parent_comment_id' ) ) {
  function beslock_get_product_interaction_parent_comment_id() {
    return isset( $_POST['beslock_parent_comment_id'] ) ? absint( wp_unslash( $_POST['beslock_parent_comment_id'] ) ) : 0;
  }
}

if ( ! function_exists( 'beslock_get_product_interactions_feedback' ) ) {
  function beslock_get_product_interactions_feedback() {
    return array(
      'errors'            => array(),
      'success'           => '',
      'mode'              => beslock_get_product_interaction_mode(),
      'parent_comment_id' => beslock_get_product_interaction_parent_comment_id(),
      'values'            => array(
        'name'    => isset( $_POST['beslock_interaction_name'] ) ? sanitize_text_field( wp_unslash( $_POST['beslock_interaction_name'] ) ) : '',
        'email'   => isset( $_POST['beslock_interaction_email'] ) ? sanitize_email( wp_unslash( $_POST['beslock_interaction_email'] ) ) : '',
        'content' => isset( $_POST['beslock_interaction_content'] ) ? sanitize_textarea_field( wp_unslash( $_POST['beslock_interaction_content'] ) ) : '',
        'rating'  => isset( $_POST['beslock_interaction_rating'] ) ? absint( wp_unslash( $_POST['beslock_interaction_rating'] ) ) : 0,
      ),
    );
  }
}

if ( ! function_exists( 'beslock_validate_product_interaction_submission' ) ) {
  function beslock_validate_product_interaction_submission( $mode, $values ) {
    $errors = array();

    $name    = trim( (string) ( $values['name'] ?? '' ) );
    $email   = trim( (string) ( $values['email'] ?? '' ) );
    $content = trim( (string) ( $values['content'] ?? '' ) );
    $rating  = absint( $values['rating'] ?? 0 );

    if ( '' === $content ) {
      if ( 'question' === $mode ) {
        $errors[] = __( 'Escribe tu consulta.', 'beslock' );
      } elseif ( 'reply' === $mode ) {
        $errors[] = __( 'Escribe tu respuesta.', 'beslock' );
      } else {
        $errors[] = __( 'Escribe tu reseña.', 'beslock' );
      }
    }

    if ( '' === $name && '' === $email ) {
      $errors[] = __( 'Ingresa al menos tu nombre o tu correo.', 'beslock' );
    }

    if ( '' !== $email && ! is_email( $email ) ) {
      $errors[] = __( 'Ingresa un correo válido.', 'beslock' );
    }

    if ( 'review' === $mode && ( $rating < 1 || $rating > 5 ) ) {
      $errors[] = __( 'Selecciona una calificación.', 'beslock' );
    }

    return $errors;
  }
}

if ( ! function_exists( 'beslock_resolve_product_interaction_parent_comment_id' ) ) {
  function beslock_resolve_product_interaction_parent_comment_id( $product_id, $mode, $parent_comment_id ) {
    if ( 'reply' !== $mode ) {
      return 0;
    }

    if ( $parent_comment_id < 1 ) {
      return new WP_Error( 'missing_parent_comment', __( 'No se pudo identificar la consulta a responder.', 'beslock' ) );
    }

    $parent_comment = get_comment( $parent_comment_id );
    if ( ! $parent_comment || ! is_a( $parent_comment, 'WP_Comment' ) ) {
      return new WP_Error( 'invalid_parent_comment', __( 'No se pudo identificar la consulta a responder.', 'beslock' ) );
    }

    if ( absint( $parent_comment->comment_post_ID ) !== absint( $product_id ) ) {
      return new WP_Error( 'invalid_parent_product', __( 'No se pudo identificar la consulta a responder.', 'beslock' ) );
    }

    $parent_type = function_exists( 'beslock_get_product_comment_interaction_type' )
      ? beslock_get_product_comment_interaction_type( $parent_comment )
      : sanitize_key( (string) get_comment_meta( $parent_comment_id, 'interaction_type', true ) );

    if ( 'question' !== $parent_type || 1 !== absint( $parent_comment->comment_approved ) ) {
      return new WP_Error( 'invalid_parent_status', __( 'Solo puedes responder a una consulta publicada.', 'beslock' ) );
    }

    return absint( $parent_comment_id );
  }
}

if ( ! function_exists( 'beslock_create_product_interaction' ) ) {
  function beslock_create_product_interaction( $product_id, $mode, $values, $parent_comment_id = 0 ) {
    $commentdata = array(
      'comment_post_ID'      => absint( $product_id ),
      'comment_content'      => (string) ( $values['content'] ?? '' ),
      'comment_author'       => (string) ( $values['name'] ?? '' ),
      'comment_author_email' => (string) ( $values['email'] ?? '' ),
      'comment_parent'       => 'reply' === $mode ? absint( $parent_comment_id ) : 0,
      'comment_type'         => '',
      'comment_approved'     => 0,
    );

    $comment_id = wp_new_comment( wp_slash( $commentdata ), true );

    if ( is_wp_error( $comment_id ) ) {
      return $comment_id;
    }

    update_comment_meta( $comment_id, 'interaction_type', $mode );

    if ( 'review' === $mode ) {
      update_comment_meta( $comment_id, 'rating', absint( $values['rating'] ?? 0 ) );
    }

    return $comment_id;
  }
}

if ( ! function_exists( 'beslock_handle_product_interaction_submission' ) ) {
  function beslock_handle_product_interaction_submission() {
    if ( 'POST' !== strtoupper( $_SERVER['REQUEST_METHOD'] ?? '' ) ) {
      return;
    }

    if ( empty( $_POST['beslock_product_interaction_submit'] ) ) {
      return;
    }

    if ( empty( $_POST['beslock_product_interaction_nonce'] ) || ! wp_verify_nonce( sanitize_text_field( wp_unslash( $_POST['beslock_product_interaction_nonce'] ) ), 'beslock_product_interaction_submit' ) ) {
      return;
    }

    $product_id = isset( $_POST['beslock_product_id'] ) ? absint( wp_unslash( $_POST['beslock_product_id'] ) ) : 0;
    $mode       = beslock_get_product_interaction_mode();
    $feedback   = beslock_get_product_interactions_feedback();
    $errors     = beslock_validate_product_interaction_submission( $mode, $feedback['values'] );
    $parent_comment_id = beslock_get_product_interaction_parent_comment_id();

    if ( ! $product_id || 'product' !== get_post_type( $product_id ) ) {
      $errors[] = __( 'No se pudo identificar el producto.', 'beslock' );
    }

    if ( empty( $errors ) ) {
      $resolved_parent_comment_id = beslock_resolve_product_interaction_parent_comment_id( $product_id, $mode, $parent_comment_id );
      if ( is_wp_error( $resolved_parent_comment_id ) ) {
        $errors[] = $resolved_parent_comment_id->get_error_message();
      }
    }

    if ( empty( $errors ) ) {
      $created = beslock_create_product_interaction( $product_id, $mode, $feedback['values'], $resolved_parent_comment_id ?? 0 );

      if ( is_wp_error( $created ) ) {
        $errors[] = __( 'No se pudo enviar tu mensaje. Verifica los datos e inténtalo de nuevo.', 'beslock' );
      } else {
        if ( 'question' === $mode ) {
          $feedback['success'] = __( 'Gracias por tu consulta. Será revisada antes de publicarse.', 'beslock' );
        } elseif ( 'reply' === $mode ) {
          $feedback['success'] = __( 'Gracias por tu respuesta. Será revisada antes de publicarse.', 'beslock' );
        } else {
          $feedback['success'] = __( 'Gracias por tu reseña. Será revisada antes de publicarse.', 'beslock' );
        }

        $feedback['values'] = array(
          'name'    => '',
          'email'   => '',
          'content' => '',
          'rating'  => 0,
        );
        $feedback['parent_comment_id'] = 0;
      }
    }

    $feedback['errors'] = $errors;
    $GLOBALS['beslock_product_interactions_feedback'] = $feedback;
  }
  add_action( 'template_redirect', 'beslock_handle_product_interaction_submission', 20 );
}

if ( ! function_exists( 'beslock_render_product_interactions_block' ) ) {
  function beslock_render_product_interactions_block( $product ) {
    if ( is_numeric( $product ) && function_exists( 'wc_get_product' ) ) {
      $product = wc_get_product( absint( $product ) );
    }

    if ( ! $product || ! is_a( $product, 'WC_Product' ) ) {
      return;
    }

    $feedback = isset( $GLOBALS['beslock_product_interactions_feedback'] ) && is_array( $GLOBALS['beslock_product_interactions_feedback'] )
      ? $GLOBALS['beslock_product_interactions_feedback']
      : beslock_get_product_interactions_feedback();
    $questions = function_exists( 'beslock_get_product_questions_list' )
      ? beslock_get_product_questions_list( $product )
      : array();

    get_template_part(
      'template-parts/product/product-interactions-form',
      null,
      array(
        'product_id' => absint( $product->get_id() ),
        'product_name' => $product->get_name(),
        'feedback'   => $feedback,
        'questions'  => $questions,
      )
    );
  }
}
