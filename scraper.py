#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import threading
import time
from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
import lxml
import schedule

class wikipediaPage:
    name = ''
    link = ''
    nodes = []
    group = 1

data = {}
data['nodes'] = []
data['links'] = []
currentNodes = 0
maxNodes = 100
termine = False

initialUrl = "https://en.wikipedia.org/wiki/Music"

def scrape(aUrl):
    global currentNodes
    currentNodes = currentNodes + 1
    page = requests.get(aUrl).text
    soup = BeautifulSoup(page, 'lxml')
    newPage = wikipediaPage()
    newPage.link = aUrl
    newPage.name = soup.find('h1').text
    pageLinks = soup.find('div',id="mw-content-text").find_all('a', limit=40)
    pageHrefs = list(set(list( map( getLink, pageLinks))))
    filteredPageHrefs = list(set(list(filter( lambda s: s!=None ,pageHrefs))))
    newPage.nodes = filteredPageHrefs
    global termine
    if not termine:
        toAddNodes = list( map( lambda x: addNode(x,newPage.link), newPage.nodes ))
        explore = list(map(lambda x: addThread(x), newPage.nodes))
    elif threading.activeCount() < 3:
        writeJSON()

def addThread(urlToScrape):
    global maxNodes
    if currentNodes < maxNodes:
        if threading.activeCount()<20000:
            print( currentNodes, maxNodes, "page to scrape: " , urlToScrape)
            ts = threading.Thread(target=scrape, args=[urlToScrape])
            ts.start()
    else:
        global termine
        termine = True

        

def addInicio():
    data['nodes'].append({
        'id': "INICIO",
        'group': 1
    })

def addNode(newNodeId, father):
    data['nodes'].append({
        'id': newNodeId,
        'group': 1
    })
    data['links'].append({
        'source': father,
        'target': newNodeId,
        'value': 1
    })

def getLink(a):
    if a.get("href") != None and a.get("href").startswith("/wiki/") and not a.get("href").endswith(".jpg" or ".svg" or ".jpeg"):
        return str("http://wikipedia.org" + a.get("href"))

def writeJSON():
    with open('file.json', 'w') as outfile:
        json.dump(data, outfile)
    outfile.close()

def log():
    print("number of active threads: ", threading.activeCount())
    print("time: ", time.clock())
    print(termine)


addInicio()
addNode(initialUrl, "INICIO")
scrape(initialUrl)


schedule.every(1).seconds.do(log)

while True:
    schedule.run_pending()

tsc = threading.Thread(target=scrape, args=[initialUrl])
tsc.start()
