# culture-measure
This project aims to measure organisational culture of companies through
application of machine learning and NLP to process publicly available
organisation artefacts and company reviews. After data filtering and pre-processing,
topic models are trained using STM on annual reports, and on Glassdoor reviews using
overall star ratings as a topical prevalence covariate.

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

### Data joining
The data joining script joins specified text fields in Glassdoor reviews into a single text field to enable
easier processing. Joined text will be placed into a new column in a `.csv` file called `review_text`.  
To specify the review fields to be joined, modify the `JOIN_FIELDS` constant within the file.  

To run the `join_review_text.py` script, execute: `python join_review_text.py <filePaths.txt>`. It is recommended
to run the join script post filtering.  
Output files will be written into a `joined_reviews/` directory


### STM Application
The `stm.r` script trains stm models based on a corpus provided on `line 8`. For example to train models on
Ericsson Glassdoor data, point `read.csv` to the directory containing the data 
`review_data = read.csv('./Dataset/Glassdoor_data/ericsson-filtered-joined.csv')`.
Refer to the [stm documentation](https://cran.r-project.org/web/packages/stm/vignettes/stmVignette.pdf) to modify the
base script to produce
the desired output of topical prevalence, topical content or covariate effect estimation charts. It is not
possible to create covariate effect estimation charts for Glassdoor reviews because there is no star rating.
