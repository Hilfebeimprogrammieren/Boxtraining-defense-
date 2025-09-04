[app]
title = Box-Training
package.name = boxtraining
package.domain = org.example

source.dir = .
source.include_exts = py,png

version = 0.1
requirements = python3, pygame==2.5.2

orientation = landscape
fullscreen = 1

android.api = 33
android.minapi = 21
android.archs = arm64-v8a, armeabi-v7a

# Lizenzen automatisch bestätigen
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 0
