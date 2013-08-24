import csv
import re
data = []
fieldnames=[]

inputFile = '2009_PollingStations.csv'
outputFile = 'output.csv'
def main():
    with open(inputFile, 'rb') as csvfile:
        reader = csv.reader(csvfile)
        fieldnames = reader.next()

        count = 0
        for row in reader:
            newRow = []
            for value in row:
                value = value.strip()
                value = value.replace('\r', ' ')
                value = value.replace('\n', ' ')
                value = value.replace(b'\xa0', ' ')
                value = re.sub('\s+', ' ', value)
                newRow.append(value)
            count += 1
            print count
            data.append(newRow)

    with open(outputFile, 'wb') as csvfile:
        output =  csv.writer(csvfile, delimiter=',')

        print "Writing"
        output.writerow(fieldnames)
        output.writerows(data)
        print "Done"

if __name__ == "__main__":
    main()
