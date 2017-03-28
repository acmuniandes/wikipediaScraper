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

class wikipediaPage:
    name = ''
    link = ''
    nodes = []
    group = 1

data = {}
data['nodes'] = []
data['links'] = []

maxNodes = 160
currentNodes = 0

initialUrl = "http://en.wikipedia.org/wiki/GitHub"



def scrape(aUrl):
    print(aUrl)
    # print(threading.activeCount())
    page = requests.get(aUrl).text
    soup = BeautifulSoup(page, 'lxml')
    newPage = wikipediaPage()
    newPage.link = aUrl
    newPage.name = soup.find('h1').text

    pageLinks = soup.find('div', id="mw-content-text").find_all('a')
    pageHrefs = list(set(list( map( getLink , pageLinks ) )))
    filteredPageHrefs = list(set(list(filter( lambda s: s != None , pageHrefs))))
    newPage.nodes = filteredPageHrefs

    global maxNodes, currentNodes
    if currentNodes < maxNodes:
        toAddEdges = list( map( lambda x: addEdge(newPage.link , x ) , newPage.nodes ) )
        toAddNodes = list( map( lambda x: addNode(x, newPage.link) , newPage.nodes ) )
        currentNodes = currentNodes + 1
        print(currentNodes, maxNodes)
        print(currentNodes<maxNodes)
        explore = list(map(lambda x: addThread(x), newPage.nodes))


def addThread(urlToScrape):
    global maxNodes,currentNodes
    if currentNodes<maxNodes:
        currentNodes = currentNodes + 1
        print(currentNodes , maxNodes)
        print(currentNodes<maxNodes)
        ts  = threading.Thread( target = scrape , args=[urlToScrape] )
        ts.start()

def addInicio():
    data['nodes'].append({
        'id': "INICIO",
        'group': 10
    })
    with open('file.json' , 'w') as outfile:
        json.dump(data, outfile)
    outfile.close()


def addNode(newNodeId, father):
    data['nodes'].append({
        'id': newNodeId,
        'group': 1
    })
    data['links'].append({
        'source': father,
        'target': newNodeId,
        'value': 20
    })
    with open('file.json' , 'w') as outfile:
        json.dump(data, outfile)
    outfile.close()

addNode(initialUrl , "INICIO")


def addEdge(fromNodeId , toNodeId):
    data['links'].append({
        'source': fromNodeId,
        'target': toNodeId,
        'value': 1
        })
    with open('file.json' , 'w') as outfile:
        json.dump(data, outfile)
    outfile.close()

def getLink(a):
    if a.get("href")!=None and a.get("href").startswith("/wiki/") and not(a.get("href").endswith(".jpg" or ".svg" or ".jpeg")):
        return str("http://wikipedia.org" + a.get("href") )

addInicio()


tsc = threading.Thread(target = scrape , args=[initialUrl] )
tsc.start()
