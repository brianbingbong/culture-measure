"""
Written by Brian Li Ong
Date: 07/09/2021
This script takes a txt file containing paths to input files to be preprocessed into document term matrices (TDM). NLP
techniques applied will be word tokenization, punctuation removal, removal or stopwords, named entity removal,
lemmatization, case normalisation, parts of speech (POS) tagging, phrase chunking to extract noun and verb
phrases. The output will be a plain text file.
containing all extracted phrase tokens.

TODO: replace numbers with 0 instead of nothing??? maybe
"""

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk import Tree
import nltk.tag
import sys
import logging
from pdfminer.high_level import extract_text
import re
import csv
import os

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
    with open(sys.argv[1], 'r') as f:
        artefactFiles = f.read().splitlines()

    # set up nlp preprocessing
    stopWords = set(stopwords.words("english"))
    lemmatizer = WordNetLemmatizer()
    chunkGrammarNp = """NP: {<DT>?<JJ>*<NN>}    #Noun Phrases """
    chunkGrammarVp1 = """VP: {<VB.*><DT>?<JJ>*<NN><RB.?>?}   #Verb Phrase type 1"""
    chunkGrammarVp2 = """VP: {<DT>?<JJ>*<NN><VB.*><RB.?>?}   #Verb Phrase type 2"""
    chunkPhraseParserNp = nltk.RegexpParser(chunkGrammarNp)
    chunkPhraseParserVp1 = nltk.RegexpParser(chunkGrammarVp1)
    chunkPhraseParserVp2 = nltk.RegexpParser(chunkGrammarVp2)

    for artefact in artefactFiles:
        with open(artefact, 'rb') as inFile:
            fileName = artefact[:-4].split('/')[1]

            # ensure that each file is a pdf or txt
            if artefact[-4:] == '.pdf':
                text = extract_text(inFile)
            elif artefact[-4:] == '.txt':
                text = inFile.read()
            else:
                logger.error(f'{artefact} file type not supported, ensure files are of type .pdf or .txt')
                exit(1)

        logger.info(f'Processing {artefact}...')

        # remove punctuation
        # credit to: https://stackoverflow.com/questions/265960/best-way-to-strip-punctuation-from-a-string
        text = re.sub(r'[^\w\s]', '', text)
        # remove numbers
        text = re.sub(r'[0-9]', '', text)
        # remove underscores
        text = text.replace('_', '')

        wordTokensRaw = word_tokenize(text)
        wordTokensLemmatized = [lemmatizer.lemmatize(word) for word in wordTokensRaw]
        wordTokens = [word for word in wordTokensLemmatized if word not in stopWords]

        namedEntitiesTree = nltk.ne_chunk(nltk.pos_tag(wordTokens))

        # named entity extraction and removal
        # credit to: https://stackoverflow.com/questions/43742956/fast-named-entity-removal-with-nltk
        namedEntities = set([leaf[0][0] for leaf in namedEntitiesTree if type(leaf) == nltk.Tree])
        wordTokens = [leaf[0].lower() for leaf in namedEntitiesTree if type(leaf) != nltk.Tree]

        # create chunk tree
        phraseChunkTreeNp = chunkPhraseParserNp.parse(nltk.pos_tag(wordTokensRaw))
        phraseChunkTreeVp1 = chunkPhraseParserVp1.parse(nltk.pos_tag(wordTokensRaw))
        phraseChunkTreeVp2 = chunkPhraseParserVp2.parse(nltk.pos_tag(wordTokensRaw))

        # extract text for noun and verb phrases and join together all phrases into a single array
        phraseTokens = extractChunkText(phraseChunkTreeNp, 'NP', namedEntities) + \
                       extractChunkText(phraseChunkTreeVp1, 'VP', namedEntities) + \
                       extractChunkText(phraseChunkTreeVp2, 'VP', namedEntities)

        # construct words dtm
        wordsDtm = dict.fromkeys(wordTokens, 0)
        for word in wordTokens:
            wordsDtm[word] += 1

        # construct phrases dtm
        phrasesDtm = dict.fromkeys(phraseTokens, 0)
        for phrase in phraseTokens:
            phrasesDtm[phrase] += 1

        # create a DTMs directory if non existent
        if not os.path.exists('DTMs'):
            print("yep")
            os.makedirs('DTMs')

        # write output to files
        with open('DTMs/' + fileName + '-words.csv', 'w') as outFile:
            fieldnames = ['token', 'frequency']
            writer = csv.DictWriter(outFile, fieldnames=fieldnames)

            writer.writeheader()
            for word in wordsDtm.keys():
                writer.writerow({'token': word,
                                 'frequency': wordsDtm[word]})

            logger.info(f'Word tokens for {artefact} written to DTMs/{fileName}-words.csv')

        with open('DTMs/' + fileName + '-phrases.csv', 'w') as outFile:
            fieldnames = ['token', 'frequency']
            writer = csv.DictWriter(outFile, fieldnames=fieldnames)

            writer.writeheader()
            for phrase in phrasesDtm.keys():
                writer.writerow({'token': phrase,
                                 'frequency': phrasesDtm[phrase]})
            logger.info(f'Phrase tokens for {artefact} written to DTMs/{fileName}-phrases.csv')


def extractChunkText(chunkTree, chunkType, namedEntities):
    # get the leaves of the all noun phrase subtrees into arrays
    # credit to https://stackoverflow.com/questions/52021855/nltk-linguistic-tree-traversal-and-extract-noun-phrase-np
    chunkLeaves = [subtree.leaves() for subtree in chunkTree if type(subtree) == Tree and subtree.label() == chunkType]

    NAMED_ENTITY_REPLACEMENT = 'xxx'

    # discard the POS tag for each word, join the words of each phrase array into a string
    for i in range(len(chunkLeaves)):
        for j in range(len(chunkLeaves[i])):
            chunkLeaves[i][j] = chunkLeaves[i][j][0].lower()
            # replace named entities with 'xxx'
            if chunkLeaves[i][j] in namedEntities:
                chunkLeaves[i][j] = NAMED_ENTITY_REPLACEMENT
        chunkLeaves[i] = " ".join(chunkLeaves[i])

    return chunkLeaves


if __name__ == '__main__':
    main()
