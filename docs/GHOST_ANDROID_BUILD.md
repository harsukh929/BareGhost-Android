# Ghost Android build source discovery

## Finding (checked 2026-11-04)

Ghost Downloader 3's public `main` tree contains Android-specific Python adapters and a platform shim:
- `app/platform/android.py`
- `features/*/android.py`
- `tests/test_android.py` and `tests/import_android_packs.py`

The upstream README describes Android 9+ on `arm64-v8a`, and the latest release observed during this audit is `v4.4.6`.

However, the Android Gradle host project is not committed in the public Ghost repository. Its own `.github/workflows/build.yml` checks out a separate repository, `XiaoYouChR/Ghost-Downloader-Android`, into the `android/` directory for Android build jobs. The workflow then builds native dependencies and runs `./gradlew :app:assembleRelease` (or debug).

A direct GitHub API lookup of `XiaoYouChR/Ghost-Downloader-Android` returned HTTP 404 in this audit. This can mean the repository is private, unavailable to this connection, or otherwise not publicly accessible; it does not prove that the repository does not exist.

## Consequence for BareGhost

The Android host/runtime is not absent from the upstream build design; it is maintained separately and is fetched by the upstream workflow using the `ANDROID_REPO_TOKEN` secret. BareGhost cannot legally or technically reproduce that build by copying only the public Ghost repository. We need authorized access to that separate Android source, or a documented public API/runtime distribution from its maintainers.

Do not substitute the desktop Qt application, embed the upstream APK as if it were a library, or invent missing Gradle files. Keep the current bridge contract as a boundary until a real Android host/runtime is available.

## What can be reused now

- Public Android-specific feature-pack adapters and platform shim, after auditing dependencies and behavior.
- Public build workflow as evidence of the upstream build sequence and native dependency requirements.
- Public release metadata for version tracking only; a release APK is not a reusable library.

## Remaining gates

1. Obtain authorized source access or a documented supported Android integration interface.
2. Audit the Android Gradle project, Chaquopy/Python runtime configuration, native libraries, permissions, foreground service, and storage implementation.
3. Build and test the Ghost Android runtime independently on ARM64.
4. Integrate its supported engine API behind BareGhost's typed bridge.
5. Build Bare Chromium separately on a suitable x86-64 Linux host, then package/test the combined app.

DRM-protected media remains unavailable. No Widevine key extraction, decryption, or DRM bypass is part of this project.
