from download import setup_download_folder
from puppet import Puppet
from script import load_script
from userprofile import profile_dir


def main():
    BINARY = "C:\\Program Files\\Mozilla Firefox\\firefox.exe"
    profile = profile_dir()
    if profile is None:
        print("profile is None")
        return

    puppet = Puppet(BINARY, profile)
    if not puppet.has_session:
        print("puppet doesn't has marionette")
        return

    DOWNLOAD = "download"
    setup_download_folder(DOWNLOAD)

    SCRIPT = "src\\puppeteer\\scripts\\sample.py"
    script = load_script(SCRIPT)
    if script is None:
        print("script is None")
        puppet.quit()
        return

    err = puppet.exec(script)
    if not err is None:
        print("error occurred in script: ", err)

    # DOWNLOAD_TEST = "http://xcal1.vodafone.co.uk/"
    # DOWNLOAD_DIR = "download"

    # puppet.marionette.navigate(DOWNLOAD_TEST)
    # puppet.wait(5)
    # puppet.set_download(DOWNLOAD_DIR)
    # tgt = puppet.query_selector(
    #     "body > table > tbody > tr:nth-child(16) > td:nth-child(1) > a")
    # tgt.click()
    # puppet.wait(15)

    if puppet.has_session:
        puppet.quit()
        print("quit in main.")


main()
