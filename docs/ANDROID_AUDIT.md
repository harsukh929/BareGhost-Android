# Upstream Android audit (2026-11-04)

Ghost Downloader 3 README declares Android 9+ and arm64-v8a, and describes background downloads and live M3U8 recording. Android adapters were found for HTTP, FTP, BitTorrent, eD2k, M3U8, yt-dlp, Bilibili, GitHub and HuggingFace. The yt-dlp Android adapter is marked draft; adapter presence does not prove production readiness.

Bare is a Chromium-for-Android patch series, not a standalone library. The inspected build guide specifies Docker with at least 32 GB allocated RAM and about 100 GB free disk; Chromium source is about 50 GB. The documented build uses an x86-64 Ubuntu 22.04 container.

The public Ghost tree inspected did not expose the Android host project/classes referenced by its Android tests. Native dependencies need Android packaging. A finished combined APK is not available from this starter.