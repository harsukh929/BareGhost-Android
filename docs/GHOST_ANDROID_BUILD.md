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


## Required repository access configuration

The upstream reusable test workflow declares `ANDROID_REPO_TOKEN` as a required workflow secret and uses it to check out `XiaoYouChR/Ghost-Downloader-Android`. The same secret is passed by the upstream release workflow into its test job. This confirms that an ordinary anonymous checkout is not the supported path.

For this project, configure a GitHub Actions repository secret named exactly `ANDROID_REPO_TOKEN` only if the upstream maintainer has granted the account/token read access to that Android host repository:

1. Create a fine-grained personal access token (or other maintainer-approved credential) with read-only Contents access to the Android host repository.
2. In `harsukh929/BareGhost-Android`, open **Settings → Secrets and variables → Actions → New repository secret**.
3. Set the name to `ANDROID_REPO_TOKEN` and paste the token as the secret value.
4. Never commit the token, put it in workflow YAML, or paste it into an issue or chat.

A secret name alone does not grant repository access. If the upstream repository owner has not granted access, ask them for authorized source access or a supported integration package. Do not attempt to work around repository permissions.

Until the authorized host source is available, CI can validate BareGhost's standalone policy and bridge contracts, but cannot validate or build the Ghost Android host. The current CI success must not be interpreted as an Android APK build.

## Aria2 RPC integration audit (2026-11-04)

The public Ghost source does contain an Aria2-compatible JSON-RPC/WebSocket listener. The settings page wires an `aria2RpcListener`, and the listener implementation binds only to loopback addresses (`127.0.0.1` and `::1`). Its tests exercise HTTP JSON-RPC and WebSocket calls, token checks, and `aria2.addUri`.

This is useful as an interface reference, but it is **not by itself an embeddable Android engine**:
- The listener is owned by a running Ghost application/engine instance; it does not launch the engine or package its dependencies.
- The listener binds to loopback, so a separate Android app process cannot assume it can reach it through a normal network endpoint.
- The public CLI `ghd` is installed from within the running desktop application; it is not evidence of a standalone Android service binary.
- The upstream Android Gradle host is still required to package the Python runtime, native dependencies, app lifecycle, storage and background work.

Therefore BareGhost may implement an Aria2-compatible client adapter later, but only after an authorized Ghost Android host/runtime is available and its supported process boundary is verified. Do not treat the RPC claim as resolving the missing Android host source.

