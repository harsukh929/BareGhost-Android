# Ghost Android compatibility notes

Checked 2026-11-04 against the public Ghost Downloader 3 source, developer documentation, release metadata and build workflow.

## What the public evidence establishes

- Ghost publishes an ARM64 Android APK and documents Android support.
- Its own build workflow fetches a separate Android host project before building the APK. BareGhost does not currently have that host source or a supported API contract.
- Android-specific feature adapters in the public repository are not sufficient on their own to prove every engine works in a new host app.
- Ghost's developer documentation states that `bittorrent_pack`, `ed2k_pack`, and `jack_yao` are stripped from Android builds.
- The public developer documentation says the Feature Pack API is still stabilizing; the roadmap still lists making it public as unfinished.
- M3U8 delegates to external `N_m3u8DL-RE`; eD2k uses an external runtime; BitTorrent uses libtorrent. Their presence in the desktop project does not prove Android ARM64 binaries are packaged.

## Known upstream Android issues to account for

These are user-reported issues in Ghost's tracker, not claims that every device/version is affected:

- Magnet/torrent parsing has had an Android report of `No parser matched`.
- eD2k has had Android crash reports.
- Browser-extension panels and recording overlays have had touch usability problems on Android.
- Custom download-folder handling has had secondary-user path issues.
- Android YouTube quality selection has had a UI state bug.
- Android download task creation has had permission-related silent failure reports.

The issue tracker is living data; verify current status and exact versions before using any item as a release blocker.

## BareGhost integration requirements

1. Do not claim protocol support solely because an adapter file exists.
2. Do not mark BitTorrent or eD2k as supported based on Ghost's public Android adapter files; upstream strips those packs from its Android build.
3. Each engine must pass an ARM64 build/import test and a real-device download test.
4. M3U8, eD2k and BitTorrent require explicit verification of their external/native runtime dependencies.
5. The UI must handle Android touch, orientation, permission denial, background execution and SAF/MediaStore destinations.
6. Browser extension integration must be tested in Bare's Android extension runtime, not assumed from desktop extension support.
7. Keep unsupported or unverified engines hidden/disabled in the product capability list.
8. Preserve the media bridge's strict URL, cookie and DRM safeguards.

## Current status

The BareGhost policy and bridge scaffolding is present. A complete Android Ghost host is still unavailable to this workspace. No engine has been integrated or tested in BareGhost, and no APK has been produced.

Sources:
- https://github.com/XiaoYouChR/Ghost-Downloader-3
- https://gd.xychr.com/docs/dev/built-in-packs/
- https://gd.xychr.com/docs/dev/download-engine/
- https://gd.xychr.com/docs/getting-started/install/
