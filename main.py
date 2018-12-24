#!/usr/bin/python3

import requests
import re
from bs4 import BeautifulSoup
from py2neo import Graph,Node,Relationship
import random

neo_graph = Graph(
  "http://localhost:7474",
  username="neo4j",
  password="111"
)

def getHtml(tailUrl):
  url = 'https://en.wikipedia.org/wiki/' + tailUrl
  headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/64.0.3282.140 Safari/537.36'}
  res = requests.get(url, headers=headers)
  res.encoding = 'utf-8'
  soup = BeautifulSoup(res.text, 'html.parser')
  textList = soup.find('div', id="bodyContent").find_all('a', href=re.compile("^(/wiki/)((?!;)\S)*$"))
  return textList

def filter(tailUrl):
  url = 'https://en.wikipedia.org/wiki/' + tailUrl
  if not re.search('\.(jpg|JPG)$', url):
    if not ':' in t.get('href') and not '%' in t.get('href'):
      return 1

headUrl = 'https://en.wikipedia.org/wiki/'
num = 1
k = 1
tailUrl = "Moon"
while True:
    for n in range(1, 99):
        textList = getHtml(tailUrl)
        node1 = Node(label="FatherWord", name=tailUrl)
        neo_graph.create(node1)
        index = 0
        try:
            urlDict = {}
            for t in textList:
              if filter(tailUrl):
                node2 = Node(label="SonWord", name=t.get_text())
                neo_graph.create(node1)
                node1TOnode2 = Relationship(node1, 'Include', node2)
                neo_graph.create(node1TOnode2)
                urlDict[index] = t.get_text()
                index += 1
                print('\r\n')
                k += 1
            tailUrl = urlDict[random.randint(2,8)]
            print("完成：", n)
            print(k)
        except IndexError:
            break
        except OSError:
            continue
    print('下载完成')
    num += 1

