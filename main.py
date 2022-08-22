
from scrap import Scrape

print("# Please input the URL what you want to get repository\n")
url = str(input())

# url = "https://github.com/search?q=lightgbm&type=Repositories&ref=advsearch&l=&l="

delay = 3

print("\n# URL: ", url, delay)

print("\n# Please wait downloading files, you can check url and processes of this\n")
cclauss = Scrape(url)

if url.split("/")[len(url.split("/"))-1].split("?")[0] != "search":
    cclauss.downloadUser()
else:
    print("\n # Downloading Repositories \n")
    cclauss.downloadRepoFiles()

    print("\n # downloading Commits \n")
    cclauss.downloadCommitFiles()

    print("\n # downloading Issues \n")
    cclauss.downloadIssueFiles()

    print("\n # downloading Wikis \n")
    cclauss.downloadWikiFiles()

cclauss.getLogoText()
