# SPDX-License-Identifier: Zlib
# kigo/platform_info.py

import sys
import os
import platform as _platform


# -------------------------------------------------
# Mobile platforms
# -------------------------------------------------

def is_android() -> bool:
    """True if running on Android (ARC++ or native)."""
    return hasattr(sys, "getandroidapilevel")


def android_api_level():
    """Return Android API level or None."""
    if hasattr(sys, "getandroidapilevel"):
        return sys.getandroidapilevel()
    return None


def is_ios() -> bool:
    """True if running on iOS (future-ready)."""
    return sys.platform == "ios"


# -------------------------------------------------
# Desktop OS detection
# -------------------------------------------------

def is_windows() -> bool:
    return sys.platform.startswith("win")


def is_linux() -> bool:
    return sys.platform.startswith("linux")


def is_macos() -> bool:
    return sys.platform == "darwin"


def is_freebsd() -> bool:
    return sys.platform.startswith("freebsd")


def is_openbsd() -> bool:
    return sys.platform.startswith("openbsd")


def is_sunos() -> bool:
    # Solaris reports as "sunos"
    return sys.platform == "sunos"


# -------------------------------------------------
# ChromeOS detection (Crostini / ARC++)
# -------------------------------------------------

def is_chromeos() -> bool:
    """
    Detect ChromeOS.
    Covers:
    - Linux (Crostini)
    - Android Runtime (ARC++)
    """
    # Crostini exposes this env var
    if "SOMMELIER_VERSION" in os.environ:
        return True

    # Fallback: os-release check
    try:
        with open("/etc/os-release", "r", encoding="utf-8") as f:
            data = f.read().lower()
            if "chromeos" in data or "chromiumos" in data:
                return True
    except Exception:
        pass

    return False


# -------------------------------------------------
# Platform groups
# -------------------------------------------------

def is_mobile() -> bool:
    return is_android() or is_ios()


def is_desktop() -> bool:
    return not is_mobile()


def is_bsd() -> bool:
    return is_freebsd() or is_openbsd()


def is_unix_desktop() -> bool:
    return (
        is_linux()
        or is_macos()
        or is_bsd()
        or is_sunos()
        or is_chromeos()
    )


# -------------------------------------------------
# Window system detection (X11 / Wayland)
# -------------------------------------------------

def window_system() -> str:
    """
    Returns:
        'wayland', 'x11', or 'unknown'
    """
    if os.environ.get("WAYLAND_DISPLAY"):
        return "wayland"
    if os.environ.get("DISPLAY"):
        return "x11"
    return "unknown"


# -------------------------------------------------
# Qt backend decision
# -------------------------------------------------

def qt_backend() -> str:
    """
    Android → PySide6
    Everything else → PyQt6
    """
    if is_android():
        return "pyside"
    return "pyqt"


# -------------------------------------------------
# Human-readable platform name
# -------------------------------------------------

def platform_name() -> str:
    if is_android():
        return "android"
    if is_chromeos():
        return "chromeos"
    if is_ios():
        return "ios"
    if is_windows():
        return "windows"
    if is_macos():
        return "macos"
    if is_linux():
        return "linux"
    if is_freebsd():
        return "freebsd"
    if is_openbsd():
        return "openbsd"
    if is_sunos():
        return "sunos/solaris"
    return _platform.system().lower()


# -------------------------------------------------
# Debug / dev helper
# -------------------------------------------------

def summary() -> dict:
    return {
        "platform": platform_name(),
        "chromeos": is_chromeos(),
        "mobile": is_mobile(),
        "desktop": is_desktop(),
        "window_system": window_system(),
        "qt_backend": qt_backend(),
        "android_api": android_api_level(),
    }
