# Browser-to-downloader bridge protocol v1

The browser must send a user-initiated request only after a supported probe. The JSON shape is documented in `integration/download-request.schema.json`.

## Required safeguards
- `pageUrl` and `mediaUrl` must be absolute HTTP(S) URLs with a host.
- Do not send `Cookie` or `Cookie2` unless the user explicitly enabled session-cookie forwarding.
- Incognito requests always set `isIncognito=true` and `allowSessionCookies=false`; cookies are rejected.
- Header names/values containing CR or LF are rejected.
- Format identifiers are opaque extractor IDs; never invent them.
- This protocol does not grant permission to download restricted, paywalled or DRM-protected media.
- The host must validate URLs and permissions again before enqueueing.

## Current status
The Kotlin `DownloadRequest` and `DownloaderHost` are interface/validation scaffolding. There is no connected Android Ghost host implementation in this repository yet.
