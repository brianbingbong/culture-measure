"""
This script filters Glassdoor review data in a csv file to exclude reviews which do not contain at least one of the
provided keywords in any of its text fields.
"""

import logging
import re
import csv
import os
import sys

FILTERED_TEXT_DIRECTORY = 'filtered_artefacts/reviews'
FILTER_FIELDS = ['pros', 'cons', 'advice_to_mgmt', 'review_title']

# set up logger
LOGGER = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

# suppress logger for pdfminer
pdfminerLogger = logging.getLogger('pdfminer')
pdfminerLogger.setLevel(logging.ERROR)

# credit: https://stackoverflow.com/questions/18682965/python-remove-last-line-from-string
def removeLastLineFromString(s):
    return s[:s.rfind('\n')]

def main():
    # check that the right number of arguments are given in command line
    arguments = len(sys.argv) - 1
    if (arguments != 2):
        LOGGER.error("Invalid number of arguments")
        LOGGER.error("Expected :  " + sys.argv[0] + " <files> <keywords>")
        exit(1)

    # get the keywords into an array
    with open(sys.argv[2], 'r') as f:
        keywords = f.read().splitlines()

    # get the file names of artefacts to be read
    with open(sys.argv[1], 'r') as f:
        artefactFiles = f.read().splitlines()

    with open(artefactFiles[0], 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            columnNames = row
            break

    for artefact in artefactFiles:
        fileName = artefact[:-4].split('/')[-1]
        if artefact[-4:] != '.csv':
            LOGGER.error(f'{artefact} file type not supported, ensure file is of .csv type')
            exit(1)

        filteredReviews = []

        with open(artefact, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                for field in FILTER_FIELDS:
                    keywordFound = False
                    for word in row[field].split(' '):
                        if re.sub(r'[^\w\s]', '', word).lower() in keywords:
                            filteredReviews.append(row)
                            keywordFound = True
                            break
                    if keywordFound:
                        break

        # remove the last 3 lines of the cons and advice to management because extra incorrect words are scraped
        for review in filteredReviews:
            review['cons'] = removeLastLineFromString(removeLastLineFromString(removeLastLineFromString(removeLastLineFromString(review['cons']))))
            review['advice_to_mgmt'] = removeLastLineFromString(removeLastLineFromString(removeLastLineFromString(removeLastLineFromString(review['advice_to_mgmt']))))

        # create a filtered reviews directory if it does not exist
        if not os.path.exists(FILTERED_TEXT_DIRECTORY):
            LOGGER.info('Creating directory for filtered reviews')
            os.makedirs(FILTERED_TEXT_DIRECTORY)

        # write output to files
        with open(f'{FILTERED_TEXT_DIRECTORY}/{fileName}-filtered.csv', 'w') as outFile:
            writer = csv.DictWriter(outFile, fieldnames=columnNames)
            LOGGER.info(f'Writing filtered review into {fileName}-filtered.csv')
            writer.writeheader()
            for review in filteredReviews:
                writer.writerow(review)

    exit(0)


if __name__ == '__main__':
    main()