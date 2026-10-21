# Wire protocol 1

All endpoints require `Origin` matching the configured editor origin and `Host`
matching `127.0.0.1:PORT`. Requests other than OPTIONS also require
`X-Graffalo-Pairing: SESSION_CODE`. Pairing is ephemeral and lasts at most six
hours. Cookies are not used. Responses carry `Cache-Control: no-store`.

- `GET /status`: name, semantic package `version`, integer `protocolVersion`,
  and `providers: [{id: "codex" | "grok", installed: boolean}]`.
  Installed means executable discovery only, not confirmed sign-in.
- `POST /runs`: `{id: UUID, provider, prompt, context: object, contract: object,
  history?: [{role: "user" | "assistant", text}]}`. Returns 202 `{id}`.
- `GET /runs/ID`: `{status, output, reply, error}`. Status is starting, running,
  completed, cancelled, or error. `reply` is `{message, operations, warning?}`.
  Polling supplies incremental output; this is not SSE.
- `DELETE /runs/ID`: requests cancellation, returns 204. Poll until terminal state
  if confirmation is needed. Completed runs are kept in memory in a bounded cache.
- `OPTIONS`: exact-origin preflight, including private-network response header.
  Browser support/policy is independent of this header.

Limits: 2 MB body, 1 MB context, 32 KB contract, 16 KB prompt, 12 history entries
with 32 KB each, 512 KB output, 100 proposed operations, one active turn, ten-minute
execution timeout. Length limits are UTF-8 byte counts unless otherwise noted.

The editor owns the operation contract and validates all output before Apply.
The companion never accepts executable names, arbitrary commands, or file paths
from browser requests. Providers are a fixed allowlist. Unknown request fields are
rejected. Authentication/protocol errors are reduced to generic messages.

Clients must check `protocolVersion === 1` before sending diagram data. Protocol
changes that break clients increment this integer; compatible additions do not.
Package releases follow SemVer independently. The Graffalo editor should link to
Releases when the companion is missing or incompatible.
