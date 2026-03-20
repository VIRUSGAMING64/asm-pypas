import os

class CodeSaver:
    def __init__(self, path):
        self.base_path = os.path.realpath(path)
        os.makedirs(self.base_path, exist_ok=True)

    def resolve_path(self, name: str) -> str:
        if not isinstance(name, str):
            raise ValueError("invalid file name")

        name = name.strip()
        if name == "":
            raise ValueError("invalid file name")

        candidate = os.path.realpath(os.path.join(self.base_path, name))
        if os.path.commonpath([self.base_path, candidate]) != self.base_path:
            raise ValueError("path traversal detected")

        return candidate

    def save(self, name, code: str):
        path = self.resolve_path(name)
        with open(path, "wb") as f:
            f.write(code.encode())

    def load(self, name):
        path = self.resolve_path(name)
        with open(path, "r") as f:
            data = f.read(2**30)
        return data

    def delete(self, name):
        path = self.resolve_path(name)
        os.remove(path)