# 10-cli-only-no-daemon-composition

Browser surfaces NEVER write the filesystem. All composition mutation occurs only via the CLI executor with --confirm. No daemon, no watcher, no scheduler.
