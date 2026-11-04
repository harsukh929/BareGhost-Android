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

The public Ghost source contains an Aria2-compatible JSON-RPC/WebSocket listener. The inspected implementation establishes:

- `Engine.start()` starts the RPC listener; `Engine.stop()` stops it.
- RPC is disabled by default (`isAria2RpcEnabled = false`).
- The configured default port is `16800`; allowed ports are 1024–65535.
- The listener binds IPv4 loopback `127.0.0.1` and attempts IPv6 loopback `::1`.
- HTTP POST and WebSocket requests use the `/jsonrpc` path.
- The service implements a limited Aria2-compatible method set, including `aria2.getVersion`, `aria2.getGlobalOption`, and `aria2.addUri`.
- The RPC token is configurable, but its default is the empty string. The inspected service checks the supplied token only when a non-empty configured secret exists. Therefore, enabling RPC without setting a strong token leaves the local listener without token authentication.
- Upstream tests include an Android engine fixture and exercise IPv4/IPv6 loopback requests, but that does not prove the separate Android host's background lifecycle, port/token discovery, or integration stability for BareGhost.

A separate Android app process on the same device can generally reach a loopback listener through `127.0.0.1:<port>`, because Android apps normally share the device network namespace. This makes a two-app proof-of-concept plausible, provided the Ghost Android app is installed and running, RPC is enabled, a strong token is configured, and the port is known.

This remains only a **two-app bridge**, not the requested single-app integration. It does not launch or package Ghost's Python runtime, native dependencies, Android lifecycle, storage implementation, or foreground service inside BareGhost. The public `ghd` CLI is installed from within the running desktop application; it is not evidence of a standalone Android engine binary.

Security requirements for any prototype:
1. Never enable Ghost RPC with an empty token.
2. Generate and store a high-entropy token locally; do not expose it in logs, URLs, exported settings, or browser page JavaScript.
3. Restrict the client to loopback and validate the expected listener/port before sending tasks.
4. Do not forward browser cookies or authorization headers by default; require explicit per-download consent for session-bound requests.
5. Treat RPC as an optional compatibility experiment only; it does not change the missing Android host source blocker.

Therefore BareGhost may implement an Aria2-compatible client adapter as a separately testable experiment, but must not present it as an embedded Ghost engine or as completion of the single-app requirement. The authorized Android host source or a documented supported Android runtime/API is still required for the intended product.
