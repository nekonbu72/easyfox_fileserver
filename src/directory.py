import json
import os
from pathlib import Path
from typing import Callable, List


class DirTree:
    def __init__(self,
                 root: str,
                 suffixes: List[str] = [],
                 depth: int = 0,
                 limit_depth: int = 99,
                 top: str = ""):
        root_p = Path(root)
        self.exists = root_p.exists()
        self.parent = str(root_p.parent)
        self.name = root_p.name
        self.stem = root_p.stem
        self.suffix = root_p.suffix

        self.full_path = os.path.join(self.parent, self.name)

        self.is_dir = root_p.is_dir()
        self.is_file = root_p.is_file()

        if len(suffixes) > 0 and self.is_file:
            self.is_allowed_suffix = self.suffix in suffixes
        else:
            self.is_allowed_suffix = True

        self.depth = depth
        if self.depth == 0:
            self.top = self.full_path
        else:
            self.top = top
        next_depth = self.depth + 1
        children = []
        if next_depth <= limit_depth and root_p.is_dir():
            for child in root_p.iterdir():
                children.append(DirTree(root=str(child),
                                        suffixes=suffixes,
                                        depth=next_depth,
                                        limit_depth=limit_depth,
                                        top=self.top))
        self.children = children

        self.has_children = len(self.children) > 0
        self.count_children = len(self.children)

    def to_JSON(self) -> str:
        return _my_encode(json.dumps(self.__dict__,
                                     cls=_DirTreeJSONEncoder,
                                     ensure_ascii=False))


class _DirTreeJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, DirTree):
            json_str = json.dumps(o.__dict__,
                                  cls=_DirTreeJSONEncoder,
                                  ensure_ascii=False)
            return _my_encode(json_str)
        return super().default(o)


def _my_encode(str: str) -> str:
    encoders = [__encode_escape,
                __encode_naming]

    for encoder in encoders:
        str = encoder(str)
    return str


def __encode_escape(str: str) -> str:
    return str                      \
        .replace(r'\"', '"')        \
        .replace(r"\\\\", r"\\")    \
        .replace(r'\"', r'\\"')     \
        .replace('"{', "{")         \
        .replace('}"', "}")


def __encode_naming(str: str) -> str:
    return str                                              \
        .replace("full_path", "fullPath")                   \
        .replace("is_dir", "isDir")                         \
        .replace("has_children", "hasChildren")             \
        .replace("is_file", "isFile")                       \
        .replace("is_allowed_suffix", "isAllowedSuffix")    \
        .replace("count_children", "countChildren")
