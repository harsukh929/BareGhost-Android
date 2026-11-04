# Upstream integration checklist

## Bare
- [ ] Pin Bare commit and Chromium revision.
- [ ] Follow build prerequisites and patch order.
- [ ] Preserve extension workflows where supported.
- [ ] Test extension compatibility on target Android device.
- [ ] Preserve notices and bundled extension licenses.

## Ghost
- [ ] Pin Ghost commit and audit Android adapters.
- [ ] Integrate Android task engine and background service.
- [ ] Validate HTTP, BitTorrent, FTP, M3U8, DASH, eD2k, yt-dlp, GitHub and HuggingFace dependencies on ARM64.
- [ ] Port supported settings only.
- [ ] Test pause/resume, retries, headers, proxy, speed limits and persistence.

## Combined app
- [ ] Implement media probe bridge and in-player button.
- [ ] Use actual formats only; generic fallback only for a direct URL.
- [ ] No DRM download/decryption.
- [ ] Test background operation, process death and storage permissions.
- [ ] Build, sign and test ARM64 APK on Android 16.
- [ ] Publish source and license notices as required.