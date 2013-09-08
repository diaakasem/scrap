import csv
import time
data = []

def formatDate(oldDate):
    fromFormat = '%m/%d/%Y'
    toFormat = '%Y-%m-%d'
    print oldDate
    return time.strftime(toFormat, time.strptime(oldDate, fromFormat))

def monthFormatDate(oldDate):
    fromFormat = '%m/%d/%Y'
    toFormat = '%m/%Y'
    return time.strftime(toFormat, time.strptime(oldDate, fromFormat))

def updateRows(data):
    rows = []
    for row in data:
        newRow = {}
        newRow['Date'] = formatDate(row['date'])

        try:
            credit = int(row['credit'])
        except Exception:
            credit = float(row['credit'])

        if credit > 0:
            newRow['Entries / Debit'] = ''
            newRow['Entries / Credit'] = str(credit)
        else:
            newRow['Entries / Debit'] = str(-credit)
            newRow['Entries / Credit'] = ''

        newRow['Journal'] = 'Bank'
        newRow['Entries / Name'] = row['bank_name']
        newRow['Entries / Account'] = '10002 Bank'
        newRow['Period'] = monthFormatDate(row['date'])
        rows.append(newRow)
    return rows

def main():

    input_fieldnames = ['date', 'credit', 'astrisk', 'empty', 'bank_name']
    with open('raw.csv', 'rb') as csvfile:
        rows = csv.DictReader(csvfile, dialect='excel', delimiter=',', fieldnames=input_fieldnames)

        for row in rows:
            data.append(row)

    rows = updateRows(data)

    output_fieldnames = ['Date', 'Entries / Debit', 'Entries / Credit', 'Journal', 'Entries / Name', 'Entries / Account', 'Period']
    with open('output.csv', 'wb') as csvfile:
        output = csv.DictWriter(csvfile, delimiter=',', fieldnames=output_fieldnames)

        output.writeheader()
        for row in rows:
            output.writerow(row)

if __name__ == "__main__":
    main()
