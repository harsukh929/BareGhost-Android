# Build host requirements

Bare's current source build guide requires:
- x86-64 Ubuntu 22.04 container (Docker)
- at least 32 GB RAM allocated to Docker
- about 100 GB free disk (Chromium checkout alone about 50 GB)
- Android ARM64 device for validation

The process fetches Chromium at the pinned commit, applies the ordered Bare patch series, installs Android build dependencies, generates GN files and runs `autoninja -C out/Bare chrome_public_apk`.

## Cloud build options (checked 2026-11-04)

The user's repository is public, so standard GitHub-hosted runners are available without a local Linux machine. However, GitHub documents the public-repository standard Linux runner as 4 CPU, 16 GB RAM and 14 GB SSD. That is below Bare's documented build requirements and cannot hold the Chromium checkout/build.

GitHub Larger Runners include an Ubuntu x64 option with 8 CPU, 32 GB RAM and 300 GB SSD, which is the smallest documented general-purpose size that matches the stated RAM/disk floor. GitHub says Larger Runners are available to GitHub Team and GitHub Enterprise Cloud customers; a valid billing method and a nonzero Actions spending limit are also required. This is a cloud option, not a free standard-runner capability. Do not switch a workflow to a paid runner label until the account has explicitly configured and authorized that runner.

References:
- https://docs.github.com/en/actions/reference/runners/github-hosted-runners
- https://docs.github.com/en/actions/reference/runners/larger-runners
- https://docs.github.com/en/actions/how-tos/write-workflows/choose-where-workflows-run/choose-the-runner-for-a-job

## Current workspace limitation

The present ChatGPT working environment previously measured about 6 GB RAM and 30 GB free disk, with Docker and Gradle absent. It cannot perform this Chromium build. The user's own computer does not need to be a Linux build machine if an appropriately sized cloud runner is available and configured.

A typical hosted CI runner must not be assumed to have enough disk or RAM. Do not try to squeeze the full Chromium build onto the standard 14 GB runner or claim that a successful policy-test workflow built the browser.

Reference: https://github.com/BareBrowser/bare-browser/blob/main/docs/build-from-source.md
