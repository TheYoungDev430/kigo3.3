# SPDX-License-Identifier: Zlib
# kigo/logging/jsonlog.py

import json
import os
import datetime
from typing import Any


class JsonLogger:
    def __init__(self, enabled: bool = False, path: str = "kigo.log.json"):
        self.enabled = enabled
        self.path = path

        if self.enabled:
            # Ensure file exists
            try:
                os.makedirs(os.path.dirname(path), exist_ok=True)
            except Exception:
                pass

    def _write(self, level: str, msg: str, **extra: Any):
        if not self.enabled:
            return

        entry = {
            "time": datetime.datetime.now().isoformat(timespec="seconds"),
            "level": level,
            "msg": msg,
        }

        if extra:
            entry.update(extra)

        try:
            with open(self.path, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        except Exception:
            # Logging must NEVER crash the app
            pass

    def info(self, msg: str, **extra: Any):
        self._write("INFO", msg, **extra)

    def warn(self, msg: str, **extra: Any):
        self._write("WARN", msg, **extra)

    def error(self, msg: str, **extra: Any):
        self._write("ERROR", msg, **extra)