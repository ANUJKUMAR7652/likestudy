[app]
title = StudyLike PRO
package.name = studylikepro
package.domain = org.studylike
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,wav,csv
version = 1.0

# 🚀 Requirements
requirements = python3, kivy==2.3.0, kivymd, pillow==10.2.0, urllib3

# 🛑 Permissions & Settings (Permissions are now fixed)
android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, MANAGE_EXTERNAL_STORAGE
orientation = portrait
android.api = 33
android.minapi = 21
android.accept_sdk_license = True
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1
