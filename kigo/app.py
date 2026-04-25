# SPDX-License-Identifier: Zlib
# kigo/app.py

import sys

from kigo.platform_info import summary as platform_summary
from kigo.logging import JsonLogger
from kigo.qt.backend import QtCore, QtWidgets


class App:
    """
    Base Kigo application class.

    Features:
    - JSON logging (opt-in via `log = "on"`)
    - Cross-platform Qt backend
    - Clean lifecycle hooks
    """

    def __init__(self, *, dev: bool = False):
        # ----------------------------------
        # Detect logging switch
        # ----------------------------------
        enabled = False
        try:
            enabled = globals().get("log") in ("on", True)
        except Exception:
            enabled = False

        self.log = JsonLogger(enabled=enabled)
        self.dev = dev

        if enabled:
            self.log.info("Kigo logging enabled")

        # ----------------------------------
        # Qt application
        # ----------------------------------
        self.qt_app = QtWidgets.QApplication(sys.argv)

        # ----------------------------------
        # Platform info (one-time snapshot)
        # ----------------------------------
        self.platform = platform_summary()

        if enabled:
            self.log.info("Platform detected", **self.platform)

        # ----------------------------------
        # Lifecycle hooks
        # ----------------------------------
        self._started = False

    # --------------------------------------
    # Lifecycle hooks (override these)
    # --------------------------------------

    def on_start(self):
        """Called once after QApplication is ready."""
        pass

    def on_exit(self):
        """Called right before application exits."""
        pass

    # --------------------------------------
    # Internal lifecycle
    # --------------------------------------

    def _start(self):
        if self._started:
            return
        self._started = True

        if self.log.enabled:
            self.log.info("App starting")

        try:
            self.on_start()
        except Exception as e:
            if self.log.enabled:
                self.log.error("Error in on_start", error=str(e))
            raise

    def _exit(self):
        if self.log.enabled:
            self.log.info("App exiting")

        try:
            self.on_exit()
        except Exception as e:
            if self.log.enabled:
                self.log.error("Error in on_exit", error=str(e))

    # --------------------------------------
    # Run
    # --------------------------------------

    def run(self):
        """
        Start the Qt event loop.
        """
        self._start()

        exit_code = 0
        try:
            exit_code = self.qt_app.exec()
        finally:
            self._exit()

        sys.exit(exit_code)

