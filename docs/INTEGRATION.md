# Integration contract

## Component boundary
1. **Browser:** Bare Chromium patch series, built as its own Android browser binary/package initially.
2. **Discovery:** user-initiated media probe. Only explicit, supported media metadata enters the bridge.
3. **Bridge:** typed request containing page URL, selected media URL/format ID, title, and explicitly authorized headers. Incognito sessions do not forward cookies by default.
4. **Engine runtime:** Android-compatible Ghost host/runtime. Do not embed the upstream APK or assume desktop Qt code is reusable.
5. **UI:** small download affordance in the player; quality list appears only after a successful probe.
6. **Background work:** Android foreground service, notification and SAF/MediaStore storage flow.

## Download UI states
- `UNKNOWN`: no reliable media source; no download option.
- `PROBING`: small progress state.
- `FORMATS_FOUND`: only real extractor formats with safe source URLs.
- `SOURCE_ONLY`: one generic Download action only for a direct HTTP(S) URL.
- `UNAVAILABLE`: DRM-protected, inaccessible or unsupported; no download action.

Never infer 1080p/4K from player dimensions. Never decrypt or bypass Widevine/other DRM. Do not defeat paywalls, access controls or anti-bot controls. Treat page URLs, metadata and request headers as untrusted input. Protocol engines such as FTP/BitTorrent require their own explicit typed paths; they must not be smuggled through the media HTTP(S) URL bridge.

Kotlin interfaces define contracts only. Ghost engine adapters and Android host integration still need implementation against a pinned upstream API.
