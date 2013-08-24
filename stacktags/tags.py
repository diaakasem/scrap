from bs4 import BeautifulSoup
import urllib2
import csv
import time


url = "http://stackoverflow.com/tags?page=%s&tab=popular"
data = []
outputFile = 'csvoutput.csv'
fields = ['name', 'description']
pagesCount = 998

def extractPage(url):
    page = urllib2.urlopen(url).read()
    soup = BeautifulSoup(page)
    for tds in soup.findAll('td', {'class': 'tag-cell'}):
        anchors = tds.find('a')
        excerpt = tds.find('div', {'class': 'excerpt'})
        if excerpt and excerpt.text:
            text = excerpt.text.encode('ascii', 'ignore')
        else:
            text = " "
            print "[ %s ] seem does not have a description" % anchors.text
        data.append({
            'name': anchors.text,
            'description': text
            })

def writeData(outputFile, data):
    with open(outputFile, 'wb') as csvfile:
        output = csv.DictWriter(csvfile, delimiter='\t', fieldnames=fields)
        output.writeheader()
        output.writerows(data)

def main():
    for i in range(1, pagesCount+1):
        print "Working on : %s" % i
        extractPage(url % str(i))
        time.sleep(1)
    print "Writing to disk."
    writeData(outputFile, data)
    print "Done."

if __name__ == '__main__':
    main()

