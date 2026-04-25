# SPDX-License-Identifier: Zlib
# kigo/cli/doctor.py

import sys
import os
import importlib.util


def ok(msg): print(f"✅ {msg}")
def warn(msg): print(f"⚠️  {msg}")
def err(msg): print(f"❌ {msg}")


def run_doctor():
    print("Kigo Doctor running…\n")

    checks = [
        check_python,
        check_app_file,
        check_kigo_import,
        check_qt_backend,
        check_platform_file,
    ]

    failed = False
    for check in checks:
        try:
            result = check()
            if result is False:
                failed = True
        except Exception as e:
            err(f"{check.__name__} crashed: {e}")
            failed = True

    print()
    if failed:
        err("Problems detected. Fix the issues above.")
        sys.exit(1)
    else:
        ok("No critical issues found. You’re good to go 🚀")


# -------------------------
# Individual checks
# -------------------------

def check_python():
    if sys.version_info < (3, 9):
        err("Python 3.9+ is required")
        return False
    ok(f"Python {sys.version.split()[0]}")
    return True


def check_app_file():
    if not os.path.exists("app.py"):
        err("app.py not found")
        return False
    ok("app.py found")
    return True


def check_kigo_import():
    try:
        import kigo
        ok("Kigo importable")
        return True
    except Exception as e:
        err(f"Kigo import failed: {e}")
        return False


def check_qt_backend():
    try:
        from kigo.qt.backend import QtCore
        ok("Qt backend OK")
        return True
    except Exception as e:
        err(f"Qt backend failed: {e}")
        return False


def check_platform_file():
    try:
        from kigo.platform_info import platform_name
        ok(f"Platform detected: {platform_name()}")
        return True
    except Exception as e:
        err(f"Platform detection failed: {e}")
        return False
