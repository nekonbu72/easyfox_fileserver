import pathlib
from typing import List, Optional


def load_scripts(dir: str, *suffixes: str) -> List[str]:
    scripts = []
    p = pathlib.Path(dir)
    if p.is_dir():
        for content in p.iterdir():
            script = __load_script(content, *suffixes)
            if not script is None and len(script) > 0:
                scripts.append(script)
    return scripts


def load_script(path: str) -> Optional[str]:
    p = pathlib.Path(path)
    return __load_script(p, p.suffix)


def __load_script(path: pathlib.Path, *suffixes: str) -> Optional[str]:
    if path.is_file() and path.suffix in suffixes:
        with open(str(path)) as f:
            script = str(f.read())
        return script
    return None
