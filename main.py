#!/usr/bin/python

import urllib2
import urllib
import sys
import re
import os
from BeautifulSoup import BeautifulSoup

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

def get_index_of(value, in_list):
    for index, valeur in enumerate(in_list):
        if valeur == value:
            return index
    return -1

def open_html(website):
    req = urllib2.Request(website, headers=hdr)
    response = urllib2.urlopen(req)
    data = response.read()
    return data

def get_manga_name(website):
    soup = BeautifulSoup(website)
    for link in soup.findAll("select"):
        if (link.get("data-nom") != "None"):
            manga_name = link.get("data-nom")
            break
    return manga_name

def get_chapter_name(website):
    soup = BeautifulSoup(website)
    td = soup.findAll("td")

    for index, valeur in enumerate(td):
        if str(valeur) == "<td>Titre:</td>":
            chapter_name = td[index + 1]
            break
    chapter_name = re.findall('>(.*)<', str(chapter_name))
    return chapter_name

def main():
    website = open_html(sys.argv[1])
    manga_name = get_manga_name(website)
    chapter_name = get_chapter_name(website)
    print chapter_name[0]

if __name__ == '__main__':
    main()
