# -*- coding: utf-8 -*-

import re
import json
import datetime
from bs4 import BeautifulSoup
import requests


BASE_URL = "http://www.cdvm.gov.ma"

def get_all_pages(base_extension):
    div = get_tab_div(base_extension)
    links = div.find_all("li", {"class": "pager-item"})
    get_links(base_extension)
    for link in links:
        get_links(link.find("a")["href"])

def get_tab_div(base_extension):
    response = requests.get(BASE_URL + base_extension)
    text = response.text
    soup = BeautifulSoup(text)
    div = soup.find("div", id=re.compile(r"quicktabs_tabpage_\d_1"))
    return div

def get_links(url_extension):
    div = get_tab_div(url_extension)
    tbody = div.find("tbody")
    for tr in tbody.find_all("tr"):
        extract_data(BASE_URL + tr.find("a")["href"])


def get_license_type_from_url(url):
    if "/entreprises-de-marche/societes-de-bourse" in url:
        return "Sociétés de Bourse"
    if "/entreprises-de-marche/societes-de-gestion" in url:
        return "Société de gestion"
    if "/entreprises-de-marche/teneurs-de-compte" in url:
        return "Teneurs de comptes"

def extract_data(url):
    response = requests.get(url)
    text = response.text
    soup = BeautifulSoup(text)
    tbody = soup.find("tbody")
    information = {}
    information["source_url"] = url
    information["sample_date"] = str(datetime.datetime.now())
    information["type"] = get_license_type_from_url(url)
    trs = tbody.find_all("tr", recursive=False)
    for tr in trs:
        if len(tr) == 5:
            value = tr.find_all("td")[1].text
            #There are links to some lists but they are not of any interest to us
            if not value.startswith("Liste des"):
                information[tr.find_all("td")[0].text] = value
        else:
            owners = {}
            inner_table = tr.find("table")
            for row in inner_table.find_all("tr"):
                # sometimes the table contains ths, sometimes tds.
                # This does not have any influence on the content though.
                ths = row.find_all("th")
                tds = row.find_all("td")
                if ths:
                    # sometimes th contains real information and not only
                    # the headings. In this case we want to include the data
                    if ths[0].text != u'Dénomination':
                        owners[ths[0].text] = ths[1].text
                if tds:
                    owners[tds[0].text] = tds[1].text


            information["Actionnaires"] = owners

    print json.dumps(information)

if __name__ == "__main__":
    get_all_pages("/entreprises-de-marche/societes-de-bourse")
    get_all_pages("/entreprises-de-marche/societe-de-gestion")
    get_all_pages("/entreprises-de-marche/teneurs-de-comptes")
