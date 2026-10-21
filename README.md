# Graffalo Agent Bridge

An experimental local companion that connects Graffalo's diagram chat to an
installed, signed-in **Codex** or **Grok Build**. Your agent manages its own provider
login. Graffalo does not collect model API keys or provider passwords.

**Status: alpha.** Protocol fixtures and native build checks are automated; live
account compatibility and browser-to-companion connectivity need validation on
your machine. This is a command-line companion with launchers, not a tray app.
These alpha releases are unsigned and not notarized; macOS/Windows may block it. Do not
disable OS protections. Build from reviewed source if your OS blocks the download.

## Download and run

Download the archive for your computer from [GitHub Releases](https://github.com/monomyth/graffalo-agent-bridge/releases).
Extract it before running. No Rust installation or Graffalo source checkout is
needed for these binaries. Install and sign in to the native agent separately:
`codex login` or `grok login`, using its own supported account.

| Computer | Archive target | Launcher |
| --- | --- | --- |
| macOS Apple Silicon | `aarch64-apple-darwin` | `Start Graffalo.command` |
| macOS Intel | `x86_64-apple-darwin` | `Start Graffalo.command` |
| Linux x64 (glibc 2.35+) | `x86_64-unknown-linux-gnu` | `start-graffalo.sh` |
| Linux ARM64 (glibc 2.35+) | `aarch64-unknown-linux-gnu` | `start-graffalo.sh` |
| Windows x64 | `x86_64-pc-windows-msvc` | `Start Graffalo.cmd` |

The launcher starts the companion for **https://graffalo.io** and shows a
session pairing code. Keep its terminal open. In a Graffalo build containing the
experimental **Chat** panel, paste the code and click **Pair companion**. The
hosted editor must have this integration deployed; installing the companion alone
does not add Chat to an older Graffalo deployment.

Start the companion from a terminal:

```sh
./graffalo-agent-bridge
```

The default editor is `https://graffalo.io`. Use `--origin HTTPS_ORIGIN` to connect
a different trusted editor. On Windows use `graffalo-agent-bridge.exe`. Only the
exact configured origin is allowed; no paths, trailing slash, or wildcards. One origin per running instance.
Port `43781` is the default; use `--port 43782` and match it in Graffalo if needed.
Stop with **Ctrl+C**. Restarting creates a new pairing code; codes expire after six
hours and are never saved by the bridge.

Your browser may request local-network permission. Some browsers or enterprise
policies block a hosted page contacting the companion even after pairing. Do not
expose the companion on the public network to work around this.

Native agents must be discoverable on the launcher's `PATH`. On Windows this alpha
finds native `.exe` executables only; npm-only `.cmd` wrappers are not supported.
On Unix Stop terminates the agent process group. On Windows it terminates the
direct native child; descendant cleanup needs further validation.

## Verify downloads

Each release includes `SHA256SUMS.txt`. Compare your archive's digest with its
entry using `shasum -a 256 ARCHIVE` (macOS), `sha256sum ARCHIVE` (Linux), or
`Get-FileHash ARCHIVE -Algorithm SHA256` (PowerShell). Checksums detect corruption;
they are not platform signing or independent provenance verification.

Every archive includes this README, the MIT license, dependency notices, and a
launcher. `--version` prints the package and wire versions; `--licenses` prints
license texts without starting a server. No automatic updates or background
installation are performed.

## What gets shared

Graffalo sends your current message, selected canvas/shape context, editing
contract, and a bounded recent conversation to the local agent. The native agent
then uses its provider, normal account permissions, billing, and usage limits.
This is not a way to embed the consumer ChatGPT or Grok.com website or bypass a
subscription's rules. The companion does not ship either agent.

Replies stream back as text. Diagram operations are **proposals**; the Graffalo
editor validates scope and presents a preview. Clicking **Apply** makes one
undoable change. The bridge alone never writes a Graffalo document and never
connects to Graffalo's production database.

The bridge has no telemetry, database, environment file, or persistent chat store.
It does not read provider credential files itself. Native agents manage their own
credentials and may retain their own logs/history according to their settings.
Treat the temporary pairing code as a secret while it is valid.

## Boundaries

- Accepts connections only from this computer; checks exact Origin, Host, and a random session code.
- API-key environment variables are removed from native child environments.
  Codex must report a ChatGPT login; Grok Build must support cached native login.
- Uses a temporary empty workspace, asks native agents to disable unrelated tools,
  and declines permission/tool-service requests. These controls rely partly on
  the installed agent; they are not an OS sandbox or a guarantee against a
  compromised agent/browser extension.
- One active turn, bounded request/context/output sizes, ten-minute turn deadline.
- Only connect sites you trust. An authorized editor can send model requests
  through your account, consuming its normal usage allowance.

See [wire protocol](docs/PROTOCOL.md), [security reporting](SECURITY.md), and
[release process](docs/RELEASING.md).

## Build and test

Requires Rust 1.98.0 (pinned in `rust-toolchain.toml`) and Python 3 for Unix protocol
fixtures and release scripts.

```sh
cargo test --locked
cargo fmt --check
cargo clippy --locked --all-targets -- -D warnings
python3 scripts/notices.py --check
python3 scripts/publication_check.py
cargo build --locked --release
cargo run --locked
```

Tests use synthetic diagrams and fake protocol peers. They never sign in, read
provider credentials, or send model requests. Live checks should be performed
separately with the user's explicit participation.

## Repository scope and licensing

Only this bridge is MIT-licensed, copyright Mriya Research LLC. Graffalo's editor,
backend, account/billing code, document data, assets, and application history are
not part of this repository or license grant. Names of providers identify
compatibility; this project is not an official OpenAI or xAI product.

GitHub is the public publication upstream. A separate Origin inbound mirror tracks
this repository; Graffalo's own Origin repositories remain separate. See
[repository synchronization](docs/REPOSITORIES.md).
