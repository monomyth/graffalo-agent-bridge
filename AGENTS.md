# Public companion repository

This repository contains only the MIT-licensed local agent bridge. Never copy
Graffalo editor/backend source, document data, credentials, environment files,
private assets, or Graffalo Git history into it. Test only with synthetic data.
Do not make provider requests or change native agent logins in automated tests.

Preserve exact-origin/loopback/pairing checks and diagram review before writes.
No API-key collection, credentials database, telemetry, or general shell service.
Keep dependencies permissive. Run notices.py after Cargo.lock changes; CI rejects
unreviewed license expressions. Ship all notices with binaries.

GitHub is the publication upstream; Origin is its inbound mirror. Push changes to
GitHub and verify the corresponding ref is synchronized in Origin. Never push
unrelated Graffalo branches/history here. Release only after CI succeeds; use
prereleases while live compatibility/platform signing remain unverified.
