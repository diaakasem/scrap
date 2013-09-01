from bs4 import BeautifulSoup
import urllib2
import csv
import time, datetime
import re
import json
import math
from dateutil.parser import *


config = {
        "weight-kg"           : 0,
        "horse-age"           : 0,
        "career-win-rate"     : 0,
        "career-place-rate"   : 100,
        "career-prize-money"  : 0,
        "average-prize-money" : 0,
        "jockey-wins"         : 0,
        "track-wins"          : 0,
        "good-tracks"         : 0,
        "heavy-tracks"        : 0,
        "synthetic-tracks"    : 0,
        "jumps-tracks"        : 0,
        "barrier"             : 0,
        "distance-wins"       : 0,
        "track-distance-wins" : 0,
        "fast-tracks"         : 0,
        "dead-tracks"         : 0,
        "slow-tracks"         : 0
        }


BASE = "http://www.puntersparadise.com.au"
meetings_url = "%s/form-guid/" % BASE
meetings_url = 'http://www.puntersparadise.com.au/form-guide'

url = BASE + "/%s"
data = []
outputFile = 'csvoutput.csv'
fields = ['Rcdate', 'Track', 'Rcno', 'Rctime', 'Tab', 'Horse', 'Rat']
pagesCount = 998

def ordinal(n):
    if 10 <= n % 100 < 20:
        return str(n) + 'th'
    else:
        return  str(n) + {1 : 'st', 2 : 'nd', 3 : 'rd'}.get(n % 10, "th")

def isToday(ts):
    n = datetime.datetime.now()
    d = datetime.datetime.fromtimestamp(ts)
    print "Race Date : %s " % d
    print "Your current time: %s " % n
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
    title = re.findall('(.+)\s*Race.*(\d+)', racedata[1])[0]
    track = title[0]
    track = track.strip()
    racenumber = title[1]
    racenumber = re.findall('\d+', racedata[1])[0]
    ts = float(soup.find('abbr', {'class': 'time12'})['data-utime'])
    otime = datetime.datetime.fromtimestamp(ts)
    racetime = otime.strftime('%I:%M%p')

    if not isToday(ts):
        print "Skipping - Not today : %s " % racedate
        return

    horses = []
    runners = soup.findAll('div', {'class': 'csRunner'})
    def num(string):
        s = str(float(string))
        if len(s) > 4:
            return float(s[0:4])
        return float(s)

    maxResults = {
            "weight-kg"           : 0,
            "horse-age"           : 0,
            "career-win-rate"     : 0,
            "career-place-rate"   : 0,
            "career-prize-money"  : 0,
            "average-prize-money" : 0,
            "jockey-wins"         : 0,
            "track-wins"          : 0,
            "good-tracks"         : 0,
            "heavy-tracks"        : 0,
            "synthetic-tracks"    : 0,
            "jumps-tracks"        : 0,
            "barrier"             : 0,
            "distance-wins"       : 0,
            "track-distance-wins" : 0,
            "fast-tracks"         : 0,
            "dead-tracks"         : 0,
            "slow-tracks"         : 0
            }
    for runner in runners:
        obj = {
            "runner-name"         : runner.get('data-runner-name', ''),
            "runner-title"        : runner.get('data-runner-title', ''),

            "weight-kg"           : num(runner.get('data-weight-kg', '0')),
            "horse-age"           : num(runner.get('data-horse-age', '0')),
            "career-win-rate"     : num(runner.get('data-career-win-rate', '0')),
            "career-place-rate"   : num(runner.get('data-career-place-rate', '0')),
            "career-prize-money"  : num(runner.get('data-career-prize-money', '0')),
            "average-prize-money" : num(runner.get('data-average-prize-money', '0')),
            "jockey-wins"         : num(runner.get('data-jockey-wins', '0')),
            "track-wins"          : num(runner.get('data-track-wins', '0')),
            "good-tracks"         : num(runner.get('data-good-tracks', '0')),
            "heavy-tracks"        : num(runner.get('data-heavy-tracks', '0')),
            "synthetic-tracks"    : num(runner.get('data-synthetic-tracks', '0')),
            "jumps-tracks"        : num(runner.get('data-jumps-tracks', '0')),
            "barrier"             : num(runner.get('data-barrier', '0')),
            "distance-wins"       : num(runner.get('data-distance-wins', '0')),
            "track-distance-wins" : num(runner.get('data-track-distance-wins', '0')),
            "fast-tracks"         : num(runner.get('data-fast-tracks', '0')),
            "dead-tracks"         : num(runner.get('data-dead-tracks', '0')),
            "slow-tracks"         : num(runner.get('data-slow-tracks', '0'))
            }
        maxResults = {
            "weight-kg"           : max(obj["weight-kg"], maxResults["weight-kg"]),
            "horse-age"           : max(obj["horse-age"], maxResults["horse-age"]),
            "career-win-rate"     : max(obj["career-win-rate"], maxResults["career-win-rate"]),
            "career-place-rate"   : max(obj["career-place-rate"], maxResults["career-place-rate"]),
            "career-prize-money"  : max(obj["career-prize-money"], maxResults["career-prize-money"]),
            "average-prize-money" : max(obj["average-prize-money"], maxResults["average-prize-money"]),
            "jockey-wins"         : max(obj["jockey-wins"], maxResults["jockey-wins"]),
            "track-wins"          : max(obj["track-wins"], maxResults["track-wins"]),
            "good-tracks"         : max(obj["good-tracks"], maxResults["good-tracks"]),
            "heavy-tracks"        : max(obj["heavy-tracks"], maxResults["heavy-tracks"]),
            "synthetic-tracks"    : max(obj["synthetic-tracks"], maxResults["synthetic-tracks"]),
            "jumps-tracks"        : max(obj["jumps-tracks"], maxResults["jumps-tracks"]),
            "barrier"             : max(obj["barrier"], maxResults["barrier"]),
            "distance-wins"       : max(obj["distance-wins"], maxResults["distance-wins"]),
            "track-distance-wins" : max(obj["track-distance-wins"], maxResults["track-distance-wins"]),
            "fast-tracks"         : max(obj["fast-tracks"], maxResults["fast-tracks"]),
            "dead-tracks"         : max(obj["dead-tracks"], maxResults["dead-tracks"]),
            "slow-tracks"         : max(obj["slow-tracks"], maxResults["slow-tracks"])
            }
        horses.append(obj)

    horsesRates = {}
    for horse in horses:
        rate = 0
        for k in config.iterkeys():
            rate += ( horse.get(k, 0) / (maxResults.get(k, 1) or 1) ) * config.get(k, 0) / 100

        horsesRates[horse.get('runner-name', '').strip()] = int(round(rate * 100))

    data = soup.find('table', {'class': 'formRaceCard'})
    data = data.findAll('tr')[1:]

    for tr in data:
        number = tr.find('td', {'class': 'horseNumber'})
        number = number.find('a').text

        name = tr.find('td', {'class': 'horseDetails'})
        name = name.find('a', {'class': 'hoverTrigger'}).text
        name = name.strip()

        # rate = tr.find('td', {'class': 'winPercent'}).text
        # rate = re.findall('\d+', rate)[0]
        rate = horsesRates.get(name, 0)

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

    result.sort(key=lambda row: row.get('Rat', 0), reverse=True)
    # print json.dumps(result, sort_keys = False, indent = 4)
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

