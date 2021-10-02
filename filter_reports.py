"""
TODO: Write some documentation in readme, write a description of the file at the top
"""

import copy
import logging
import re
from pdfminer.high_level import extract_text
import os
import sys

FILTERED_TEXT_DIRECTORY = 'filtered_artefacts/reports'

# set up logger
LOGGER = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

# suppress logger for pdfminer
pdfminerLogger = logging.getLogger('pdfminer')
pdfminerLogger.setLevel(logging.ERROR)

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

    for artefact in artefactFiles:
        fileName = artefact[:-4].split('/')[-1]
        if artefact[-4:] == '.pdf':
            with open(artefact, 'rb') as inFile:
                text = extract_text(inFile)
        elif artefact[-4:] == '.txt':
            with open(artefact, 'r') as inFile:
                text = inFile.read()
        else:
            LOGGER.error(f'{artefact} file type not supported, ensure files are of type .pdf or .txt')
            exit(1)

        filteredParagraphs = []
        paragraphs = text.split('\n\n')
        for i in range(len(paragraphs)):
            paragraph = copy.copy(paragraphs[i])
            paragraph = paragraph.replace('\n', ' ')
            paragraph = paragraph.replace('  ', ' ')
            paragraphWords = paragraph.split(' ')
            for word in paragraphWords:
                if re.sub(r'[^\w\s]', '', word).lower() in keywords:
                    filteredParagraphs.append(paragraph)
                    break

        # create a filtered reports directory if it does not exist
        if not os.path.exists(FILTERED_TEXT_DIRECTORY):
            LOGGER.info('Creating directory for filtered reports')
            os.makedirs(FILTERED_TEXT_DIRECTORY)

        # write output to files
        with open(f'{FILTERED_TEXT_DIRECTORY}/{fileName}-filtered.txt', 'w') as outFile:
            LOGGER.info(f'Writing filtered report into {fileName}-filtered.csv')
            for paragraph in filteredParagraphs:
                outFile.write(paragraph + '\n')

    exit(0)


if __name__ == '__main__':
    main()