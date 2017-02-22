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
import math
import random
import threading

class wikipediaPage:
    name = ''
    link = ''
    nodes = ''

initialUrl = "http://en.wikipedia.org/wiki/GitHub"


def scrape(aUrl):
    print(threading.active_count())
    page = requests.get(aUrl).text
    soup = BeautifulSoup(page, 'lxml')
    newPage = wikipediaPage()
    newPage.name = soup.find('h1').text
    pageAs = soup.find('div', id="mw-content-text").find_all('a', limit=50)
    pageHrefs = list(map(getLink, pageAs))
    filteredPageHrefs = list(filter(lambda s: s != None , pageHrefs))
    pageHrefsWithHttp = list(map(addHttp , filteredPageHrefs))
    newPage.nodes = pageHrefsWithHttp
    randomNumber = random.randint(2,4)
    selectedNumber = len(newPage.nodes)/(randomNumber)
    print("length " + str(len(newPage.nodes)))
    print("divided by " + str(randomNumber) )
    floorNumber = math.floor( selectedNumber )
    print("floorNumber is" + str(floorNumber))
    selectedPage = newPage.nodes[floorNumber]
    if selectedPage == None:
        selectedPage = newPage.nodes[3]
        ts = threading.Thread(target = scrape , args=[selectedPage] )
        tsh = threading.Thread(scrape, args=[newPage.nodes[4]])
        tsh.start()
        # ts.setName(selectedPage)
        ts.start()
    print(selectedPage)
    ts  = threading.Thread( target = scrape , args=[selectedPage] )
    tsc = threading.Thread(target = scrape , args=[newPage.nodes[floorNumber+1]])
    tsc.start()
    # ts.setName(selectedPage)
    ts.start()


def addHttp(a):
    a = str("http://wikipedia.org" + a)
    return a

def getAs(a):
    if(a.find("a")!=None):
        return a.find("a")

def getLink(a):
    if a.get("href")!=None and a.get("href").startswith("/wiki/") and not(a.get("href").endswith(".jpg" or ".svg" or ".jpeg")):
        return a.get("href")

def isNotNone(a):
    if a != None:
        return True

def log(a):
    print(":::::" + a)

tsc = threading.Thread(target = scrape , args=[initialUrl] )
tsc.setName(initialUrl)
tsc.start()
