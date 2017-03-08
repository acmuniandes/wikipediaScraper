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
import networkx as nx
import matplotlib as plt
import pygraphviz

plt.use("Agg")
G=nx.Graph()
G.add_node(1)


class wikipediaPage:
    name = ''
    link = ''
    nodes = []
    id = ''
    sons=[]

initialUrl = "http://en.wikipedia.org/wiki/GitHub"
numfoto=0


def scrape(aUrl):
    page = requests.get(aUrl).text
    soup = BeautifulSoup(page, 'lxml')
    newPage = wikipediaPage()
    newPage.link = aUrl
    newPage.id = hash(aUrl)
    G.add_node(newPage.id)
    newPage.name = soup.find('h1').text
    pageAs = soup.find('div', id="mw-content-text").find_all('a', limit=50)
    pageHrefs = list(map(getLink, pageAs))
    filteredPageHrefs = list(filter(lambda s: s != None , pageHrefs))
    pageHrefsWithHttp = list(map(addHttp , filteredPageHrefs))
    newPage.nodes = pageHrefsWithHttp
    newPage.sons = list( map(lambda x: hash(x) , newPage.nodes ) )
    edges = list(map(lambda x: (newPage.id , x ) , newPage.sons ))
    G.add_edges_from( edges )
    print(type(G))
    K5=nx.complete_graph(5)
    A=nx.drawing.nx_agraph.to_agraph(K5)
    # A=nx.to_agraph(G)
    pos = nx.drawing.nx_agraph.graphviz_layout(A)
    A.draw('file.dot')
    # figura = nx.draw_random(G)
    # plt.pyplot.show()
    # global numfoto
    # plt.pyplot.savefig("fotos/" + str(numfoto) + "path.pdf", linewidth=30.0)
    # numfoto += 1
    randomNumber = random.randint(2,4)
    selectedNumber = len(newPage.nodes)/(randomNumber)
    floorNumber = math.floor( selectedNumber )
    selectedPage = newPage.nodes[floorNumber]
    writePage(newPage)
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



def writePage(aPage):
    with open('results.csv','a') as csvfile:
        fieldnames = ['id','sons' , 'name' , 'link', 'nodes']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({'id':aPage.id, 'sons':aPage.sons, 'name': aPage.name , 'link':aPage.link, 'nodes':aPage.nodes })


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
