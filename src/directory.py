import json
import os
from pathlib import Path
from typing import Callable, List
from inspect import ismethod


class DirTree:
    def __init__(self,
                 root: str,
                 suffixes: List[str] = [],
                 depth: int = 0,
                 limit_depth: int = 99,
                 top: str = ""):
        root_p = Path(root)
        self.__exists = root_p.exists()
        self.__parent = str(root_p.parent)
        self.__name = root_p.name
        self.__stem = root_p.stem
        self.__suffix = root_p.suffix

        self.__full_path = os.path.join(self.parent, self.name)

        self.__is_dir = root_p.is_dir()
        self.__is_file = root_p.is_file()

        if len(suffixes) > 0 and self.is_file:
            self.__is_allowed_suffix = self.suffix in suffixes
        else:
            self.__is_allowed_suffix = True

        self.__depth = depth
        if self.depth == 0:
            self.__top = self.full_path
        else:
            self.__top = top
        next_depth = self.depth + 1

        self.__relative = str(root_p.relative_to(self.top))

        children = []
        if next_depth <= limit_depth and root_p.is_dir():
            for child in root_p.iterdir():
                children.append(DirTree(root=str(child),
                                        suffixes=suffixes,
                                        depth=next_depth,
                                        limit_depth=limit_depth,
                                        top=self.top))
        self.__children = children

        self.__has_children = len(self.children) > 0
        self.__count_children = len(self.children)

    @property
    def exists(self):
        return self.__exists

    @property
    def parent(self):
        return self.__parent

    @property
    def name(self):
        return self.__name

    @property
    def stem(self):
        return self.__stem

    @property
    def full_path(self):
        return self.__full_path

    @property
    def suffix(self):
        return self.__suffix

    @property
    def is_dir(self):
        return self.__is_dir

    @property
    def is_file(self):
        return self.__is_file

    @property
    def is_allowed_suffix(self):
        return self.__is_allowed_suffix

    @property
    def depth(self):
        return self.__depth

    @property
    def top(self):
        return self.__top

    @property
    def relative(self):
        return self.__relative

    @property
    def children(self):
        return self.__children

    @property
    def has_children(self):
        return self.__has_children

    @property
    def count_children(self):
        return self.__count_children

    def to_JSON(self) -> str:
        return _my_encode(json.dumps(self._JSONable_dict(),
                                     cls=_DirTreeJSONEncoder,
                                     ensure_ascii=False))

    def _JSONable_dict(self) -> dict:
        dic = {}
        for prop in _public_props(self):
            dic[prop] = getattr(self, prop)
        return dic


class _DirTreeJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, DirTree):
            json_str = json.dumps(o._JSONable_dict(),
                                  cls=_DirTreeJSONEncoder,
                                  ensure_ascii=False)
            return _my_encode(json_str)
        return super().default(o)


def _public_props(o) -> List[str]:
    public = []
    for attr in dir(o):
        if not attr[0] == "_" and not ismethod(getattr(o, attr)):
            public.append(attr)
    return public


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
