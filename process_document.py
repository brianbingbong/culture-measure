"""
Written by Brian Li Ong
Date: 07/09/2021
This script takes a PDF file and performs text preprocessing to transform the document into a document term matrix
(TDM). NLP techniques applied will be word tokenization, punctuation removal, removal or stopwords, named entity
removal, lemmatization, case normalisation, parts of speech (POS) tagging, phrase chunking to extract noun and verb
phrases. The output will be a plain text file.
containing all extracted phrase tokens.
"""

from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import nltk.tag
import sys
import logging
from pdfminer.high_level import extract_text
import re
import string

ARTEFACT_FILES = "files.txt"

# set up logger
logger = logging.getLogger()
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)


# Package names needed: 'averaged_perceptron_tagger', 'punkt', 'maxent_ne_chunker', 'words'
def downloadNLTKPackage(packageName):
    import nltk
    import ssl

    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context

    nltk.download(packageName)


def main():
    # check that the right number of arguments are given in command line
    arguments = len(sys.argv) - 1
    if (arguments != 1):
        logger.error("Invalid number of arguments")
        logger.error("Expected :  " + sys.argv[0] + " <sheetID>")
        exit(1)

    # get the file names of artefacts to be read
    with open('files.txt', 'r') as f:
        artefactFiles = f.read().splitlines()

    # set up nlp preprocessing
    stopWords = set(stopwords.words("english"))
    lemmatizer = WordNetLemmatizer()
    chunkGrammar = r"""
      NP: {<DT|JJ|NN.*>+}          # Chunk sequences of DT, JJ, NN
      VP: {<VB.*><NP|PP|CLAUSE>+$} # Chunk verbs and their arguments
      """
    chunkPhraseParser = nltk.RegexpParser(chunkGrammar)

    for artefact in artefactFiles:
        with open(artefact, 'rb') as f:
            text = extract_text(f)
            # remove punctuation
            # credit to: https://stackoverflow.com/questions/265960/best-way-to-strip-punctuation-from-a-string
            text = re.sub(r'[^\w\s]', '', text)
            # remove numbers
            text = re.sub(r'[0-9]', '', text)
            # remove underscores
            text = text.replace('_', '')

            wordTokensRaw = word_tokenize(text)

            wordTokens = [word for word in wordTokensRaw if word not in stopWords]
            wordTokens = [lemmatizer.lemmatize(word) for word in wordTokens]

            # named entity removal
            # credit to: https://stackoverflow.com/questions/43742956/fast-named-entity-removal-with-nltk
            namedEntitiesTree = nltk.ne_chunk(nltk.pos_tag(wordTokens))
            wordTokens = [leaf[0] for leaf in namedEntitiesTree if type(leaf) != nltk.Tree]
            print(wordTokens)

            # # create chunk tree
            # phraseChunkTree = nltk.RegexpParser(chunkGrammar).parse(nltk.pos_tag(wordTokens))
            #
            # phraseChunkTree.draw()
            #
            # # extract noun and verb phrases
            # wordTokens = [leaf[0] for leaf in phraseChunkTree if type(leaf) != nltk.Tree]
            #
            # print(wordTokens)


if __name__ == '__main__':
    main()