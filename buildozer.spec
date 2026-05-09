name: Build APK with Buildozer

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    # 22.04 sabse stable hai Buildozer ke liye
    runs-on: ubuntu-22.04

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      # 🚀 TURBO ENGINE (Fresh Start ke liye ise pehli baar chalne dein)
      - name: Cache Buildozer data
        uses: actions/cache@v4
        with:
          path: .buildozer
          key: ${{ runner.os }}-buildozer-${{ hashFiles('buildozer.spec') }}
          restore-keys: |
            ${{ runner.os }}-buildozer-

      - name: Install dependencies
        run: |
          sudo apt-get update
          # Maine yahan 'libunwind-dev' add kar diya hai jo error de raha tha
          sudo apt-get install -y python3-pip build-essential git python3 python3-dev ffmpeg libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev libportmidi-dev libswscale-dev libavformat-dev libavcodec-dev zlib1g-dev libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev libunwind-dev
          pip install --upgrade pip
          pip install buildozer cython==0.29.33 kivy

      - name: Build APK with Buildozer
        run: |
          buildozer android debug || buildozer android debug
        env:
          BUILDOZER_ALLOW_ORG_NAME_AS_PROJECT_NAME: 1

      - name: Upload APK
        uses: actions/upload-artifact@v4
        with:
          name: StudyLike-PRO-APK
          path: bin/*.apk
