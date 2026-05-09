[app]
# App ka naam
title = StudyLike PRO

# Package ka naam (Unique hona chahiye)
package.name = studylikepro
package.domain = org.studylike

# Kahan se files uthani hain
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,wav,csv
source.include_patterns = assets/*,images/*.png

# App ka version
version = 1.0

# 🚀 Requirements: Inhe dhyan se dekhiye
requirements = python3, kivy==2.3.0, kivymd, pillow==10.2.0, urllib3

# File manager aur quiz ke liye storage permissions
android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, MANAGE_EXTERNAL_STORAGE

# Screen orientation (Hamesha portrait rahega)
orientation = portrait

# Android API Settings
android.api = 33
android.minapi = 21
android.ndk = 25b
android.skip_update = False
android.accept_sdk_license = True

# Status bar ko dikhane ke liye
fullscreen = 0

[buildozer]
# Log level 2 taaki error saaf dikhe
log_level = 2
warn_on_root = 1
