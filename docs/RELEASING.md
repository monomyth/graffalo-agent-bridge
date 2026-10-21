# Releases

1. Update Cargo.toml with a SemVer version (use `-alpha.N` while experimental),
   update Cargo.lock with Cargo, and write docs/RELEASE_NOTES.md.
2. Run CI checks, regenerate notices after dependency changes, and review the
   complete publication file set. Never import Graffalo history or private code.
3. Commit and push to GitHub main. Wait for all native checks to pass.
4. Tag that reviewed commit `vVERSION` and push the tag to GitHub.
5. The Build workflow tests and packages five native targets. Only after every
   build succeeds does the publish job assemble SHA256SUMS and publish the release.
   Versions containing `-` are prereleases. Reruns replace assets deterministically.
6. Verify download contents/digests, smoke-test the native binary, and verify Origin
   mirror synchronization for main and the release tag.

Actions are pinned to immutable commits. Release creation alone has contents-write
permission. PR workflows cannot publish. Builds use Cargo.lock and pinned Rust.
The archives contain binaries, launchers, README, LICENSE, and third-party notices;
they do not include workspace files, provider binaries, credentials, or a database.

Current release archives are unsigned; macOS notarization and Windows signing need
owner-provided certificates configured as scoped GitHub Actions secrets in a
separate change. Do not claim signing until it is verified. A tray app, one-click
pairing, automatic updates, and native installers are follow-up work.
