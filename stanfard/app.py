import base64
from itertools import chain
from bs4 import BeautifulSoup
from soupselect import select
import urllib2
import csv
import time, datetime
import re
import json
from dateutil.parser import *
from decorators import retry
import StringIO
import gzip

Accept='text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
Language='en-US,en;q=0.8'
Encoding='gzip,deflate,sdch'
CacheControl='no-cache'
Connection='keep-alive'
Host='explorecourses.stanford.edu'
Pragma='no-cache'
Agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36'

@retry(urllib2.URLError, tries=4, delay=3, backoff=2)
def request(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', Agent)
    req.add_header('Accept', Accept)
    req.add_header('Accept-Encoding', Encoding)
    req.add_header('Accept-Language', Language)
    req.add_header('Cache-Control', CacheControl)
    req.add_header('Connection', Connection)
    req.add_header('Host', Host)
    req.add_header('Paragma', Pragma)
    req.add_header('User-Agent', Agent)
    # req.add_unredirected_header('User-Agent', agent)
    reqObj = urllib2.urlopen(req)
    res = reqObj.read()
    data = StringIO.StringIO(res)
    gzipper = gzip.GzipFile(fileobj=data)
    html = gzipper.read()
    return html

BASE = "http://explorecourses.stanford.edu/"
url = BASE + "/%s"
data = []
outputFile = 'output.txt'
fields = ['number', 'time', 'title']
pagesCount = 998

def isToday(date_str):
    d = parse(date_str)
    n = datetime.datetime.now()
    return d.day == n.day

def href(links):
    return [link['href'] for link in links]

def getLinks():
    selector = '.departmentsContainer ul li a'
    page = request(BASE)
    soup = BeautifulSoup(page)
    links = select(soup, selector)
    return href(links)

def extractPage(url, pagination=True):
    print 'Extracting : %s' % url
    result = []
    page = request(url)
    soup = BeautifulSoup(page)
    info = select(soup, '.courseInfo')
    for record in info:
        courseNumber = record.find('span', {'class': 'courseNumber'}).text
        courseTitle = record.find('span', {'class': 'courseTitle'}).text
        courseAttrs = record.find('div', {'class': 'courseAttributes'}).text
        terms = [x for x in courseAttrs.split('|') if 'terms' in x.lower()] 
        if terms:
            courseTime = str(terms[0].split(':')[1]).strip()
        else:
            courseTime = "not given this year"

        obj = {
                'title': courseTitle,
                'number': courseNumber,
                'time': courseTime
                }
        result.append(obj)

    subresults = []
    if pagination:
        pages = select(soup, '#pagination a')
        pagesLinks = href(pages)
        for l in set(pagesLinks):
            subresults.extend(extractPage(BASE + l, False))
    if subresults:
        result.extend(subresults) 
    return result

def writeData(outputFile, data):
    with open(outputFile, 'wb') as csvfile:
        output = csv.DictWriter(csvfile, delimiter=',', fieldnames=fields)
        output.writeheader()
        output.writerows(data)

def formatData(data):
    return '%(number)s %(title)s\n%(time)s\n\n' % data

def save(outputFile, data):
    with open(outputFile, 'wb') as textfile:
        res = ''
        for obj in data:
            res += formatData(obj)
        textfile.write(res)

allResults = []
def main():
    links = getLinks()
    for link in links[12:15]:
        link = re.sub('filter.*(&|$)', '', link)
        # Adds results
        result = extractPage(BASE + link)
        # Have it saved 
        allResults.extend(result)
        time.sleep(1)
    print "Writing to disk."
    save(outputFile, allResults)
    print "Done."

if __name__ == '__main__':
    main()

