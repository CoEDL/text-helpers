#!/usr/bin/env python3

"""
Takes a word or PDF document and converts it into a text file
Created by Romi Hill (Appen) for Zara Maxwell-Smith (CoEDL)
"""

# ----- LIBRARIES ----- #
from argparse import ArgumentParser
import os
import re
import sys

from docx2python import docx2python
import unicodedata
import subprocess
import pdfplumber
import textract
# ---------------------------------------------------------------------- #

# ----- PRE-DEFINED CONSTANTS ----- #

LIGATURES = {0xFB00: u'ff',
             0xFB03: u'ffi',
             0xFB04: u'ffl',
             0xFB01: u'fi',
             0xFB02: u'fl',
             0x000C: u'\n',
             0x008D: u'\n',
             0x008F: u'\n',
             0x0090: u'\n',
             0x0082: u'\n',
             0x0081: u'\n',
             0x008a: u'\n',
             0x0089: u'\n',
             0x0088: u'\n',
             0x0087: u'\n',
             0x0086: u'\n',
             0x0085: u'\n',
             0x0084: u'\n',
             0xF08D: u'',
             0xF08F: u'',
             0xF090: u'',
             0xF082: u'',
             0xF081: u'',
             0xF08a: u'',
             0xF089: u'',
             0xF088: u'',
             0xF087: u'',
             0xF086: u'',
             0xF085: u'',
             0xF084: u''}

# ---------------------------------------------------------------------- #

# ----- HELPER FUNCTIONS ----- #


def readPDFFile(inputFile):
    """
    Read PDF into strings using textract
    PDF can be encoded with text or not (i.e. an image)
    """

    # extract the text from PDF
    doc = textract.process(inputFile, method='pdftotext').decode("utf-8")
    # if there's no text, then doc should just consist of white spaces
    # it might have some pesky characters like page breaks or line breaks,
    # which is why we can't assume doc is an empty string
    if doc.isspace():
        # use OCR to try to convert the characters in the file into a string
        doc = textract.process(inputFile, method='tesseract', language='eng').decode("utf-8")

    return doc

# ---------------------------------------------------------------------- #


def readPDFFile_old(inputFile):
    """
    Old function to read PDF into strings.
    This function uses pdfplumber which is easier to install than textract.
    If textract cannot be install, use this instead
    """

    # create an empty string which will store the text in the pdf 
    doc = ''
    with pdfplumber.open(inputFile) as inFile:
        # read in the string by page
        for page in inFile.pages:
            # try to extract text from the pdf
            try:
                doc = doc + page.extract_text()
            # if that doesn't work, end the function. The script can't handle these kinds of files
            except:
                print('\tPDF is unreadable')
                inFile.close()
                return doc
        # tell Python to close the input file. 
        inFile.close()
    return doc

# ---------------------------------------------------------------------- #


def listOfFiles(inputFolder):
    """
    Amended from https://thispointer.com/python-how-to-get-list-of-files-in-directory-and-sub-directories/
    Gets a list of files from inputFolder, including files in subfolders
    """

    # get all files/folders in current folder
    filesInDir = os.listdir(inputFolder)
    # create empty list which will contain all files
    allFiles = []
    # iterate over every file/folder in the directory
    for entry in filesInDir:
        # get the full path name of the file/folder we're at
        fullPath = os.path.join(inputFolder, entry)
        # Test whether the current entry is a directory
        if os.path.isdir(fullPath):
            # it is a directory, so get the all the files within this directory and add it to the list of files
            allFiles = allFiles + listOfFiles(fullPath)
        else:
            # it is not a directory, so it must be a file. Add it to the list
            allFiles.append(fullPath)

    # returns a list of all files with the inputFolder and subfolders within that          
    return allFiles

# ---------------------------------------------------------------------- #


