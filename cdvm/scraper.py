# -*- coding: utf-8 -*-

import re
import json
import datetime
import turbotlib
from bs4 import BeautifulSoup
import requests

def get_all_pages(base_extension):
    base_url = "http://www.cdvm.gov.ma"
    base_extension = "/entreprises-de-marche/societes-de-bourse"
    base_extension = "/entreprises-de-marche/societe-de-gestion"
    r = requests.get(base_url + base_extension)
    text = r.text
    soup = BeautifulSoup(text)
    div = soup.find("div", id = re.compile("quicktabs_tabpage_\d_1"))
    links =div.find_all("li", {"class": "pager-item"}) 
    get_links(base_extension)
    for link in links:
        get_links(link.find("a")["href"])


def get_links(url_extension):
    base_url = "http://www.cdvm.gov.ma"
    r = requests.get(base_url + url_extension)
    text = r.text
    soup = BeautifulSoup(text)
    div = soup.find("div", id = re.compile("quicktabs_tabpage_\d_1"))
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
            inner_table = tr.find("table")
            for row in inner_table.find_all("tr"):
                # sometimes the table contains ths, sometimes tds.
                # This does not have any influence on the content though.
                ths = row.find_all("th")
                tds = row.find_all("td")
                if ths:
                    owners[ths[0].text] = ths[1].text
                if tds:
                    owners[tds[0].text] = tds[1].text


            information["Actionnaires"] = owners

    print(json.dumps(information))

if __name__ == "__main__":
    get_all_pages("/entreprises-de-marche/societes-de-bourse")
    get_all_pages("/entreprises-de-marche/societe-de-gestion")
    get_all_pages("/entreprises-de-marche/teneurs-de-comptes")
