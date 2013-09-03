import sys
import urllib, urllib2, cookielib
from BeautifulSoup import BeautifulSoup
import re


basicData = {
    'From':'lhr',
    'To':'ams',
    'Departure':'9/4/2013',
    'Return':'9/4/2013',
    'Adults':'1',
    'Childs':'0',
    'Infants':'0',
    'CabinClassId':'1',
    'IncludeGds':'true',
    'IncludeGds':'false',
    'IncludeLowCost':'false',
    'AirCanada':'false',
    'IncludeRail':'false',
    'IncludeHotel':'No hotel results',
    'IncludeVehicles':'false',
    'datetimerequest':'1;9;113;19;17;44'
    }
headers = {
    'Accept':'text/html, */*; q=0.01',
    'Accept-Encoding':'gzip,deflate,sdch',
    'Accept-Language':'en-US,en;q=0.8',
    'Cache-Control':'no-cache',
    'Connection':'keep-alive',
    'Content-Length':'284',
    'Content-Type':'application/x-www-form-urlencoded',
    'Cookie':'arp_scroll_position=526',
    'Host':'demo.travelportuniversalapi.com',
    'Origin':'http://demo.travelportuniversalapi.com',
    'Pragma':'no-cache',
    'X-Requested-With':'XMLHttpRequest'
    }            
class website:
    def __init__(self):
        self.host = 'demo.travelportuniversalapi.com'
        self.ua = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:23.0) Gecko/20100101 Firefox/23.0'  
        self.session = cookielib.CookieJar() #session devine o instanta a obiectului cookielib
        pass     

    def addHeaders(self, url, request, headers):
        headers['User-Agent'] = self.ua
        headers['Referer'] = url
        for k, v in headers.iteritems():
            request.add_header(k,v)

    def get(self):
        try:
            url = 'http://demo.travelportuniversalapi.com/(S(cexfuhghvlzyzx5n0ysesra1))/Search' #this varies every 20 minutes
            data = None
            headers = {'User-Agent': self.ua}
            request = urllib2.Request(url, data, headers)
            self.session.add_cookie_header(request)
            response = urllib2.urlopen(request)
            self.session.extract_cookies(response, request)
            url = response.geturl()
            print url

            data = {'From': 'lhr', 'To': 'ams', 'Departure' : '9/4/2013','Return' : '9/6/2013'}
            basicData.update(data)
            request = urllib2.Request(url+'/SetSearchTermsInSession', data=urllib.urlencode(basicData))
            self.addHeaders(url, request, headers)
            # self.session.extract_cookies(response, request)
            self.session.add_cookie_header(request)
            response = urllib2.urlopen(request, timeout=30) #HTTP Error 404: Not Found - aici am eroare
            print response
            request = urllib2.Request(url+'/SearchLowFare', data=urllib.urlencode(basicData))
            self.addHeaders(url, request, headers)
            print request
            # self.session.extract_cookies(response, request)
            self.session.add_cookie_header(request)
            response = urllib2.urlopen(request, timeout=30) #HTTP Error 404: Not Found - aici am eroare
            print response
            self.session.extract_cookies(response, request)
            print  response.read()
        except urllib2.URLError as e:
            print >> sys.stderr, e
            return None

rt = website()
rt.get()
