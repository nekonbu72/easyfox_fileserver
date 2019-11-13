DOWNLOAD_TEST = "http://xcal1.vodafone.co.uk/"
DOWNLOAD_DIR = "download"

mrnt.navigate(DOWNLOAD_TEST)

wait(5)

set_download(DOWNLOAD_DIR)

tgt = query_selector(
    "body > table > tbody > tr:nth-child(16) > td:nth-child(1) > a")

tgt.click()

wait(10)

# quit()
