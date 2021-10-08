# culture-measure
This project aims to measure organisational culture of companies through
application of machine learning and NLP to process publicly available
organisation artefacts and company reviews.

## Usage

### Data filtering
The data filtering scripts can filter two types of data.
1. Textual documents: filter to only include paragraphs that contain at least one specified keyword
2. CSV documents: filter to only include rows that contain at least one specified keyword in given fields
   1. To modify these fields, open the source code of the `filter_reviews` script to modify the constant defining them

Both scrips take two input arguments:
1. A `.txt` file containing a path to each artefact to be filtered on separate lines. Here is an example:
```
artefacts/artefact1.txt
artefacts/artefact2.pdf
artefacts/artefact2.txt
```
2. A `.txt` file containing all filter words on separate lines. Here is an example:
```
friendly
toxic
happy
```

#### Text documents
All artefacts must be in `.pdf` or `.txt` format.  
To run the `filter_reports.py` script, execute: `python filter_reports.py <filePaths.txt> <filter_keywords.txt>`  
Output files will be written into a `filtered_artefacts/reports` directory.

#### Glassdoor Reviews
All artefacts must be in `.csv` format and must contain the columns referenced in the code of the script.  
To run the `filter_reviews.py` script, execute: `python filter_reviews.py <filePaths.txt> <filter_keywords.txt>`  
Output files will be written into a `filtered_artefacts/reviews` directory.

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
