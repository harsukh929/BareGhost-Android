# Ghost Downloader Android adapter matrix

| Pack | Adapter | Exposed functions |
|---|---|---|
| HTTP | Yes | URL, headers, client profile, User-Agent, subworkers |
| FTP | Yes | subworkers |
| BitTorrent | Yes | peer/seeding status, tracker controls |
| eD2k | Yes | network state, stop, server/node controls |
| M3U8 | Yes | stream selection, headers, live recording limit |
| yt-dlp | Yes, draft | format/playlist probe, quality/audio, subtitles, trim |
| Bilibili | Yes | quality/audio, QR login, subtitles, clip edits |
| GitHub | Yes | HTTP options and mirror probe |
| HuggingFace | Yes | mirror probe and token URL |

These adapters are source evidence, not proof of a working combined APK. The Android host project and native/runtime dependency packaging remain blockers.