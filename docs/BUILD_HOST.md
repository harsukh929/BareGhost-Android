# Build host requirements

Bare's current source build guide requires:
- x86-64 Ubuntu 22.04 container (Docker)
- at least 32 GB RAM allocated to Docker
- about 100 GB free disk (Chromium checkout alone about 50 GB)
- Android ARM64 device for validation

The process fetches Chromium at the pinned commit, applies the ordered Bare patch series, installs Android build dependencies, generates GN files and runs `autoninja -C out/Bare chrome_public_apk`.

The present ChatGPT working environment previously measured about 6 GB RAM and 30 GB free disk, with Docker and Gradle absent. It cannot perform this Chromium build. A properly provisioned self-hosted Linux runner or dedicated build machine is required. A typical hosted CI runner should not be assumed to have enough disk or RAM.

Reference: https://github.com/BareBrowser/bare-browser/blob/main/docs/build-from-source.md
