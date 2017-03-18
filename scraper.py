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
import json

lock = threading.Lock()

class wikipediaPage:
    name = ''
    link = ''
    nodes = []
    id = ''
    sons=[]
    group = 1

data = {}
data['nodes'] = []
data['links'] = []


initialUrl = "http://en.wikipedia.org/wiki/GitHub"


def scrape(aUrl):
    page = requests.get(aUrl).text
    soup = BeautifulSoup(page, 'lxml')
    newPage = wikipediaPage()
    newPage.link = aUrl
    newPage.id = hash(aUrl)
    newPage.name = soup.find('h1').text
    pageAs = soup.find('div', id="mw-content-text").find_all('a', limit=50)
    pageHrefs = list(map(getLink, pageAs))
    filteredPageHrefs = list(filter(lambda s: s != None , pageHrefs))
    pageHrefsWithHttp = list(map(addHttp , filteredPageHrefs))
    newPage.nodes = pageHrefsWithHttp
    newPage.sons = list( map(lambda x: x , newPage.nodes ) )
    edges = list(map(lambda x: (newPage.link , x ) , newPage.sons ))
    addNode(newPage.link)
    toAddNodes = list(map(lambda x: addNode(x) , newPage.sons ))
    links = list(map(lambda x: addEdge(newPage.link , x ) , newPage.sons ))
    randomNumber = random.randint(2,4)
    selectedNumber = len(newPage.nodes)/(randomNumber)
    floorNumber = math.floor( selectedNumber )
    selectedPage = newPage.nodes[floorNumber]
    writePage(newPage)
    if selectedPage == None:
        selectedPage = newPage.nodes[3]
        scrape(selectedPage)
        ts = threading.Thread(target = scrape , args=[selectedPage] )
        tsh = threading.Thread(scrape, args=[newPage.nodes[4]])
        tsh.start()
        ts.setName(selectedPage)
        ts.start()
    print(selectedPage)
    scrape(selectedPage)
    ts  = threading.Thread( target = scrape , args=[selectedPage] )
    tsc = threading.Thread(target = scrape , args=[newPage.nodes[floorNumber+1]])
    tsc.start()
    ts.setName(selectedPage)
    ts.start()


def writePage(aPage):
    with open('results.csv','a') as csvfile:
        fieldnames = ['id','sons' , 'name' , 'link', 'nodes']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({'id':aPage.id, 'sons':aPage.sons, 'name': aPage.name , 'link':aPage.link, 'nodes':aPage.nodes })

def addNode(newNodeId):
    lock.acquire()
    data['nodes'].append({
        'id': newNodeId,
        'group': 1
    })
    with open('file.json', 'w') as outfile:
        json.dump(data, outfile)
    lock.release()

def addEdge(fromNodeId , toNodeId):
    lock.acquire()
    data['links'].append({
        'source': fromNodeId,
        'target': toNodeId,
        'value': 1
    })
    with open('file.json', 'w') as outfile:
        json.dump(data, outfile)
    lock.release()

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
