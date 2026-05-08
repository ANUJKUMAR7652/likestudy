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
requirements = python3, kivy==2.3.0, kivymd, pillow, audiostream

# File manager aur quiz ke liye storage permissions
android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE

# Screen orientation (Phone ke hisaab se portrait)
orientation = portrait

# Android API Target
android.api = 33
android.minapi = 21

[buildozer]
# Log level
log_level = 2
warn_on_root = 1
