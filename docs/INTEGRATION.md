# Integration contract

## Proposed component boundary
1. **Browser process:** Bare Chromium patch series, built as its own Android browser binary/package initially.
2. **Browser-to-downloader handoff:** a narrow Android bridge passing page URL, selected media URL/format ID, page title and explicitly authorized request headers.
3. **Ghost engine runtime:** Android-compatible Ghost host/runtime; use its own task/session model rather than copying Qt desktop UI code.
4. **UI:** small download affordance inside the player; quality list is populated only by a completed probe.
5. **Storage and background work:** Android foreground service / SAF / MediaStore, with user-visible notifications and persisted task state.

## Current verified facts
- Bare is a Chromium patch series, not a Gradle dependency.
- Ghost publishes an Android ARM64 APK and has Android adapter modules, but the public source tree inspected is missing the Android host project referenced by its own Android tests.
- Therefore the next blocking dependency is the Ghost Android host/runtime source or a documented stable API. The existing APK cannot simply be merged into Bare.

## Download UI states
- `UNKNOWN`: no reliable media source; no download option.
- `PROBING`: show a small progress state.
- `FORMATS_FOUND`: show only real extractor formats.
- `SOURCE_ONLY`: show one generic Download action only when a permitted direct URL exists.
- `UNAVAILABLE`: DRM-protected, inaccessible or unsupported; no download action.

Never infer 1080p/4K from player dimensions. Never decrypt or bypass Widevine/other DRM. Do not defeat paywalls, access controls or anti-bot controls. Forward cookies/headers only for user-authorized sessions; never from Incognito by default. Treat page URLs and metadata as untrusted.

Kotlin files in `app/src/main/kotlin` are contracts, not a finished engine implementation.
