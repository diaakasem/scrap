import csv
import time
data = []
fieldnames=[]

def formatDate(oldDate):
    fromFormat = '%m/%d/%y'
    toFormat = '%Y-%m-%d'
    return time.strftime(toFormat, time.strptime(oldDate, fromFormat))

def updateRows(data):
    lastRow = None
    for row in data:
        if not lastRow:
            # fieldnames = row.keys()
            lastRow = row
            row['Order Date'] = formatDate(row['Order Date'])
            continue

        if row['Supplier'] == lastRow['Supplier'] \
                and row['Destination'] == row['Destination'] \
                and row['Order Reference'] == row['Order Reference']:
            row['Supplier'] = ''
            row['Order Date'] = ''
            row['Order Reference'] = ''
            row['Destination'] = ''
        else:
            row['Order Date'] = formatDate(row['Order Date'])
            lastRow = row
    return data


def main():
    with open('2009_PollingStations.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile)
        fieldnames = reader.next()

    with open('input.csv', 'rb') as csvfile:
        rows =  csv.DictReader(csvfile, dialect='excel', delimiter=',')

        for row in rows:
            data.append(row)

    rows = updateRows(rows)

    with open('output.csv', 'wb') as csvfile:
        output =  csv.DictWriter(csvfile, delimiter=',', fieldnames=fieldnames)

        output.writeheader()
        for row in data:
            output.writerow(row)

if __name__ == "__main__":
    main()
