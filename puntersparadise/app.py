from bs4 import BeautifulSoup
import urllib2
import csv
import time, datetime
import re
import json
from dateutil.parser import *


BASE = "http://www.puntersparadise.com.au"
meetings_url = "%s/form-guid/" % BASE
meetings_url = 'http://www.puntersparadise.com.au/form-guide'

url = BASE + "/%s"
data = []
outputFile = 'csvoutput.csv'
fields = ['Rcdate', 'Track', 'Rcno', 'Rctime', 'Tab', 'Horse', 'Rat']
pagesCount = 998

def isToday(date_str):
    d = parse(date_str)
    n = datetime.datetime.now()
    return d.day == n.day

def getMeetings():
    page = urllib2.urlopen(meetings_url).read()
    soup = BeautifulSoup(page)
    scripts = soup.findAll('script')
    script = [ script for script in scripts if 'meeting_events' in str(script) ]
    jsCode = re.sub('<[^<]+?>', '', str(script[0]))
    array = re.findall('meeting_events\s*=\s*(.*)\s*;', jsCode)
    return json.loads(array[0])

def extractPage(url):
    page = urllib2.urlopen(url).read()
    soup = BeautifulSoup(page)
    fh = soup.find('div' , {'class': 'formHeader'})
    h2 = fh.find('h2').text
    result = []
    racedata = h2.split('-')
    racedate = racedata[0].strip()

    if not isToday(racedate):
        print "Skipping - Not today : %s " % racedate
        return

    title = re.findall('(.+)\s*Race.*(\d+)', racedata[1])[0]
    track = title[0]
    racenumber = title[1]
    racenumber = re.findall('\d+', racedata[1])[0]
    racetime = soup.find('abbr', {'class': 'time12'})['data-utime']
    otime = datetime.datetime.fromtimestamp(float(racetime))
    racetime = otime.strftime('%I:%M%p')

    data = soup.find('table', {'class': 'formRaceCard'})
    data = data.findAll('tr')[1:]

    for tr in data:
        number = tr.find('td', {'class': 'horseNumber'})
        number = number.find('a').text

        name = tr.find('td', {'class': 'horseDetails'})
        name = name.find('a', {'class': 'hoverTrigger'}).text

        rate = tr.find('td', {'class': 'winPercent'}).text
        rate = re.findall('\d+', rate)[0]
        obj = {
                'Rcdate': racedate,
                'Track': track,
                'Rctime': racetime,
                'Rcno': racenumber,
                'Tab': number,
                'Horse': name,
                'Rat': rate
                }
        result.append(obj)
    return result

def writeData(outputFile, data):
    with open(outputFile, 'wb') as csvfile:
        output = csv.DictWriter(csvfile, delimiter=',', fieldnames=fields)
        output.writeheader()
        output.writerows(data)

def main():
    result = []
    meetings = getMeetings()
    for meeting in meetings:
        u = url % meeting['href']
        print "Working on : %s" % meeting['href']
        data = extractPage(u)
        if data:
            result = result + data

        print "Writing to disk."
        writeData(outputFile, result)
        time.sleep(1)
    print "Done."

if __name__ == '__main__':
    main()

