"""
Written by Brian Li Ong
Date: 07/09/2021
This script takes a PDF file and performs text preprocessing to transform the document into a document term matrix
(TDM). NLP techniques applied will be word tokenization, removal or stopwords, named entity removal, lemmatization,
parts of speech (POS) tagging, phrase chunking to extract noun and verb phrases. The output will be a plain text file
containing all extracted phrase tokens.
"""

from pdfminer.high_level import extract_text
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
import nltk.tag


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
    with open('Data Viz 1 Report.pdf', 'rb') as f:
        text = extract_text(f)


if __name__ == '__main__':
    main()