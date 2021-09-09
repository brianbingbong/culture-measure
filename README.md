# culture-measure
This project aims to measure organisational culture of companies through
application of machine learning and NLP to process publicly available
organisation artefacts.

## Usage

### Pre-processing
Add the path to each artefact into a plain `.txt` file, with each artefact
on a new line. All artefact documents must be in either `.pdf` or `.txt` format. 
Here is an example of its contents:  
```
artefacts/artefact1.txt
artefacts/artefact2.pdf
artefacts/artefact2.txt
```

To run the pre-processing script, execute: `python process_documents.py <filePaths.txt>`

What will be produced is for each document in the input `.txt` file, a 
`<document_name>-phrases.csv` and `<document_name>-words.csv` file 
will be created which count the frequency of noun and verb phrase tokens,
and word tokens respectively after processing. These will be placed into a 
`DTMs` directory.
