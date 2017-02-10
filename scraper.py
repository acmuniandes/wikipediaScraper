#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import csv
import html5lib
from urllib.request import urlopen
import os
import requests
import csv
import lxml

class wikipediaPage:
    name = ''
    link = ''
    nodes = ''

initialUrl = "http://en.wikipedia.org/wiki/GitHub"


def scrape(aUrl):
    page = requests.get(aUrl).text
    soup = BeautifulSoup(page, 'lxml')
    newPage = wikipediaPage()
    newPage.name = soup.find('h1').text
    pageContent = soup.find('div', id="mw-content-text")
    pagePs = pageContent.find_all('p')
    pageAs = list(map(getAs, pagePs))
    pageHrefs = list(map(getLink, pageAs))
    print(pageHrefs)


def getAs(a):
    if(a.find("a")!=None):
        return a.find("a")

def getLink(a):
    if a != None and a.get("href")!=None and a.get("href").startswith("/wiki/"):
        return a.get("href")

def log(a):
    print(":::::" + a)

scrape(initialUrl)
