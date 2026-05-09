name: Build APK with Buildozer

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

# Yeh line Node.js wali warning ko hamesha ke liye band kar degi
env:
  FORCE_JAVASCRIPT_ACTIONS_TO_NODE24: true

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      # Yahan humne saare apt-get hata diye aur seedha official machine lagayi hai
      - name: Build with Buildozer
        uses: ArtemSBulgakov/buildozer-action@v1
        id: buildozer
        with:
          command: buildozer android debug
          buildozer_version: master

      - name: Upload APK
        uses: actions/upload-artifact@v4
        with:
          name: StudyLike-PRO-APK
          # Yeh command automatic aapka APK dhundh kar upload kar degi
          path: ${{ steps.buildozer.outputs.filename }}