def readWithFormatting(files, inputFolderName, outputFolderName):
    """
    Converts files into .txt
    Maintains formatting as much as possible
    """
    
    # go over every file in list containing all files
    for inputFile in files:
        doc = ''
        # get the full name and the extension of the files
        fileName, fileExtension = os.path.splitext(inputFile)
        # direct the new file name to the output folder by replacing the input folder name to the output folder name
        outputPathFileName = fileName.replace(inputFolderName, outputFolderName)
        # get the output file path (not including the filename)
        outputPath = os.path.dirname(outputPathFileName)

        # check whether the output path exists
        if not os.path.exists(outputPath):
            # if it doesn't, create it
            os.makedirs(outputPath)

        if fileExtension == '.docx':
            print('Processing: {}'.format(inputFile))
            # uses docx2python for now, since it's probably easier to keep the formatting consistent later on
            doc = docx2python(inputFile)
            doc = doc.text
            # uses regex to replace repeated new lines into one
            doc = re.sub(r'\n\n*', '\n', doc)
            
        elif fileExtension == '.doc':
            print('Processing: {}'.format(inputFile))
            doc = textract.process(inputFile).decode("utf-8")
            # uses regex to replace repeated new lines into one newline
            doc= re.sub(r'\n\n*', '\n', doc)

        elif fileExtension == '.pdf':
            print('Processing: {}'.format(inputFile))
            # read in the pdf file as a string
            # this is a bit more complicated so it has its own function
            doc = readPDFFile(inputFile)   

        elif fileExtension == '.png' or fileExtension == '.jpeg' or fileExtension == '.jpg':
            print('Processing: {}'.format(inputFile))
            # uses OCR to extract the text
            doc = textract.process(inputFile, method='tesseract', language = 'eng+ind').decode("utf-8")

        if doc:
            # standardise the string (e.g. convert ligatures, other encoding issues)
            doc = doc.translate(LIGATURES)
            # save the string as the file name + .txt
            newFileName = outputPathFileName + '.txt'
            with open(newFileName, 'w') as outFile:
                outFile.write(doc)
                outFile.close()

# ---------------------------------------------------------------------- #


def readWithNoFormatting(files, inputFolderName, outputFolderName):
    """
    Converts files into .txt
    Strips punctuations and multiple new lines
    """

    # go over every file in list containing all files
    for inputFile in files:
        doc = ''
        # get the full name and the extension of the files
        fileName, fileExtension = os.path.splitext(inputFile)
        # skip hidden files
        if not fileExtension:
            continue
        # store the output path with filename
        outputPathFileName = fileName.replace(inputFolderName, outputFolderName)
        # store the output path without filename
        outputPath = os.path.dirname(outputPathFileName)

        # create path to output folder if it doesn't exist
        if not os.path.exists(outputPath):
            os.makedirs(outputPath)

        # prints to terminal which file is being processed
        # will be useful for debugging if there's an error on one of the files
        print('Processing: {}'.format(inputFile))

        # use textract to extract text
        # process() returns a byte object, so we need to decode it into a string using .decode("utf-8")
        # if you're getting funny symbols, we might need to change the decoder
        doc = textract.process(inputFile).decode("utf-8")
        # if there's no text, then doc should just consist of white spaces.
        # it might have some pesky characters like page breaks or line breaks,
        # which is why we can't assume doc is an empty string
        if doc.isspace():
            # use OCR to try to convert the characters in the file into a string
            doc = textract.process(inputFile, method='tesseract', language = 'eng+ind').decode("utf-8")

        # only keep word characters
        doc = re.sub(r'[^\w\s]','',doc)

        # remove multiple new lines
        doc = re.sub(r'\n\n*', '\n', doc)

        doc = doc.translate(LIGATURES)
            # save the string as the file name + .txt
        newFileName = outputPathFileName + '.txt'

        # store the new file name with .txt
        newFileName = outputPathFileName + '.txt'
        # write and save the file
        with open(newFileName, 'w') as outFile:
            outFile.write(doc)
            outFile.close()

# ---------------------------------------------------------------------- #

# ---------------------------------------------------------------------- #
# ----- MAIN FUNCTION ----- #


def main():
    parser = ArgumentParser(description="This script will help extract text from pdf files.")
    # assuming people run this from pwd, so use relative paths for simplicity
    parser.add_argument('-i', '--input_dir', help='Directory of pdf files to read', type=str, default='./input')
    parser.add_argument('-o', '--output_dir', help='Where the text files will be saved', type=str, default='./output')
    parser.add_argument('-f', '--formatting', help='Keep formatting of tables etc?', type=bool, default=True)
    args = parser.parse_args()
    try:
        inputFolderName = args.input_dir
        outputFolderName = args.output_dir
        keepFormatting = args.formatting
    except Exception:
        parser.print_help()
        sys.exit(0)

    if not os.path.exists(outputFolderName):
        os.makedirs(outputFolderName)

    # get list of files from inputFolder
    files = listOfFiles(inputFolderName)

    if keepFormatting:
        readWithFormatting(files, inputFolderName, outputFolderName)
    else:
        readWithNoFormatting(files, inputFolderName, outputFolderName)

# ---------------------------------------------------------------------- #


if __name__ == '__main__':
    main()
