# 10-cli-only-no-daemon-extraction

Browser surfaces NEVER write the filesystem. All extraction mutation occurs only via the CLI executor with --confirm. No daemon. No watcher. No scheduler. No background worker.
