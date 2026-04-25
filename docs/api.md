Kigo API Reference (v1.0)

Status: Stable
API Guarantee: All APIs documented here are stable within the 3.x series.
Breaking changes will only occur in a 4.x release.


1. Overview
Kigo is a cross‑platform, Qt‑based application framework designed around:

explicit lifecycle management
inspector‑first debugging
unified GUI (Qt), NUI (WebEngine), and ECS inspection
safe, opt‑in tooling
honest performance and platform guarantees

This document defines the official public API surface of Kigo.
Anything not mentioned here is considered internal and may change without notice.

2. Application Core
kigo.app.App
The base class for all Kigo applications.
Pythonfrom kigo.app import AppShow more lines
Constructor
PythonApp(*, dev: bool = False)Show more lines
Parameters

dev (bool): Enables developer tooling. Defaults to False.

Lifecycle Hooks
Pythondef on_start(self) -> NoneShow more lines
Called once after the Qt application is initialized.
Pythondef on_exit(self) -> NoneShow more lines
Called once before application shutdown.
Attributes

























AttributeTypeDescriptionqt_appQApplicationThe underlying Qt applicationplatformdictSnapshot of platform informationlogJsonLoggerApplication logger
Methods
Pythondef run(self) -> NoReturnShow more lines
Starts the Qt event loop and blocks until exit.

3. Platform Detection
Pythonfrom kigo.platform_info import platform_name, summaryShow more lines
platform_name() -> str
Returns the current platform identifier.
Possible values include:

"windows"
"macos"
"linux"
"chromeos"
"android"
"freebsd"
"openbsd"
"sunos/solaris"


summary() -> dict
Returns a structured snapshot of the runtime environment.
This data is immutable after app startup.

4. Networking (Qt‑native)
Pythonfrom kigo.net import req, post, put, delete, ResponseShow more lines
req(url, *, headers=None, timeout_ms=15000) -> Response
Performs a synchronous HTTP GET request using Qt’s networking stack.
Response



































AttributeTypeDescriptionokboolWhether the request succeededstatusintHTTP status codetextstrResponse bodyurlstrFinal URLerrorstr | NoneError message, if any

5. Logging
Logging is opt‑in and disabled by default.
Enabling Logging
Pythonlog = "on"Show more lines
Must be defined before creating the App.
Logger API
Pythonapp.log.info(message, **data)app.log.warn(message, **data)app.log.error(message, **data)Show more lines
All logs are written in newline‑delimited JSON.
Logging must never crash the application.

6. Time Freeze Debugging
Pythonfrom kigo.debug import freezeShow more lines
freeze(reason: str = "Execution paused", *, data: dict | None = None)
Pauses application logic while keeping the UI responsive.

Rendering continues
State remains intact
Execution resumes when released

This function is safe in production builds but intended for debugging.

7. Visual Inspection (GUI)
Pythonfrom kigo.inspector import enable_inspectorShow more lines
enable_inspector(app: QApplication) -> Inspector
Activates the in‑process Visual Inspector.
Capabilities

Widget hover highlighting
Click‑to‑inspect
Geometry and hierarchy inspection
Dockable inspector panel

This API is stable.

8. WebEngine DOM Inspection (NUI)
Pythonfrom kigo.inspector.web import enable_dom_inspectorShow more lines
enable_dom_inspector(view: QWebEngineView) -> DOMBridge
Enables DOM inspection for a WebEngine view.
Features

Click DOM elements
Receive structured DOM data in Python
No external DevTools dependency


9. ECS Entity Inspection
Pythonfrom kigo.inspector.ecs import ECSInspectorShow more lines
ECSInspector(world)
Creates a dockable inspector for an ECS world.
Capabilities

Entity listing
Component inspection
Live updates
Compatible with time‑freeze debugging


10. CLI
Kigo installs the following commands:
Shellkigo runkigo doctorShow more lines
kigo run
Runs app.py in the current directory.
kigo doctor
Performs diagnostics:

Python version
Dependency availability
Qt backend health
Platform detection
Common project errors

kigo doctor will never modify source files.

11. Public vs Internal API
Public API

Everything listed in this document
All symbols re‑exported in __init__.py files

Internal API

Any symbol prefixed with _
Any submodule not re‑exported
All implementation details

Importing internal APIs is unsupported.

12. Versioning & Stability Contract
Kigo follows Semantic Versioning:

PATCH: bug fixes only
MINOR: new features, backwards compatible
MAJOR: breaking changes

Deprecated APIs will emit warnings for at least one minor release before removal.

13. Guarantees
Kigo guarantees:

No silent breaking changes
No background behavior
No implicit magic
No platform lies

This API reference is the contract. 

✅ End of API Reference