<?php
if ( ! defined( 'ABSPATH' ) ) {
  exit;
}

$product_id   = isset( $args['product_id'] ) ? absint( $args['product_id'] ) : 0;
$product_name = isset( $args['product_name'] ) ? wp_strip_all_tags( (string) $args['product_name'] ) : '';
$feedback     = isset( $args['feedback'] ) && is_array( $args['feedback'] ) ? $args['feedback'] : array();
$questions    = isset( $args['questions'] ) && is_array( $args['questions'] ) ? $args['questions'] : array();
$mode         = isset( $feedback['mode'] ) ? sanitize_key( (string) $feedback['mode'] ) : 'review';
$feedback_parent_comment_id = isset( $feedback['parent_comment_id'] ) ? absint( $feedback['parent_comment_id'] ) : 0;
$values       = isset( $feedback['values'] ) && is_array( $feedback['values'] ) ? $feedback['values'] : array();
$errors       = isset( $feedback['errors'] ) && is_array( $feedback['errors'] ) ? $feedback['errors'] : array();
$success      = isset( $feedback['success'] ) ? (string) $feedback['success'] : '';
$form_action  = $product_id ? get_permalink( $product_id ) : '';

$is_reply_feedback = 'reply' === $mode;
$main_form_mode = in_array( $mode, array( 'review', 'question' ), true ) ? $mode : 'review';
$main_form_values = $is_reply_feedback ? array(
  'name'    => '',
  'email'   => '',
  'content' => '',
  'rating'  => 0,
) : $values;
$reply_form_values = $is_reply_feedback ? $values : array(
  'name'    => '',
  'email'   => '',
  'content' => '',
);

$name_value    = isset( $main_form_values['name'] ) ? (string) $main_form_values['name'] : '';
$email_value   = isset( $main_form_values['email'] ) ? (string) $main_form_values['email'] : '';
$content_value = isset( $main_form_values['content'] ) ? (string) $main_form_values['content'] : '';
$rating_value  = isset( $main_form_values['rating'] ) ? absint( $main_form_values['rating'] ) : 0;
$reply_name_value    = isset( $reply_form_values['name'] ) ? (string) $reply_form_values['name'] : '';
$reply_email_value   = isset( $reply_form_values['email'] ) ? (string) $reply_form_values['email'] : '';
$reply_content_value = isset( $reply_form_values['content'] ) ? (string) $reply_form_values['content'] : '';
?>

