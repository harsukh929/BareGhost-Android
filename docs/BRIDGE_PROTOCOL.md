# Browser-to-downloader bridge protocol v1

## Intended user experience

A user taps a normal file/download link or the browser's download control in Bare. Bare forwards the browser's native download-start event directly to the in-process downloader coordinator. The coordinator calls the injected Ghost-backed `DownloaderHost.enqueue()` method. No external app launch, link copy, or manual paste is part of the intended flow.

## Direct-download path

`BrowserDownloadCoordinator.onBrowserDownload()` accepts the original HTTP(S) URL, source page URL, suggested filename, request headers and Incognito state. It constructs a validated `DownloadRequest`, then immediately submits it to `DownloaderHost.enqueue()` in the supplied coroutine scope. Its listener reports the Ghost task ID on success or a failure reason.

The Bare integration point is Chromium's native download-start callback (the exact callback signature depends on the pinned Bare/Chromium revision). Wire that callback to `onBrowserDownload()`; do not intercept arbitrary page JavaScript clicks or claim every website's custom button is a browser download event. For media detected by an extractor, pass the selected actual format through the separate probe/format flow rather than fabricating a filename or quality.

## Required safeguards

- `pageUrl` and `mediaUrl` must be absolute HTTP(S) URLs with a host.
- Do not send `Cookie` or `Cookie2` unless the user explicitly enabled session-cookie forwarding. The direct-download coordinator currently defaults to no cookie forwarding.
- Incognito requests always set `isIncognito=true` and `allowSessionCookies=false`; cookies are rejected.
- Header names/values containing CR or LF are rejected.
- Format identifiers are opaque extractor IDs; never invent them.
- This protocol does not grant permission to download restricted, paywalled or DRM-protected media.
- The host must validate URLs and permissions again before enqueueing.
- The coordinator is intended for user-initiated browser download events. It is not a mechanism for bypassing website access controls or DRM.

## Current implementation status

- Added `BrowserDownloadCoordinator.kt`: direct in-process handoff from Bare's native download callback to `DownloaderHost.enqueue()`, with success/failure callbacks.
- Existing `DownloadRequest.kt` validates URL, headers, title and Incognito cookie rules.
- The actual Ghost Android host implementation is still not connected. `DownloaderHost` remains an interface until the separately maintained Ghost Android host source/API is available and integrated.
- Bare's native callback has not yet been wired because this repository still does not contain the actual Bare Chromium Android application project.
- Therefore this is implemented integration code and a defined connection point, not a working end-to-end APK yet.
