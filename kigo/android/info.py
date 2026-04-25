# kigo/android/info.py
from kigo.android.platform import is_android, android_api_level

def device_info():
    if not is_android():
        return None

    return {
        "api_level": android_api_level(),
        "platform": "android",
    }