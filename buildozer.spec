[app]
title = StudyLike PRO
package.name = studylikepro
package.domain = org.studylike
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,wav,csv
version = 1.0

# Dependencies (Sound aur Hindi font dono supported hain)

requirements = python3, kivy, kivymd, pillow, urllib3, cython==0.29.33
android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, MANAGE_EXTERNAL_STORAGE
orientation = portrait
android.api = 33
android.minapi = 21
android.accept_sdk_license = True
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1
