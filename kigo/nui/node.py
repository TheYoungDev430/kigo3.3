class Node:
    def __init__(self, backend, ref):
        self.backend = backend
        self.ref = ref

    def set(self, **props):
        if self.backend == "qt":
            for k, v in props.items():
                setattr(self.ref, k, v)
        elif self.backend == "web":
            self.ref.page().runJavaScript(
                f"Object.assign(window.__node, {props})"
            )