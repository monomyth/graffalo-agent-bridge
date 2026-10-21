# GitHub and Origin

GitHub upstream: https://github.com/monomyth/graffalo-agent-bridge

Origin mirror: https://origin.cursor.com/monomyth/graffalo-agent-bridge.git

This is an **inbound GitHub mirror**. Publish bridge branches and tags to GitHub;
Origin fetches the corresponding refs. Do not maintain two independently writable
copies or point the bridge at Graffalo's private application repositories.

The maintainer checkout uses `github` for the public upstream and `origin` for the
Origin mirror. Verify synchronization with:

```sh
git ls-remote github refs/heads/main
git ls-remote origin refs/heads/main
origin repo mirror status --repo monomyth/graffalo-agent-bridge
```

If a webhook is delayed, use Origin's explicit mirror-sync command for the ref,
then compare its SHA with GitHub. Mirror availability/access depends on the
maintainer's Origin installation and repository permissions.
