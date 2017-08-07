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

def create_directory(manga_name, chapter_name):
    print manga_name
    print chapter_name
    if not os.path.exists(manga_name):
        os.makedirs(manga_name)
    if not os.path.exists(manga_name + '/' + chapter_name):
        os.makedirs(manga_name + '/' + chapter_name)

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
    chapter_name = None

    for index, valeur in enumerate(td):
        if str(valeur) == "<td>Titre:</td>":
            chapter_name = td[index + 1]
            break
    #if the manga haven't chapter name. I get the chapter number
    if chapter_name == None:
        for index, valeur in enumerate(td):
            if str(valeur) == "<td>Chapitre:</td>":
                chapter_name = td[index + 1]
                break
    #Regex to get only the string between > and <
    chapter_name = re.findall('>(.*)<', str(chapter_name))
    return chapter_name[0]

def get_number_page(website):
    soup = BeautifulSoup(website)
    td = soup.findAll("option")
    return len(td)

def get_all_jpg_link(website, number_pages):
    soup = BeautifulSoup(website)
    td = soup.findAll("img")
    link_list = []
    iter = 1
    for link in soup.findAll("img"):
        if (link.get("src") != "None"):
            link = link.get("src")
            break
    number = link.split('/')
    number = number[-1].split('.')
    first_page = number[0]
    iter += int(first_page) - 1
    while iter <= number_pages + int(first_page):
        if iter < 10:
            link_list.append(link.replace(first_page + ".jpg", "0" + str(iter) + ".jpg"))
        else:
            link_list.append(link.replace(first_page + ".jpg", str(iter) + ".jpg"))
        iter += 1
    return link_list

def download_all_jpg(manga_name, chapter_name, link_list):
    page_number = 1
    for link in link_list: 
        ext = link.split(".")
        req = urllib2.Request(link, headers=hdr)
        try:
            img = urllib2.urlopen(req)
        except:
            #page_number += 1
            continue
        print "\033[1;32mDownload :\033[0m " + manga_name + "/" + chapter_name + "/" + str(page_number) + "." + ext[-1]
        localFile = open(manga_name + "/" + chapter_name + "/" + str(page_number) + "." + ext[-1], 'wb')
        localFile.write(img.read())
        localFile.close()
        page_number += 1

def main():
    website = open_html(sys.argv[1])
    manga_name = get_manga_name(website)
    chapter_name = get_chapter_name(website)
    number_pages = get_number_page(website)
    link_list = get_all_jpg_link(website, number_pages)
    create_directory(manga_name, chapter_name)
    download_all_jpg(manga_name, chapter_name, link_list)


if __name__ == '__main__':
    main()
