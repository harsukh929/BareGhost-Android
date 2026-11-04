# Ghost Downloader Android adapter and packaging matrix

This matrix separates three things that must not be conflated:
1. a Python adapter exists in Ghost's public source;
2. Ghost's own Android build packages the feature;
3. the feature has been ported, built and tested inside BareGhost.

Only the first item is established for the adapters below. The third has not happened.

| Pack | Public Android adapter evidence | Upstream Android packaging / runtime note | BareGhost status |
|---|---|---|---|
| HTTP / HTTPS | Yes | Core HTTP path; must be wired to Android storage and background execution | Not integrated |
| FTP | Yes | Android adapter exists; verify dependencies and real transfer behavior | Not integrated |
| BitTorrent / Magnet | Yes | Official Ghost Android build script strips `bittorrent_pack` | Not available until separately ported and tested |
| eD2k | Yes | Official Ghost Android build script strips `ed2k_pack`; external Kelpie runtime is involved | Not available until separately ported and tested |
| M3U8 / HLS | Yes | Uses external `N_m3u8DL-RE`; package/runtime and non-DRM behavior need ARM64 verification | Not integrated |
| yt-dlp | Yes, draft adapter | Requires a compatible Android Python/runtime and packaged dependencies | Not integrated; draft |
| Bilibili | Yes | QR/login, quality and subtitles need Android UI/session testing | Not integrated |
| GitHub | Yes | HTTP-based task path; verify mirrors and auth handling | Not integrated |
| HuggingFace | Yes | HTTP-based task path; verify mirrors and token handling | Not integrated |

## Important upstream limitation

Ghost's developer documentation says `bittorrent_pack`, `ed2k_pack`, and `jack_yao` are stripped from Android builds. The pack documentation also identifies external runtimes for eD2k, M3U8, and BitTorrent. Therefore, the presence of an Android adapter file must not be presented as proof that the official Android APK includes that engine.

Sources:
- https://gd.xychr.com/docs/dev/built-in-packs/
- https://gd.xychr.com/docs/dev/download-engine/

The public Ghost repository's plugin API is still described as stabilizing and is listed on its roadmap as not yet public. BareGhost must not assume a stable third-party plugin contract.

## Release gate

Expose an engine only after its implementation passes:
- ARM64 build/import checks;
- dependency and native-library packaging checks;
- a real transfer/probe test on Android 10+;
- pause/resume and process-death tests where supported;
- Android SAF/MediaStore destination tests;
- permission-denial and background-execution tests.

DRM-protected streams remain unavailable. No Widevine key extraction, decryption, or DRM bypass is permitted.
