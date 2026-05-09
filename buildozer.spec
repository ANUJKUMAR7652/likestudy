name: Build APK with Buildozer

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      # Yeh step seedha Docker container bulayega jisme sab kuch pehle se install hai!
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
          # Yeh naya code khud dhundh lega ki APK kahan bana hai
          path: ${{ steps.buildozer.outputs.filename }}
