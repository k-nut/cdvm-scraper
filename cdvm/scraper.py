# -*- coding: utf-8 -*-

import json
import datetime
import turbotlib
from bs4 import BeautifulSoup
import requests

def get_all_pages():
    base_url = "http://www.cdvm.gov.ma"
    base_extension = "/entreprises-de-marche/societes-de-bourse"
    r = requests.get(base_url + base_extension)
    text = r.text
    soup = BeautifulSoup(text)
    div = soup.find("div", {"id": "quicktabs_tabpage_2_1"})
    links =div.find_all("li", {"class": "pager-item"}) 
    get_links(base_extension)
    for link in links:
        get_links(link.find("a")["href"])


def get_links(url_extension):
    base_url = "http://www.cdvm.gov.ma"
    r = requests.get(base_url + url_extension)
    text = r.text
    soup = BeautifulSoup(text)
    div = soup.find("div", {"id": "quicktabs_tabpage_2_1"})
    tbody = div.find("tbody")
    for tr in tbody.find_all("tr"):
        extract_data(base_url + tr.find("a")["href"])

def extract_data(url):
    r = requests.get(url)
    text = r.text
    soup = BeautifulSoup(text)
    tbody = soup.find("tbody")
    information = {}
    information["source_url"] = url
    information["sample_date"] = str(datetime.datetime.now())
    trs = tbody.find_all("tr", recursive=False)
    for tr in trs:
        if len(tr) == 5:
            information[tr.find_all("td")[0].text] = tr.find_all("td")[1].text
        else:
            owners = {}
            body = tr.find("tbody")
            for row in body.find_all("tr"):
                owners[row.find_all("td")[0].text] = row.find_all("td")[1].text
            information["Actionnaires"] = owners

    print(json.dumps(information))

if __name__ == "__main__":
    get_all_pages()
