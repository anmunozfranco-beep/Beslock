<?php
if ( ! defined( 'ABSPATH' ) ) {
  exit;
}

function beslock_register_hero_startup_telemetry_route() {
  register_rest_route(
    'beslock/v1',
    '/hero-startup',
    array(
      'methods'             => WP_REST_Server::CREATABLE,
      'permission_callback' => '__return_true',
      'callback'            => 'beslock_handle_hero_startup_telemetry',
    )
  );
}
add_action( 'rest_api_init', 'beslock_register_hero_startup_telemetry_route' );

function beslock_handle_hero_startup_telemetry( WP_REST_Request $request ) {
  $payload = $request->get_json_params();

  if ( ! is_array( $payload ) ) {
    $payload = array();
  }

  $event = array(
    'sessionId'      => isset( $payload['sessionId'] ) ? substr( sanitize_text_field( wp_unslash( $payload['sessionId'] ) ), 0, 80 ) : '',
    'state'          => isset( $payload['state'] ) ? sanitize_key( $payload['state'] ) : '',
    'reason'         => isset( $payload['reason'] ) ? substr( preg_replace( '/[^a-z0-9:_-]/i', '', (string) $payload['reason'] ), 0, 80 ) : '',
    'navigationType' => isset( $payload['navigationType'] ) ? substr( preg_replace( '/[^a-z0-9_-]/i', '', (string) $payload['navigationType'] ), 0, 40 ) : '',
    'path'           => isset( $payload['path'] ) ? substr( sanitize_text_field( wp_unslash( $payload['path'] ) ), 0, 200 ) : '',
    'atMs'           => isset( $payload['atMs'] ) ? round( (float) $payload['atMs'], 1 ) : null,
    'waitedMs'       => isset( $payload['waitedMs'] ) ? round( (float) $payload['waitedMs'], 1 ) : null,
    'currentTime'    => isset( $payload['currentTime'] ) ? round( (float) $payload['currentTime'], 3 ) : null,
    'readyState'     => isset( $payload['readyState'] ) ? (int) $payload['readyState'] : null,
    'viewportWidth'  => isset( $payload['viewportWidth'] ) ? (int) $payload['viewportWidth'] : null,
    'viewportHeight' => isset( $payload['viewportHeight'] ) ? (int) $payload['viewportHeight'] : null,
    'blocked'        => ! empty( $payload['blocked'] ),
    'errorName'      => isset( $payload['errorName'] ) ? substr( preg_replace( '/[^a-z0-9._-]/i', '', (string) $payload['errorName'] ), 0, 60 ) : '',
    'reportedAtUtc'  => gmdate( 'c' ),
  );

  $allowed_states = array( 'ready', 'image-fallback', 'reduced-motion' );

  if ( ! in_array( $event['state'], $allowed_states, true ) ) {
    return new WP_REST_Response( array( 'ok' => false, 'ignored' => true ), 202 );
  }

  do_action( 'beslock_hero_startup_telemetry', $event, $request );

  if ( defined( 'WP_DEBUG' ) && WP_DEBUG ) {
    error_log( 'beslock_hero_startup ' . wp_json_encode( $event ) );
  }

  return new WP_REST_Response( array( 'ok' => true ), 202 );
}
