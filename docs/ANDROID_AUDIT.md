# Upstream Android audit (verified 2026-11-04)

## Bare Browser
- Audited main commit: `e776f77629bb915e0f3df63449f1f993cc1b0648`.
- Release metadata: Bare `2.0.0-beta.6`, Chromium `156.0.8078.73`, Android 10+, ARM64/32-bit ARM, 296 patches.
- Bare is a Chromium patch series, not an embeddable Android library or WebView wrapper.
- The build guide pins Chromium commit `2f9a11097447f226133bc1a31c787291a5eeab98` and requires Docker with at least 32 GB allocated RAM, about 100 GB free disk, an x86-64 Ubuntu 22.04 container, and an ARM64 Android device for testing.
- The build requires fetching Chromium/depot_tools, applying the ordered patch series, adding the signed uBlock Origin CRX, GN configuration, then `autoninja -C out/Bare chrome_public_apk`.
- Bare's extension manager supports Web Store, CRX and unpacked extension flows. Individual desktop extensions may still be incompatible with Android.

## Ghost Downloader 3
- Audited main commit: `256b082166fec444b517dd3f4bb88c55ead1325b`.
- README declares Android 9+ and `arm64-v8a`.
- Android adapters exist for HTTP, FTP, BitTorrent, eD2k, M3U8, yt-dlp, Bilibili, GitHub and HuggingFace.
- The yt-dlp Android adapter is explicitly marked draft. The M3U8 adapter exposes decryption-key fields; BareGhost will not use key extraction or DRM decryption. Its M3U8 support must be limited to streams the user is authorized to access and that are not DRM protected.
- The recursive public `main` tree contains `tests/test_android.py`, which reads `android/app/build.gradle.kts` and `android/app/src/main/python/app/config/cfg.py`; those Android host files are absent from that tree. This prevents a source-level merge of the full Ghost Android host from the inspected public snapshot.
- Ghost's official Android app is not a reusable Android library merely because an APK exists. The missing host source or a documented stable engine API is a hard integration dependency.

## Integration decision
- Keep Bare's Chromium browser build as the browser foundation.
- Do not embed Ghost's APK or copy desktop Qt UI code.
- Build a narrow browser-to-downloader contract, then integrate a verified Android Ghost host/runtime when its source/API is available.
- Keep engine support gated by Android ABI/dependency tests. Treat yt-dlp adapter as draft.

## Local build limitation
The available workspace has no Docker or Gradle and insufficient RAM/disk for Bare's documented Chromium build. No APK has been built or tested here.