<section class="product-interactions" aria-labelledby="product-interactions-title">
  <div class="product-interactions__header">
    <div>
      <h2 id="product-interactions-title"><?php echo esc_html__( 'Formulario de reseñas y consultas', 'beslock' ); ?></h2>
    </div>
    <p class="product-interactions__description">
      <?php
      printf(
        esc_html__( 'Comparte tu experiencia o deja una consulta sobre %s.', 'beslock' ),
        esc_html( $product_name )
      );
      ?>
    </p>
  </div>

  <div class="product-interactions__surface product-interactions__surface--form">
    <?php if ( ! empty( $success ) ) : ?>
      <div class="product-interactions__notice product-interactions__notice--success" role="status">
        <p><?php echo esc_html( $success ); ?></p>
      </div>
    <?php endif; ?>

    <?php if ( ! empty( $errors ) && ! $is_reply_feedback ) : ?>
      <div class="product-interactions__notice product-interactions__notice--error" role="alert">
        <ul>
          <?php foreach ( $errors as $error_message ) : ?>
            <li><?php echo esc_html( $error_message ); ?></li>
          <?php endforeach; ?>
        </ul>
      </div>
    <?php endif; ?>

    <form class="product-interactions__form" method="post" action="<?php echo esc_url( $form_action ); ?>">
      <div class="product-interactions__top-row">
        <fieldset class="product-interactions__modes">
          <legend class="screen-reader-text"><?php echo esc_html__( 'Quiero enviar', 'beslock' ); ?></legend>
          <label class="product-interactions__mode-option">
            <input type="radio" name="beslock_interaction_type" value="review" <?php checked( $main_form_mode, 'review' ); ?>>
            <span><?php echo esc_html__( 'Reseña', 'beslock' ); ?></span>
          </label>
          <label class="product-interactions__mode-option">
            <input type="radio" name="beslock_interaction_type" value="question" <?php checked( $main_form_mode, 'question' ); ?>>
            <span><?php echo esc_html__( 'Consulta', 'beslock' ); ?></span>
          </label>
        </fieldset>

        <div class="product-interactions__field product-interactions__rating">
          <fieldset class="product-interactions__stars" aria-label="<?php echo esc_attr__( 'Selecciona una calificación', 'beslock' ); ?>">
            <legend class="screen-reader-text"><?php echo esc_html__( 'Selecciona una calificación', 'beslock' ); ?></legend>
            <span class="product-interactions__stars-label"><?php echo esc_html__( 'Calificación', 'beslock' ); ?></span>
            <div class="product-interactions__stars-options">
              <?php for ( $rating = 5; $rating >= 1; $rating-- ) : ?>
                <div class="product-interactions__star-option">
                  <input
                    id="beslock-interaction-rating-<?php echo esc_attr( $product_id ); ?>-<?php echo esc_attr( $rating ); ?>"
                    type="radio"
                    name="beslock_interaction_rating"
                    value="<?php echo esc_attr( $rating ); ?>"
                    <?php checked( $rating_value, $rating ); ?>
                  >
                  <label for="beslock-interaction-rating-<?php echo esc_attr( $product_id ); ?>-<?php echo esc_attr( $rating ); ?>">
                    <span class="product-interactions__star-number"><?php echo esc_html( $rating ); ?></span>
                    <span class="product-interactions__star-icon" aria-hidden="true">&#9733;</span>
                  </label>
                </div>
              <?php endfor; ?>
            </div>
          </fieldset>
        </div>
      </div>

      <div class="product-interactions__field">
        <label for="beslock-interaction-content-<?php echo esc_attr( $product_id ); ?>"><?php echo esc_html__( 'Tu mensaje', 'beslock' ); ?></label>
        <textarea id="beslock-interaction-content-<?php echo esc_attr( $product_id ); ?>" name="beslock_interaction_content" rows="5" required><?php echo esc_textarea( $content_value ); ?></textarea>
      </div>

      <div class="product-interactions__row">
        <div class="product-interactions__field">
          <label for="beslock-interaction-name-<?php echo esc_attr( $product_id ); ?>"><?php echo esc_html__( 'Nombre', 'beslock' ); ?></label>
          <input id="beslock-interaction-name-<?php echo esc_attr( $product_id ); ?>" type="text" name="beslock_interaction_name" value="<?php echo esc_attr( $name_value ); ?>" autocomplete="name">
        </div>
        <div class="product-interactions__field">
          <label for="beslock-interaction-email-<?php echo esc_attr( $product_id ); ?>"><?php echo esc_html__( 'Correo electrónico', 'beslock' ); ?></label>
          <input id="beslock-interaction-email-<?php echo esc_attr( $product_id ); ?>" type="email" name="beslock_interaction_email" value="<?php echo esc_attr( $email_value ); ?>" autocomplete="email">
        </div>
      </div>

      <p class="product-interactions__hint"><?php echo esc_html__( 'Ingresa al menos tu nombre o tu correo.', 'beslock' ); ?></p>

      <?php wp_nonce_field( 'beslock_product_interaction_submit', 'beslock_product_interaction_nonce' ); ?>
      <input type="hidden" name="beslock_product_id" value="<?php echo esc_attr( $product_id ); ?>">
      <button class="product-interactions__submit" type="submit" name="beslock_product_interaction_submit" value="1"><?php echo esc_html__( 'Enviar', 'beslock' ); ?></button>
    </form>
  </div>

  <div class="product-interactions__questions-header">
    <h3><?php echo esc_html__( 'Preguntas y respuestas', 'beslock' ); ?></h3>
    <p><?php echo esc_html__( 'Aquí verás las consultas aprobadas para este producto y, cuando existan, sus respuestas.', 'beslock' ); ?></p>
  </div>

  <div class="product-interactions__surface product-interactions__questions">

    <?php if ( ! empty( $questions ) ) : ?>
      <ol class="product-interactions__question-list">
        <?php foreach ( $questions as $question ) : ?>
          <?php
          $question_comment_id = isset( $question['comment_id'] ) ? absint( $question['comment_id'] ) : 0;
          $show_reply_form = $is_reply_feedback && $feedback_parent_comment_id === $question_comment_id;
          $reply_dialog_id = sprintf( 'beslock-reply-dialog-%d', $question_comment_id );
          $reply_dialog_heading_id = sprintf( 'beslock-reply-dialog-heading-%d', $question_comment_id );
          ?>
          <li class="product-interactions__question-item">
            <div class="product-interactions__question-meta">
              <strong><?php echo esc_html( $question['author'] ?? '' ); ?></strong>
              <?php if ( ! empty( $question['date'] ) ) : ?>
                <time class="product-interactions__question-date" datetime="<?php echo esc_attr( $question['date_iso'] ?? '' ); ?>"><?php echo esc_html( $question['date'] ); ?></time>
              <?php endif; ?>
            </div>
            <p class="product-interactions__question-text"><?php echo esc_html( $question['text'] ?? '' ); ?></p>

            <?php if ( ! empty( $question['replies'] ) && is_array( $question['replies'] ) ) : ?>
              <ul class="product-interactions__reply-list">
                <?php foreach ( $question['replies'] as $reply ) : ?>
                  <li class="product-interactions__reply-item <?php echo ! empty( $reply['is_admin_response'] ) ? 'product-interactions__reply-item--admin' : 'product-interactions__reply-item--community'; ?>">
                    <div class="product-interactions__reply-meta">
                      <strong><?php echo esc_html( $reply['author'] ?? '' ); ?></strong>
                      <?php if ( ! empty( $reply['is_admin_response'] ) ) : ?>
                        <span class="product-interactions__reply-badge"><?php echo esc_html__( 'Beslock', 'beslock' ); ?></span>
                      <?php endif; ?>
                      <?php if ( ! empty( $reply['date'] ) ) : ?>
                        <time class="product-interactions__reply-date" datetime="<?php echo esc_attr( $reply['date_iso'] ?? '' ); ?>"><?php echo esc_html( $reply['date'] ); ?></time>
                      <?php endif; ?>
                    </div>
                    <p><?php echo esc_html( $reply['text'] ?? '' ); ?></p>
                  </li>
                <?php endforeach; ?>
              </ul>
            <?php endif; ?>

            <?php if ( $question_comment_id > 0 ) : ?>
              <div class="product-interactions__thread-actions">
                <button
                  class="product-interactions__reply-trigger"
                  type="button"
                  data-reply-dialog-trigger
                  data-reply-dialog-id="<?php echo esc_attr( $reply_dialog_id ); ?>"
                  aria-controls="<?php echo esc_attr( $reply_dialog_id ); ?>"
                  aria-expanded="<?php echo $show_reply_form ? 'true' : 'false'; ?>"
                  aria-haspopup="dialog"
                >
                  <?php echo esc_html__( 'Responder', 'beslock' ); ?>
                </button>

                <dialog
                  id="<?php echo esc_attr( $reply_dialog_id ); ?>"
                  class="product-interactions__reply-dialog"
                  aria-labelledby="<?php echo esc_attr( $reply_dialog_heading_id ); ?>"
                  <?php echo $show_reply_form ? 'data-open-on-load="true"' : ''; ?>
                >
                  <div class="product-interactions__reply-dialog-inner">
                    <div class="product-interactions__reply-dialog-header">
                      <div class="product-interactions__reply-dialog-copy">
                        <p class="product-interactions__reply-dialog-kicker"><?php echo esc_html__( 'Responder en el hilo', 'beslock' ); ?></p>
                        <h4 id="<?php echo esc_attr( $reply_dialog_heading_id ); ?>"><?php echo esc_html__( 'Publica tu respuesta', 'beslock' ); ?></h4>
                      </div>
                      <button type="button" class="product-interactions__reply-dialog-close" data-reply-dialog-close aria-label="<?php echo esc_attr__( 'Cerrar formulario de respuesta', 'beslock' ); ?>">&times;</button>
                    </div>

                    <p class="product-interactions__reply-context"><?php echo esc_html( $question['text'] ?? '' ); ?></p>

                    <form class="product-interactions__reply-form" method="post" action="<?php echo esc_url( $form_action ); ?>">
                      <?php if ( $show_reply_form && ! empty( $errors ) ) : ?>
                        <div class="product-interactions__notice product-interactions__notice--error product-interactions__notice--inline" role="alert">
                          <ul>
                            <?php foreach ( $errors as $error_message ) : ?>
                              <li><?php echo esc_html( $error_message ); ?></li>
                            <?php endforeach; ?>
                          </ul>
                        </div>
                      <?php endif; ?>

                      <div class="product-interactions__field">
                        <label for="beslock-interaction-reply-content-<?php echo esc_attr( $question_comment_id ); ?>"><?php echo esc_html__( 'Tu respuesta', 'beslock' ); ?></label>
                        <textarea id="beslock-interaction-reply-content-<?php echo esc_attr( $question_comment_id ); ?>" name="beslock_interaction_content" rows="4" required><?php echo esc_textarea( $show_reply_form ? $reply_content_value : '' ); ?></textarea>
                      </div>

                      <div class="product-interactions__row product-interactions__row--reply">
                        <div class="product-interactions__field">
                          <label for="beslock-interaction-reply-name-<?php echo esc_attr( $question_comment_id ); ?>"><?php echo esc_html__( 'Nombre', 'beslock' ); ?></label>
                          <input id="beslock-interaction-reply-name-<?php echo esc_attr( $question_comment_id ); ?>" type="text" name="beslock_interaction_name" value="<?php echo esc_attr( $show_reply_form ? $reply_name_value : '' ); ?>" autocomplete="name">
                        </div>
                        <div class="product-interactions__field">
                          <label for="beslock-interaction-reply-email-<?php echo esc_attr( $question_comment_id ); ?>"><?php echo esc_html__( 'Correo electrónico', 'beslock' ); ?></label>
                          <input id="beslock-interaction-reply-email-<?php echo esc_attr( $question_comment_id ); ?>" type="email" name="beslock_interaction_email" value="<?php echo esc_attr( $show_reply_form ? $reply_email_value : '' ); ?>" autocomplete="email">
                        </div>
                      </div>

                      <p class="product-interactions__hint product-interactions__hint--reply"><?php echo esc_html__( 'Para responder, ingresa tu nombre, tu correo o ambos.', 'beslock' ); ?></p>

                      <?php wp_nonce_field( 'beslock_product_interaction_submit', 'beslock_product_interaction_nonce' ); ?>
                      <input type="hidden" name="beslock_product_id" value="<?php echo esc_attr( $product_id ); ?>">
                      <input type="hidden" name="beslock_interaction_type" value="reply">
                      <input type="hidden" name="beslock_parent_comment_id" value="<?php echo esc_attr( $question_comment_id ); ?>">
                      <button class="product-interactions__submit product-interactions__submit--reply" type="submit" name="beslock_product_interaction_submit" value="1"><?php echo esc_html__( 'Publicar respuesta', 'beslock' ); ?></button>
                    </form>
                  </div>
                </dialog>
              </div>
            <?php endif; ?>
          </li>
        <?php endforeach; ?>
      </ol>
    <?php else : ?>
      <div class="product-interactions__empty-state">
        <p><?php echo esc_html__( 'Todavía no hay consultas publicadas para este producto.', 'beslock' ); ?></p>
      </div>
    <?php endif; ?>
  </div>
</section>
