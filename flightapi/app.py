import sys
import urllib
import urllib2
import cookielib
from BeautifulSoup import BeautifulSoup


basicData = {
    'From': 'lhr',
    'To': 'ams',
    'Departure': '9/4/2013',
    'Return': '9/4/2013',
    'Adults': '1',
    'Childs': '0',
    'Infants': '0',
    'CabinClassId': '1',
    'IncludeGds': 'true',
    'IncludeGds': 'false',
    'IncludeLowCost': 'false',
    'AirCanada': 'false',
    'IncludeRail': 'false',
    'IncludeHotel': 'No hotel results',
    'IncludeVehicles': 'false',
    'datetimerequest': '1;9;113;19;17;44'
}


class website:

    def __init__(self):
        #session devine o instanta a obiectului cookielib
        self.host = 'demo.travelportuniversalapi.com'
        self.ua = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:23.0) Gecko/20100101 Firefox/23.0'  
        self.session = cookielib.CookieJar()
        pass

    def addHeaders(self, url, request):
        request.add_header('User-Agent', self.ua)
        request.add_header('Referer', url)

    def get(self):
        try:
            #this varies every 20 minutes
            url = 'http://demo.travelportuniversalapi.com/(S(0q01avjrrcbsam3li304lx3l))/Search'
            data = None
            headers = {'User-Agent': self.ua}
            request = urllib2.Request(url, data, headers)
            self.session.add_cookie_header(request)
            response = urllib2.urlopen(request)
            self.session.extract_cookies(response, request)
            url = response.geturl()
            print url

            data = {'From': 'lhr',
                    'To': 'ams',
                    'Departure': '9/4/2013',
                    'Return': '9/6/2013'}
            basicData.update(data)

            # Updating Session
            request = urllib2.Request(url+'/SetSearchTermsInSession', data=urllib.urlencode(basicData))
            self.addHeaders(url, request)
            self.session.add_cookie_header(request)
            response = urllib2.urlopen(request, timeout=30)
            # Doing the search
            request = urllib2.Request(url+'/SearchLowFare', data=urllib.urlencode(basicData))
            self.addHeaders(url, request)
            self.session.add_cookie_header(request)
            response = urllib2.urlopen(request, timeout=30)
            self.session.extract_cookies(response, request)

            # Going to last page
            firstPage = response.read()
            soup = BeautifulSoup(firstPage)
            lastPageDiv = soup.findAll('div', {"id": "tablePagination"})[-1]
            lastPageIndex = lastPageDiv.find('div').text
            request = urllib2.Request(url+'/SearchLowFarePage', data=urllib.urlencode({'pageIndex': lastPageIndex}))
            self.addHeaders(url, request)
            self.session.add_cookie_header(request)
            response = urllib2.urlopen(request, timeout=30)
            self.session.extract_cookies(response, request)

            #clicking the law fare response button
            newUrl = url + '/GetSearchLowFareResponse'
            print newUrl
            request = urllib2.Request(newUrl, data=urllib.urlencode({}))
            self.addHeaders(url, request)
            self.session.add_cookie_header(request)
            response = urllib2.urlopen(request, timeout=30)
            self.session.extract_cookies(response, request)

            xml = response.read()
            soup = BeautifulSoup(xml)
            result = soup.find('textarea').contents[0]
            print result

        except urllib2.URLError as e:
            print >> sys.stderr, e
            return None

rt = website()
rt.get()
