#!/usr/bin/python3
#
# Copyright 5th March 2020
# Ben Foley ben@cbmm.io
# Zara Maxwell-Smith

# First stab at working out some scripts for extracting text from PDFs

import slate3k as slate
import re
import os
import nltk
import string

# Download punctuation data if we don't already have it
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    print("nltk punkt not found, downloading...")
    nltk.download('punkt')


# Use a handy method to output the results to files rather than printing to screen
def write_file(filename, content):
    path = os.path.join('output', filename)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content)
    print("wrote to", filename)

# Get the raw messy text from the PDF
# iterate all pdfs in the input dir

input_directory = 'input'

for file in os.listdir(input_directory):
    if not file.endswith(".pdf"):
        continue
    with open(os.path.join(input_directory, file), 'rb') as pdf_file:
        doc = slate.PDF(pdf_file)


    ### Formatting the text

    ## First approach to getting text into a working format
    # PDF format seems to have random single line breaks in middle of sentences
    # and uses double line breaks for paras.
    # This will replace single line breaks with spaces
    # preserving double breaks for paras.
    paragraphs_1 = doc[0]
    paragraphs_1 = paragraphs_1.replace('\n\n', '•').replace('\n', ' ').replace('•', '\r\n')
    write_file("paragraphs_1.txt", paragraphs_1)

    # ## Second approach to getting text into a working format
    # # This doesn't do anything about line breaks
    # # So it isn't accurate for sentence/para separation
    # paragraphs_2 = ' '.join(doc)
    # write_file("paragraphs_2.txt", paragraphs_2)


    # # So, let's use paragraphs_1 from here on as the source

    ### Generate a wordlist
    #
    # Tokenise the paras and gets rid of '\n'.
    # Tokens is an array, so make a str as well for str operations
    tokens = nltk.tokenize.word_tokenize(paragraphs_1)
    wordlist = '\n'.join(tokens)
    write_file("wordlist_1.txt", wordlist)


    # ### Cleaning the punctuation

    ## First approach subsets the array of tokens
    punctuation = [',','(',')','*', '**', '***', '****', '*****', '"', '“', '”']
    wordlist_clean_1 = [word for word in tokens if not word in punctuation]
    write_file("wordlist_clean_1.txt", '\n'.join(wordlist_clean_1))

    # Second approch uses regexp on the str, everything except words and spaces
    wordlist_clean_2 = re.sub(r'[^\w\s]', '', wordlist)
    write_file("wordlist_clean_2.txt", wordlist_clean_2)

    # Third approach, regexp with specific punct markss
    strip_pattern = r'[\.\-\?,()_*"“”:;!]'
    # use the third method with either the wordlist ...
    wordlist_clean_3 = re.sub(strip_pattern, '', wordlist)
    write_file("wordlist_clean_3.txt", wordlist_clean_3)
    # ... or the paragraph as input
    paragraphs_1_cleaned = re.sub(strip_pattern, '', paragraphs_1)
    write_file("paragraphs_1_clean.txt", paragraphs_1_cleaned)

    print("done")
