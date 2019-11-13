from code import compile_command
from pathlib import Path
from typing import List, Optional

from marionette_driver.marionette import Actions, HTMLElement, Marionette


class Puppet:
    MIME_TYPES = [
        "application/epub+zip",
        "application/gzip",
        "application/java-archive",
        "application/json",
        "application/ld+json",
        "application/msword",
        "application/octet-stream",
        "application/ogg",
        "application/pdf",
        "application/rtf",
        "application/vnd.amazon.ebook",
        "application/vnd.apple.installer+xml",
        "application/vnd.mozilla.xul+xml",
        "application/vnd.ms-excel",
        "application/vnd.ms-fontobject",
        "application/vnd.ms-powerpoint",
        "application/vnd.oasis.opendocument.presentation",
        "application/vnd.oasis.opendocument.spreadsheet",
        "application/vnd.oasis.opendocument.text",
        "application/vnd.openxmlformats-officedocument.presentationml.presentation",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/vnd.visio",
        "application/x-7z-compressed",
        "application/x-abiword",
        "application/x-bzip",
        "application/x-bzip2",
        "application/x-csh",
        "application/x-freearc",
        "application/xhtml+xml",
        "application/xml",
        "application/x-rar-compressed",
        "application/x-sh",
        "application/x-shockwave-flash",
        "application/x-tar",
        "application/zip",
        "appliction/php",
        "audio/aac",
        "audio/midi audio/x-midi",
        "audio/mpeg",
        "audio/ogg",
        "audio/wav",
        "audio/webm",
        "font/otf",
        "font/ttf",
        "font/woff",
        "font/woff2",
        "image/bmp",
        "image/gif",
        "image/jpeg",
        "image/png",
        "image/svg+xml",
        "image/tiff",
        "image/vnd.microsoft.icon",
        "image/webp",
        "text/calendar",
        "text/css",
        "text/csv",
        "text/html",
        "text/javascript",
        "text/javascript",
        "text/plain",
        "text/xml",
        "video/3gpp",
        "video/3gpp2",
        "video/mp2t",
        "video/mpeg",
        "video/ogg",
        "video/webm",
        "video/x-msvideo"
    ]

    def __init__(self, binary: str, profile: str):
        self.__has_session = False
        self.__auto_download = False
        self.__download_dir = ""

        if not Path(binary).is_file():
            return

        if not Path(profile).is_dir():
            return

        # geckodriver の log ファイル出力を抑止する
        NO_LOG = "-"
        self.marionette = Marionette(
            bin=binary, gecko_log=NO_LOG, profile=profile)

        # start_session にファイルを消しておかないと
        # 後で自動ダウンロードできない
        self.__delete_download_profile()

        # start_session しないと quit もできない
        self.marionette.start_session()
        self.__has_session = True

    @property
    def has_session(self):
        return self.__has_session

    @property
    def auto_download(self):
        return self.__auto_download

    def __delete_download_profile(self):
        # mimeTypes.rdf と handlers.json に
        # ファイル読み込み時の動作設定が保存されている（text/plain はファイルを保存、など）
        # 自動ダウンロードするため既存の設定は削除する
        DELETE_TARGET_FILES = ["mimeTypes.rdf", "handlers.json"]
        for name in DELETE_TARGET_FILES:
            p = Path(self.marionette.profile_path).joinpath(name)
            if p.is_file():
                p.unlink()

    def __activate_auto_download(self):
        # 一度有効にすると同セッション内では無効にできない
        self.marionette.set_pref("browser.download.useDownloadDir", True)
        self.marionette.set_pref("browser.helperApps.neverAsk.saveToDisk",
                                 ",".join(self.MIME_TYPES))
        USER_DEFINED = 2
        self.marionette.set_pref("browser.download.folderList", USER_DEFINED)
        self.marionette.set_pref("browser.download.lastDir", None)

    @property
    def download_dir(self):
        if self.__auto_download == False:
            raise Exception("auto download not activated")
        return self.__download_dir

    @download_dir.setter
    def download_dir(self, dir: str):
        p = Path(dir)
        if not p.is_dir():
            return

        full_path = str(p.resolve())
        if self.__auto_download == False:
            self.__activate_auto_download()
            self.__auto_download = True

        self.marionette.set_pref("browser.download.dir", full_path)
        self.marionette.set_pref("browser.download.downloadDir", full_path)
        self.__download_dir = full_path

    def set_download(self, dir: str):
        self.download_dir = dir

    def query_selector(self, selectors: str) -> HTMLElement:
        METHOD_CSS_SELECTOR = "css selector"
        return self.marionette.find_element(METHOD_CSS_SELECTOR, selectors)

    def query_selectors(self, selectors: str) -> List[HTMLElement]:
        METHOD_CSS_SELECTOR = "css selector"
        return self.marionette.find_elements(METHOD_CSS_SELECTOR, selectors)

    def wait(self, seconds: int):
        actions = Actions(self.marionette)
        actions.wait(seconds).perform()

    def quit(self):
        profile = Path(self.marionette.profile_path)
        self.marionette.quit()
        self.__forced_rmdir(profile)
        self.__has_session = False

    def exec(self, script: str) -> Optional[str]:
        # script 内での記述簡略化のため
        mrnt = self.marionette
        set_download = self.set_download
        wait = self.wait
        quit = self.quit
        query_selector = self.query_selector
        query_selectors = self.query_selectors

        try:
            exec(script)
            return None
        except Exception as err:
            return str(err)

    @classmethod
    def __forced_rmdir(self, p: Path):
        for f in p.iterdir():
            if f.is_file():
                f.unlink()
            elif f.is_dir():
                self.__forced_rmdir(f)
        p.rmdir()
