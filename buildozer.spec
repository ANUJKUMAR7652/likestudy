name: Build APK with Buildozer

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

# Isse Node.js wali warning band ho jayegi
env:
  FORCE_JAVASCRIPT_ACTIONS_TO_NODE24: true

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      # 🚀 Yeh hai asli "Brahmastra". Isme dependencies install karne ka jhanjhat hi nahi hai.
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
          path: ${{ steps.buildozer.outputs.filename }}
