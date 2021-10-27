"""
This script joins together text fields of Glassdoor review data in a csv sheet into a single text field.
"""

import logging
import re
import csv
import os
import sys

JOINED_REVIEWS_DIRECTORY = 'joined_reviews'
JOIN_FIELDS = ['pros', 'cons', 'review_title']
JOINED_TEXT_FIELD = 'review_text'

# set up logger
LOGGER = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

# suppress logger for pdfminer
pdfminerLogger = logging.getLogger('pdfminer')
pdfminerLogger.setLevel(logging.ERROR)

def main():
    # check that the right number of arguments are given in command line
    arguments = len(sys.argv) - 1
    if (arguments != 1):
        LOGGER.error("Invalid number of arguments")
        LOGGER.error("Expected :  " + sys.argv[0] + " <files>")
        exit(1)

    # get the file names of artefacts to be read
    with open(sys.argv[1], 'r') as f:
        artefactFiles = f.read().splitlines()

    with open(artefactFiles[0], 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            columnNames = row
            break

    for field in columnNames:
        if field in JOIN_FIELDS:
            columnNames.remove(field)

    columnNames.append(JOINED_TEXT_FIELD)

    for artefact in artefactFiles:
        fileName = artefact[:-4].split('/')[-1]
        if artefact[-4:] != '.csv':
            LOGGER.error(f'{artefact} file type not supported, ensure file is of .csv type')
            exit(1)

        joinedReviews = []

        with open(artefact, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                newRow = {}
                joinedReview = ''
                for field in row.keys():
                    if field in JOIN_FIELDS:
                        joinedReview += f'{row[field]}\n'
                    else:
                        newRow[field] = row[field]
                newRow[JOINED_TEXT_FIELD] = joinedReview
                joinedReviews.append(newRow)

        # create a joined reviews directory if it does not exist
        if not os.path.exists(JOINED_REVIEWS_DIRECTORY):
            LOGGER.info('Creating directory for joined reviews')
            os.makedirs(JOINED_REVIEWS_DIRECTORY)

        # write output to files
        with open(f'{JOINED_REVIEWS_DIRECTORY}/{fileName}-joined.csv', 'w') as outFile:
            writer = csv.DictWriter(outFile, fieldnames=columnNames)
            LOGGER.info(f'Writing joined review into {fileName}-joined.csv')
            writer.writeheader()
            for review in joinedReviews:
                writer.writerow(review)

    exit(0)


if __name__ == '__main__':
    main()