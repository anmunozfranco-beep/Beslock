# User-Skill Models

## Models

- **beginner** — {"audience": "first-time end user", "complexity_ceiling": "low", "permissions": ["operate", "request-help"], "defaults": ["expanded-prereqs", "irreversibility-warnings-explicit", "no-batching"]}
- **intermediate** — {"audience": "returning end user", "complexity_ceiling": "medium", "permissions": ["operate", "self-troubleshoot-tier1"], "defaults": ["compact-prereqs", "batched-non-destructive"]}
- **advanced** — {"audience": "power user / facility owner", "complexity_ceiling": "high", "permissions": ["operate", "configure", "self-troubleshoot-tier2"], "defaults": ["batched-non-destructive", "advanced-options-visible"]}
- **installer** — {"audience": "professional installer", "complexity_ceiling": "high", "permissions": ["install", "configure", "verify-install"], "defaults": ["batched-non-destructive", "skip-orientation"]}
- **administrator** — {"audience": "site/system admin", "complexity_ceiling": "high", "permissions": ["configure", "admin-actions", "delete-users", "factory-reset"], "defaults": ["full-controls", "irreversibility-warnings-explicit"]}
- **operator** — {"audience": "day-to-day operator with limited authority", "complexity_ceiling": "medium", "permissions": ["operate", "log-incidents"], "defaults": ["compact-prereqs", "no-admin-controls"]}
- **maintenance** — {"audience": "field maintenance technician", "complexity_ceiling": "high", "permissions": ["operate", "battery-replacement", "diagnostics", "verify-install"], "defaults": ["diagnostics-visible", "physical-presence-required"]}

## Rules

- skill never widens permissions beyond authority-area declarations
- skill never lowers safeguards (only presentation density)
- advanced/installer/administrator/maintenance may batch only non-destructive steps
- factory-reset and delete-all-users remain administrator-only across all skills
