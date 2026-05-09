[app]
# App ka naam
title = StudyLike PRO

# Package ka naam (Space nahi hona chahiye)
package.name = studylikepro
package.domain = org.studylike

# Kahan se files uthani hain
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,wav,csv

# App ka version
version = 1.0

# 🚀 Sabse important: Requirements (KivyMD aur baaki cheezein)
requirements = python3, kivy==2.3.0, kivymd, pillow==10.2.0, urllib3

# 🛑 File manager ke liye MANAGE_EXTERNAL_STORAGE bohot zaroori hai
android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, MANAGE_EXTERNAL_STORAGE

# Screen orientation (Phone ke hisaab se portrait)
orientation = portrait

# Android API Target
android.api = 34
android.minapi = 21

# 🛑 YAHAN HAI SABSE ZAROORI LINE
android.accept_sdk_license = True

[buildozer]
# Log level
log_level = 2
warn_on_root = 1
