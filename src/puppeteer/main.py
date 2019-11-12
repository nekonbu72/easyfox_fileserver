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

    res = puppet.exec(script)
    if not res is None:
        print("error occurred in script: ", res)

    if puppet.has_session:
        puppet.quit()
        print("quit in main.")


main()

if __name__ == "__main__":
    pass
