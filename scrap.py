from zipfile import ZipFile

import time

# import Scrapping modules
from bs4 import BeautifulSoup as bs
from requests import get

import os

# https://github.com/HSE-LAMBDA (organization)
# https://github.com/cclauss
# https://github.com/search?q=lightgbm&type=Repositories&ref=advsearch&l=&l=
# https://github.com/search/advanced?q=VWRegressor&type=Repositories
# https://github.com/search?q=xgboost+time+series


class Scrape:
    r"""This Class is very useful to scrape website
        You even know some tag name or class name or id name.
        This would create the Excel file in easy weay
        You only use on function @downloadFiles()
        :downloadFiles() is the function what get url path and download zipfile then unzip it.
        """

    def __init__(self, _url: str, _delay: any):
        r"""this function is constructor to get Institution Data by scraping from website
        :url: website's path name, parameter type: @String
        :_param_num: the number of parameter type: @Number
        """
        os.makedirs(os.getcwd() + "\\downloads\\issues", exist_ok=True)
        os.makedirs(os.getcwd() + "\\downloads\\wikito", exist_ok=True)
        os.makedirs(os.getcwd() + "\\downloads\\repositories", exist_ok=True)
        os.makedirs(os.getcwd() + "\\downloads\\commits", exist_ok=True)

        self.url = _url.split("?")[0]
        self.delay = _delay
        try:
            self.query = _url.split("?")[1]
        except:
            pass


        sub_url = "https://github.com/orgs" + self.url.split("/")[len(_url.split("/"))-1] +"/repositories"
        res = get(sub_url)
        if res.status_code > 300 :
            self.url = self.url
        else:
            self.url = sub_url

        self.downloads = []
        self.files = []
        self.text = "URL: " + _url + "\n"

    def downloadUser(self):
        num = 1
        i = 0
        while True:
            i = i + 1
            repo_param = {
                "page": str(i),
                "tab": "repositories"
            }
            collection = ".wb-break-all a"
            res = get(self.url, repo_param)
            if res.status_code > 300:
                break
            soup = bs(res.content, 'html.parser')
            down = soup.select(collection)
            for element in down:
                URL = "https://github.com" + element['href']
                response = get(URL, {})
                soup = bs(response.content, 'html.parser')
                file_url = soup.select(
                    "div.dropdown-menu.dropdown-menu-sw.p-0 a.no-underline")
                for j in range(1, len(file_url), 2):
                    url = file_url[j]["href"]
                    print("https://github.com" + url)
                    self.text = self.text + "https://github.com" + url + "\n"
                    r = get("https://github.com" + url)
                    time.sleep(self.delay)

                    # creating file
                    file_name = "downloads\\repositories\\" + url.replace("/","_").replace(".zip", "").replace(".","_") + "_NN" + str(num) + ".zip"
                    num = num + 1

                    # download file
                    open(file_name, 'wb').write(r.content)

                    # unzipping file
                    try:
                        with ZipFile(file_name, 'r') as zipObj:
                            # Extract all the contents of zip file in different directory
                            zipObj.extractall(file_name.split(".")[0])
                        print("-------------" + file_name +
                              " unziped--------------------")
                        self.text = self.text + "-------------" + file_name + " unziped--------------------\n"
                    except:
                        pass

    def downloadRepoFiles(self):
        i = 0
        num = 1
        # https://github.com/search/advanced?q=VWRegressor&type=Repositories
        queries = self.query.split("&")
        for ele in queries:
            if "q=" in ele:
                query = ele.replace("q=", "")
        while True:
            i = i + 1
            repo_param = {
                "p": str(i),
                "q": query,
                "type": "Repositories"
            }
            res = get(self.url, repo_param)
            if res.status_code > 300:
                break
            soup = bs(res.content, 'html.parser')
            down = soup.select("a.v-align-middle")
            for element in down:
                URL = "https://github.com" + element['href']
                response = get(URL, {})
                soup = bs(response.content, 'html.parser')
                file_url = soup.select(
                    "div.dropdown-menu.dropdown-menu-sw.p-0 a.no-underline")
                for j in range(1, len(file_url), 2):
                    url = file_url[j]["href"]
                    print("https://github.com" + url)
                    self.text = self.text + "https://github.com" + url + "\n"
                    r = get("https://github.com" + url)
                    time.sleep(self.delay)
                    # creating file
                    file_name = "downloads\\repositories\\" + url.replace("/","_").replace(".zip", "").replace(".","_") + "_NN" + str(num) + ".zip"
                    num = num + 1

                    # download file
                    open(file_name, 'wb').write(r.content)

                    # unzipping file
                    try:
                        with ZipFile(file_name, 'r') as zipObj:
                            # Extract all the contents of zip file in different directory
                            zipObj.extractall(
                                file_name.split(".")[0])
                        print("------------- " + file_name +
                              " unziped--------------------")
                        self.text = self.text + "-------------" + file_name + " unziped--------------------\n"
                    except Exception as err:
                        print(err)

    def downloadWikiFiles(self):
        num = 1
        i = 0
        # https://github.com/search/advanced?q=VWRegressor&type=Repositories
        queries = self.query.split("&")
        for ele in queries:
            if "q=" in ele:
                query = ele.replace("q=", "")
        while True:
            i = i + 1
            repo_param = {
                "p": str(i),
                "q": query,
                "type": "wikis"
            }
            res = get(self.url, repo_param)
            print(res.status_code)
            if res.status_code > 300:
                break
            soup = bs(res.content, 'html.parser')
            down = soup.select("a.Link--muted.text-bold")
            for element in down:
                URL = "https://github.com" + element['href']
                response = get(URL, {})
                soup = bs(response.content, 'html.parser')
                file_url = soup.select(
                    "div.dropdown-menu.dropdown-menu-sw.p-0 a.no-underline")
                for j in range(1, len(file_url), 2):
                    url = file_url[j]["href"]
                    print("https://github.com" + url)
                    self.text = self.text + "https://github.com" + url + "\n"
                    r = get("https://github.com" + url)
                    time.sleep(self.delay)
                    # creating file
                    file_name = "downloads\\wikito\\" + url.replace("/","_").replace(".zip", "").replace(".","_") + "_NN" + str(num) + ".zip"
                    num = num + 1

                    # download file
                    open(file_name, 'wb').write(r.content)

                    # unzipping file
                    try:
                        with ZipFile(file_name, 'r') as zipObj:
                            # Extract all the contents of zip file in different directory
                            zipObj.extractall(file_name.split(".")[0])
                        print("------------- " + file_name +
                              " unziped--------------------")
                        self.text = self.text + "-------------" + file_name + " unziped--------------------\n"
                    except:
                        continue

    def downloadIssueFiles(self):
        i = 1
        num = 1
        # https://github.com/search/advanced?q=VWRegressor&type=Repositories
        queries = self.query.split("&")
        for ele in queries:
            if "q=" in ele:
                query = ele.replace("q=", "")
        while True:
            i = i + 1
            repo_param = {
                "p": str(i),
                "q": query,
                "type": "issues"
            }
            res = get(self.url, repo_param)
            print(res.status_code)
            if res.status_code > 300:
                break
            soup = bs(res.content, 'html.parser')
            down = soup.select("a.Link--muted.text-bold")
            for j in range(0, len(down), 2):
                URL = "https://github.com" + \
                    down[j]['href'].replace("/issues", "")
                response = get(URL, {})
                soup = bs(response.content, 'html.parser')
                file_url = soup.select(
                    "div.dropdown-menu.dropdown-menu-sw.p-0 a.no-underline")
                for k in range(1, len(file_url), 2):
                    url = file_url[k]["href"]
                    print("https://github.com" + url)
                    self.text = self.text + "https://github.com" + url + "\n"
                    r = get("https://github.com" + url)
                    time.sleep(self.delay)
                    # creating file
                    file_name = "downloads\\issues\\" + url.replace("/","_").replace(".zip", "").replace(".","_") + "_NN" + str(num) + ".zip"
                    num = num + 1

                    # download file
                    open(file_name, 'wb').write(r.content)

                    # unzipping file
                    try:
                        with ZipFile(file_name, 'r') as zipObj:
                            # Extract all the contents of zip file in different directory
                            zipObj.extractall(file_name.split(".")[0])
                        print("------------- " + file_name +
                              " unziped--------------------")
                        self.text = self.text + "-------------" + file_name + " unziped--------------------\n"
                    except:
                        continue

    def downloadCommitFiles(self):
        i = 0
        num = 1
        # https://github.com/search/advanced?q=VWRegressor&type=Repositories
        queries = self.query.split("&")
        for ele in queries:
            if "q=" in ele:
                query = ele.replace("q=", "")
        while True:
            i = i + 1
            repo_param = {
                "p": str(i),
                "q": query,
                "type": "commits"
            }
            print(self.url, repo_param["p"],
                  repo_param["q"], repo_param["type"])
            res = get(self.url, repo_param)
            print(res.status_code)
            if res.status_code > 300:
                break
            soup = bs(res.content, 'html.parser')
            down = soup.select("a.Link--secondary.text-bold")
            for element in down:
                URL = "https://github.com" + element['href']
                response = get(URL, {})
                soup = bs(response.content, 'html.parser')
                file_url = soup.select(
                    "div.dropdown-menu.dropdown-menu-sw.p-0 a.no-underline")
                for j in range(1, len(file_url), 2):
                    url = file_url[j]["href"]
                    print("https://github.com" + url)
                    self.text = self.text + "https://github.com" + url + "\n"
                    r = get("https://github.com" + url)
                    time.sleep(self.delay)
                    # creating file
                    file_name = "downloads\\commits\\" + url.replace("/","_").replace(".zip", "").replace(".","_") + "_NN" + str(num) + ".zip"
                    num = num + 1

                    # download file
                    open(file_name, 'wb').write(r.content)

                    # unzipping file
                    try:
                        with ZipFile(file_name, 'r') as zipObj:
                            # Extract all the contents of zip file in different directory
                            zipObj.extractall(file_name.split(".")[0])
                        print("------------- " + file_name +
                              " unziped--------------------")
                        self.text = self.text + "-------------" + file_name + " unziped--------------------\n"
                    except:
                        continue

    def getLogoText(self):
        open("downloads//logo.txt", 'w').write(self.text)       
    
