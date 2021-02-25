This pipeline currently has 3 sections:
1. Text extraction
2. Corpus compilation and cleaning
3. Experiments with external lexicons for cleaning and corpus analysis



It has been developed for use with multilingual teaching resources (Indonesian and English) but could prove
helpful with other multilingual data.

##
1. Text extraction  - convertToText.py
##
The text extraction section was created by Romi Hill (Appen) for Zara Maxwell-Smith (CoEDL).

It has primarily been created and tested on PDF files but can also handle .doc and possibly PNG and JPEG.
It uses OCR (Optical Character Recognition) so it takes a while for the script to process those kinds of files, but the output seems reasonably accurate.

For use with PDFs which contain embedded text & Word Files you may need to install the Python libraries docx2python, pdfplumber, and ArgumentParser.

If you have pip, just use the following on the command line (or however else you install python libraries):
pip3 install docx2python
pip3 install pdfplumber
pip3 install argparse

If your document requires the use of OCR (Optical Character Recognition) it uses a Python library "textract" which requires a number of additional source libraries to download.

If you have homebrew and pip, enter these commands in the command line:
brew cask install xquartz
brew install poppler antiword unrtf tesseract swig
pip3 install textract

It may take a while to download everything.

To use the script, use the following commands:
python3 convertToText.py sample_data outputDirectory

Output is saved in a folder that you name (e.g. output).
This will read all the files in sample_data, convert everything to .txt with stripped punctuation etc,
and save it with the same folder structure as sample_data in output.

It keeps new lines characters.
It doesn't deal with tables in .doc files very well.

You can also use -f to maintain formatting in the output, using:
python3 convertToText.py sample_data -f output
does the same as above, but maintains formatting - this feature is still under development.
It works for .docx files but not for PDFs just yet.

##
2. Corpus compilation and cleaning - createCleanCorpus.py
##

Takes all .txt files in a folder (including subfolders),
reads as a corpus and provides a few basic cleaning needs.
Created by Romi Hill (Appen) and Zara Maxwell-Smith (CoEDL).

This script was developed during a project to examine Indonesian teaching resources (The Indonesian Way).

It will not run as one program, but is intended to step through a new corpus.
As you become familiar with the noise in your data you may wish to ignore some sections
or adapt others for a specific problem.

The initial section has broad sweep cleaning functionality, narrowing into specific tasks.

The section '''Cleaning after manual annotation''' writes a list of corpus types to csv file for manual annotation.
The csv file can then be manually annotated and read back in to remove/alter specific strings.

Some sections are useful in cleaning any corpus (lowercasing, numeral identification, etc.) but others
are very specific to working with Indonesian or to working with language teaching resources, or both.

The scripts can be used in conjunction with TIW_Experiments.py to remove dominant languages from your corpus.
This helps to reveal noise as well as other languages present in the corpus.

##
3. Experiments with external lexicons for cleaning and corpus analysis - TIW_Experiments.py
##

Compares the corpus (thus far used with a set of Indonesian teaching resources)
to English, Indonesian, Javanese, Sundanese lexicons.
Uses NLTK packages to produce word frequency and frequency distribution plots.
Created by Zara Maxwell-Smith.

Lexicons are drawn from a range of sources. Sorted by language:

##ENGLISH

CMU pronunciation dictionary
http://www.speech.cs.cmu.edu/cgi-bin/cmudict?in=complex

Australian English pronunciation dictionary
https://github.com/twocs/australian-lexicon/find/master

dict/words system file
from Mac system file

##INDONESIAN

Bahasa Wordnet
https://sourceforge.net/p/wn-msa/tab/HEAD/tree/trunk/wn-msa-all.tab

Kamus Alay (slang and formal translations are written into different lexicons)
https://github.com/nasalsabila/kamus-alay/blob/master/colloquial-indonesian-lexicon.csv

Korpus Indonesia
https://korpusindonesia.kemdikbud.go.id

##JAVANESE

Google Javanese data
https://github.com/google/language-resources/blob/master/jv/data/lexicon.tsv

##SUNDANESE

Google Sundanese data
https://github.com/google/language-resources/blob/master/su/data/lexicon.tsv