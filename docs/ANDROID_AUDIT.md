# Upstream Android audit (verified 2026-11-04)

## Bare Browser
- Audited main commit: `e776f77629bb915e0f3df63449f1f993cc1b0648`.
- Release metadata: Bare `2.0.0-beta.6`, Chromium `156.0.8078.73`, Android 10+, ARM64/32-bit ARM, 296 patches.
- Bare is a Chromium patch series, not an embeddable Android library or WebView wrapper.
- The inspected build guide requires Docker with at least 32 GB allocated RAM, about 100 GB free disk, an x86-64 Ubuntu 22.04 container, and an ARM64 Android device for testing.
- The build fetches Chromium/depot_tools, applies the ordered patch series, adds the signed uBlock Origin CRX, configures GN, then builds `chrome_public_apk`.
- Bare's extension manager supports Web Store, CRX and unpacked extension flows. Individual desktop extensions may still be incompatible with Android.

## Ghost Downloader 3
- Audited public main commit: `256b082166fec444b517dd3f4bb88c55ead1325b`; latest release observed: `v4.4.6`.
- README declares Android 9+ and `arm64-v8a`.
- The public tree contains Android adapters for HTTP, FTP, BitTorrent, eD2k, M3U8, yt-dlp, Bilibili, GitHub and HuggingFace, plus `app/platform/android.py`.
- The yt-dlp Android adapter remains draft. The M3U8 adapter contains decryption-related fields; BareGhost will not use key extraction or DRM decryption. M3U8 recording/downloading must be limited to streams the user is authorized to access and that are not DRM protected.
- The Android Gradle host is not in the public main tree. Ghost's own `.github/workflows/build.yml` checks out `XiaoYouChR/Ghost-Downloader-Android` into `android/` using the `ANDROID_REPO_TOKEN` secret, then builds native dependencies and runs `./gradlew :app:assembleRelease` or debug.
- A direct GitHub API lookup of that separate repository returned 404 to this connection. It may be private, unavailable to this connection, or otherwise inaccessible; this does not establish that it does not exist.
- The Ghost APK release is not a reusable Android library.

## Integration decision
- Keep Bare's Chromium browser build as the browser foundation.
- Do not embed Ghost's APK or copy desktop Qt UI code.
- Keep the typed browser-to-downloader contract, then connect a verified Android Ghost host/runtime only after authorized source access or a documented stable engine API is available.
- Gate engine support by Android ABI/dependency tests. Do not promise feature packs that have not been built and tested on Android.

## Local build limitation
The available workspace has no Docker or Gradle and insufficient RAM/disk for Bare's documented Chromium build. No APK has been built or tested here.
