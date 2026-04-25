# kigo/platform.py
import sys
import os
import platform as _platform


class PlatformInfo:
    def __init__(self):
        self.sys_platform = sys.platform
        self.system = _platform.system().lower()

        # ---- OS ----
        self.is_windows = self.sys_platform.startswith("win")
        self.is_macos = self.system == "darwin"
        self.is_linux = self.sys_platform.startswith("linux")
        self.is_freebsd = self.sys_platform.startswith("freebsd")
        self.is_openbsd = self.sys_platform.startswith("openbsd")
        self.is_sunos = self.sys_platform == "sunos"
        self.is_android = hasattr(sys, "getandroidapilevel")
        self.is_ios = self.sys_platform == "ios"

        # ---- Form factor ----
        self.is_mobile = self.is_android or self.is_ios
        self.is_desktop = not self.is_mobile

        # ---- Window system (desktop Unix) ----
        self.window_system = self._detect_window_system()

        # ---- Qt backend (runtime observation) ----
        self.qt_backend = self._detect_qt_backend()

    def _detect_window_system(self):
        # Wayland advertises WAYLAND_DISPLAY
        if os.environ.get("WAYLAND_DISPLAY"):
            return "wayland"
        # X11/XWayland uses DISPLAY
        if os.environ.get("DISPLAY"):
            return "x11"
        return "unknown"

    def _detect_qt_backend(self):
        # Android must use PySide6
        if self.is_android:
            return "pyside"
        return "pyqt"

    def summary(self):
        return {
            "os": self.system or self.sys_platform,
            "window_system": self.window_system,
            "qt_backend": self.qt_backend,
            "mobile": self.is_mobile,
        }


# Singleton (read‑only)
platform = PlatformInfo()