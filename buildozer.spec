name: Build APK with Buildozer

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

# Isse Node.js wali purani warning khatam ho jayegi
env:
  FORCE_JAVASCRIPT_ACTIONS_TO_NODE24: true

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      # 🛠️ OFFICIAL BUILDOZER ACTION (Isme sab pehle se set hai)
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
# (Line 39 ke aas-paas) Permissions for CSV and Storage
android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, MANAGE_EXTERNAL_STORAGE

# (Line 48 ke aas-paas) Screen Orientation Fix
orientation = portrait

# (Line 55 ke aas-paas) Android API Settings
android.api = 33
android.minapi = 21
android.accept_sdk_license = True
