# Integration contract

1. Browser: Bare Chromium build and extension runtime.
2. Media discovery: page/media observation and user-initiated probing.
3. Resolver: yt-dlp metadata and supported manifest parsers.
4. Download service: Ghost Android-capable engines and background tasks.
5. Settings: Android-native UI for settings actually supported on Android.
6. Storage: Android Storage Access Framework / MediaStore.

UI states: UNKNOWN (no source), PROBING, FORMATS_FOUND (actual extractor formats only), SOURCE_ONLY (one generic Download action only with a permitted direct URL), UNAVAILABLE (DRM, inaccessible or unsupported; no download action).

Never infer 1080p/4K from player dimensions. Never decrypt or bypass Widevine/other DRM. Do not defeat paywalls, access controls or anti-bot controls. Forward cookies only for user-authorized sessions and never from Incognito by default. Treat page URLs and metadata as untrusted.

The Kotlin interfaces define contracts only. Ghost engine adapters and yt-dlp invocation still need implementation against pinned upstream APIs.