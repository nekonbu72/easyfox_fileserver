from pathlib import Path


def setup_download_folder(dir: str):
    p = Path(dir)
    # dir フォルダがなければ作成
    if not p.is_dir():
        p.mkdir()
    else:
        # dir フォルダを空にする
        for f in p.iterdir():
            f.unlink()
