import json
import os
from pathlib import Path

LIMIT_DEPTH = 3


class DirNode:
    def __init__(self, exists: bool, parent: str, name: str, stem: str, suffix: str, is_dir: bool, is_file: bool,  depth: int, children: list):
        self.exists = exists
        self.parent = parent
        self.name = name
        self.full_path = os.path.join(self.parent, self.name)
        self.stem = stem
        self.suffix = suffix
        self.is_dir = is_dir
        self.is_file = is_file
        self.depth = depth
        self.children = children

    @staticmethod
    def create_from_path(p: Path, depth: int = 0) -> "DirNode":
        next_depth = depth + 1
        children = []
        if next_depth <= LIMIT_DEPTH and p.is_dir():
            for node in p.iterdir():
                children.append(DirNode.create_from_path(node, next_depth))
        return DirNode(p.exists(), str(p.parent), p.name, p.stem, p.suffix, p.is_dir(), p.is_file(), depth, children)

    def __str__(self):
        return self.full_path


class DirNodeJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, DirNode):
            json_str = json.dumps(
                o.__dict__, cls=DirNodeJSONEncoder, ensure_ascii=False)
            return escape_encode(json_str)
        return super().default(o)


def escape_encode(str: str) -> str:
    return str.replace(r'\"', '"').replace(r"\\\\", r"\\").replace('"{', "{").replace('}"', "}")


def directory_tree(root: str) -> DirNode:
    return DirNode.create_from_path(Path(root))


def directory_tree_byJSON(root: str) -> str:
    dirnode = directory_tree(root)
    json_str = escape_encode(json.dumps(
        dirnode.__dict__, cls=DirNodeJSONEncoder, ensure_ascii=False))
    return json_str


if __name__ == "__main__":
    json_str = directory_tree_byJSON('C:\\Users\\s150209\\developer')
    json_str = json.dumps(json.loads(json_str), indent=2, ensure_ascii=False)
    print(json_str)
