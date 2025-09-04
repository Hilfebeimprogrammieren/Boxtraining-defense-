[app]
title = Boxtraining Defense
package.name = boxtrainingdefense
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3, pygame==2.5.2
orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 0

[android]
# Minimal Android API
android.api = 33
# Minimal API for devices
android.minapi = 21
# Java Version
android.sdk_path = ~/.buildozer/android/platform/android-sdk
android.ndk_path = ~/.buildozer/android/platform/android-ndk-r25b
