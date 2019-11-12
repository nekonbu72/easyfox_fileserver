from code import compile_command
from pathlib import Path
from typing import List, Optional

from marionette_driver.marionette import Actions, Marionette, HTMLElement

from .mime import MIME_TYPES


class Puppet:
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
        # start_session しないと quit もできない
        self.marionette.start_session()
        self.__has_session = True

    @property
    def has_session(self):
        return self.__has_session

    @property
    def auto_download(self):
        return self.__auto_download

    def __activate_auto_download(self):
        # 一度有効にすると同セッション内では無効にできない

        # firefox52 では MIME_TYPES.rdf, firefox60 では handlers.json に
        # ファイルダウンロード時の動作設定が記述されている（text/plain はプログラムで開く、など）
        # 自動ダウンロードするため既存の設定は削除する
        MIME_TYPES_HANDLERS = ["MIME_TYPES.rdf", "handlers.json"]
        for name in MIME_TYPES_HANDLERS:
            p = Path(self.marionette.profile_path).joinpath(name)
            if p.is_file():
                p.unlink()

        self.marionette.set_pref("browser.download.useDownloadDir", True)
        self.marionette.set_pref("browser.helperApps.neverAsk.saveToDisk",
                                 ",".join(MIME_TYPES))
        USER_DEFINED = 2
        self.marionette.set_pref("browser.download.folderList", USER_DEFINED)

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
        self.marionette.quit()
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
