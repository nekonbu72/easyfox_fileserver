import json
import os
from pathlib import Path

LIMIT_DEPTH = 3


class DirTree:
    def __init__(self, root_path: str, depth: int = 0):
        p = Path(root_path)
        next_depth = depth + 1
        children = []
        if next_depth <= LIMIT_DEPTH and p.is_dir():
            for dir in p.iterdir():
                children.append(DirTree(str(dir), next_depth))
        self = self.__create(p.exists(),
                             str(p.parent),
                             p.name,
                             p.stem,
                             p.suffix,
                             p.is_dir(),
                             p.is_file(),
                             depth,
                             children)

    def __create(self,
                 exists: bool,
                 parent: str,
                 name: str,
                 stem: str,
                 suffix: str,
                 is_dir: bool,
                 is_file: bool,
                 depth: int,
                 children: list) -> "DirTree":
        self.exists = exists
        self.parent = parent
        self.name = name
        self.stem = stem
        self.suffix = suffix

        self.full_path = os.path.join(self.parent, self.name)

        self.is_dir = is_dir
        self.is_file = is_file
        self.depth = depth

        self.has_children = len(children) > 0
        self.count_children = len(children)

        self.children = children

        return self

    def to_JSON(self) -> str:
        return escape_encode(json.dumps(self.__dict__, cls=DirTreeJSONEncoder, ensure_ascii=False))

    def __str__(self):
        return self.full_path


class DirTreeJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, DirTree):
            json_str = json.dumps(
                o.__dict__, cls=DirTreeJSONEncoder, ensure_ascii=False)
            return escape_encode(json_str)
        return super().default(o)


def escape_encode(str: str) -> str:
    return str                      \
        .replace(r'\"', '"')        \
        .replace(r"\\\\", r"\\")    \
        .replace(r'\"', r'\\"')     \
        .replace('"{', "{")         \
        .replace('}"', "}")
