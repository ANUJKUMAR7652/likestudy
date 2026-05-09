name: Build APK with Buildozer

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-22.04

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      # Cache ka naam badal diya (v2) taaki fresh start ho
      - name: Cache Buildozer data
        uses: actions/cache@v4
        with:
          path: .buildozer
          key: ${{ runner.os }}-buildozer-v2-${{ hashFiles('buildozer.spec') }}

      - name: Install dependencies
        run: |
          sudo apt-get update
          # Sirf Android build ke liye zaroori tools (Bina kisi video/audio conflict ke)
          sudo apt-get install -y zip unzip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev openjdk-17-jdk
          pip install --upgrade pip
          pip install buildozer cython==0.29.33 kivy

      - name: Build APK with Buildozer
        run: |
          buildozer android debug
        env:
          BUILDOZER_ALLOW_ORG_NAME_AS_PROJECT_NAME: 1

      - name: Upload APK
        uses: actions/upload-artifact@v4
        with:
          name: StudyLike-PRO-APK
          path: bin/*.apk
