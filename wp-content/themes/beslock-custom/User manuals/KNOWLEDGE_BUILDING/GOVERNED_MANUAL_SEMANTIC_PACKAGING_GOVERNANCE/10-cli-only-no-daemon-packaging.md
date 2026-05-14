# 10-cli-only-no-daemon-packaging

Browser surfaces NEVER write the filesystem. All packaging mutation occurs only via the CLI executor with --confirm. No daemon. No watcher. No scheduler. No background worker. No telemetry.
