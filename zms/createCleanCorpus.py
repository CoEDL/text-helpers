#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Takes all .txt files in a folder (including subfolders),
reads as a corpus and provides a few basic cleaning needs.
Created by Romi Hill (Appen) and Zara Maxwell-Smith (CoEDL).
'''
# creates and loads file path
import os, os.path
import re
import csv


def listOfFiles(inputFolder):
    '''
    Amended from https://thispointer.com/python-how-to-get-list-of-files-in-directory-and-sub-directories/
    Gets a list of files from inputFolder, including files in subfolders
    '''
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


inputFolder = '/Volumes/Backup_Plus/Input/Output/'

# get list of files from inputFolder
files = listOfFiles(inputFolder)
allWordsList = []

    # go over every file in list containing all files
for inputFile in files:
        # get the full name and the extension of the files
    fileName, fileExtension = os.path.splitext(inputFile)
 
    if fileExtension == '.txt':
        #print('Processing: {}'.format(inputFile))
            #load into nltk and tokenize
        #text = nltk.data.load(inputFile, format='text')
        #tokens = tokens + nltk.word_tokenize(text)
        #print('tokens thus far', len(tokens))
        with open(inputFile,'r') as inFile:
            print('Processing: {}'.format(inputFile))
            for line in inFile:
                for word in line.split():
                    allWordsList.append(word)  

len(allWordsList)

# create list of types in corpus for inspection

typesintext = set(allWordsList)

#print(allWordsList[395273:395373])
#print(allWordsList[0:100])

'''Clean characters from each end and within strings'''

# lowercase tokens

lowerTokens = [w.lower() for w in allWordsList]

# strips characters from front and back of tokens
# test list on next line
#x = ['makan.', '!saya', '$loss.more!#']

characters_to_remove = '“”"…!#$%&@()()*+,-./:;<=>➢?@[\]^_`{|}~•●•_«»✶’‘✓üûð☐'
strippedTokensList = []
splitTokensList = []

for token in lowerTokens:
    new_token = token.strip(characters_to_remove)
    strippedTokensList.append(new_token)

# splits tokens with a given character two words e.g. 'loss.more' with whitespace

removeFromBetween = './—–―;:<=>➢?@[\]^_`{|}~•●•_«»“”"…!#$%&@()()*+,'

for token in strippedTokensList:
    pattern = "[" + removeFromBetween + "]"
    new_token = re.sub(pattern, " ", token)
    # print(new_token)
    splitTokensList.append(new_token)

# splits any tokens that contain whitespace

splitRetokenizeList = [word for line in splitTokensList for word in line.split()]
types = set(splitRetokenizeList)

######################
'''Hyphens!!!! checkup'''

# creates listB of tokens in which there is a 'word-word' (char(45) hyphen used
# ord 8211, 8212,8213 are all hyphens also 45 (normal use)
# test list on next line
#b = ['sebelum―anda―kampus―ke―bersiap-siap―berangkat―harus―dulu','antara-------------dan', '--this-is', '9makan.', '64!saya', '8-no', '', 'eat/drink',]

#listB = [a for a in b if re.search('\w–\w', a)]

'''finds all tokens with a hyphen in them to check on cleaning process'''

hyphenList = ['–', '—', '-', '―']
hyphenTokens = []
#hyphenLegitTokens = []

for token in splitRetokenizeList:
    for hyphen in hyphenList:
        if hyphen in token:
            hyphenTokens.append(token)

# lists types in tokens for closer inspection

typesinhyphens = set(hyphenTokens)
hyphensSorted = sorted(typesinhyphens)

# inspect the unicode number using: 
#ord("-")

#######################


'''Numerals'''

# removes numerals from tokens

noNum = []
num = []

for token in splitRetokenizeList:
    if token.isdigit():
        num.append(token)
    else:
        noNum.append(token)

#typestest = set(noNum)

# remove exercise numbers with format digit-digit

stripExNum = []
exNum = []

for token in noNum:
    if not re.search('\d-\d', token):
        stripExNum.append(token)
    else:
        exNum.append(token)

# Another option
#stripExNum = [x for x in splitRetokenizeList if any(re.search('\d*-\d*', x) for c in x)]

#typestest = set(stripExNum)


# replace numerals with whitespace and retokenise on whitespace

stripNum = []

for token in stripExNum:
    new_token = re.sub("\d+", " ", token)
    stripNum.append(new_token)


stripNumRetok = [word for line in stripNum for word in line.split()]

'''Letters'''

# remove single letters except 'i' and 'a'

valid_singles = ['i', 'a']
stripExAlpha = []

for token in stripNumRetok:
    if token in valid_singles or len(token) >= 2:
        stripExAlpha.append(token)

'''Specific unwanted strings'''

# remove specific tokens using a list called inValid_tokens

inValid_tokens = ['ab', 'fj', 'bcefh', 'abce', 'acd', 'bcdeh']
final_tokens = []
discard = []

for token in stripExAlpha:
    if token in inValid_tokens:
        discard.append(token)
    else:
        final_tokens.append(token)

typesInFinal = set(final_tokens)



#############

'''Cleaning after manual annotation'''

        
'''Split manually marked strings that have a hyphen e.g. 'putih-white''''

splitHyphenList = []  

# create a list of strings to be split from manually cleaned list 
      
with open('/Users/zara/manRemnants.csv', 'r') as csvFile:
        csvReader = csv.reader(csvFile)
        for row in csvReader:
            if row[1] == '1':
                splitHyphenList.append(row[0])
        inFile.close()  

manHyphenSplit = []

# test list on next line
#t = ['udah-sudah', 'eat', 'anak-anak', 'ungu-purple']
                
for token in final_tokens:
    if token in splitHyphenList:
            pattern = "[" + '-' + "]"
            new_token = re.sub(pattern, " ", token)
            # print(new_token)
            manHyphenSplit.append(new_token)
    else:
        manHyphenSplit.append(token)

manHyphenSplit = [word for line in manHyphenSplit for word in line.split()] 

typesManHyphenSplit = set(manHyphenSplit)              
                  
        
'''Remove marked up strings from a csv'''

# create list of strings to be removed
manRemove = []
       
with open('/Users/zara/remnants_ann.csv', 'r') as csvFile:
        csvReader = csv.reader(csvFile)
        for row in csvReader:
            if row[2] == '1':
                manRemove.append(row[0])
        inFile.close()

# removes the list of strings from another list

manFinal_tokens = []    
discard = []

for token in manHyphenSplit:
    if token in manRemove:
        discard.append(token)
    else:
        manFinal_tokens.append(token)
        

#typesInManFinal = set(manFinal_tokens)


#######
###############
#######################

'''Write corpus to file'''
        
with open('manCleanTIW.txt', 'w') as outFile:
    outFile.write('\n'.join(manHyphenSplit))
    outFile.close()



######################
#############
########










'''Scraps that might be helpful when working with a new dataset'''
    

to clean: 
ü
    

û
      
ð

       
       
      



☐







'''Remove unneccessary variables to save memory'''

del lowerTokens
del strippedTokensList
del splitTokensList
del splitRetokenizeList
del noNum
del num
del stripExNum
del exNum
del stripNum
del stripNumRetok


del stripExAlpha

#############

'''Check for cleaning errors'''

variables = [splitRetokenizeList, noNum, stripExNum, stripNumRetok, stripExAlpha, final_tokens]        
checkLists = ['enari']

for step in variables:
    print('Checking:', step)
    for token in step:
        if token in checkLists:
            print(token, 'is in', step)

for token in step:
    if token in checkLists:
        print(token, 'is in', step)
        

#############

'''Scraps for checking things with existing wordlists'''

# Remove English from corpus.

engRemoved = []
eng = []

for word in final_tokens:
    if word not in allEnglishLex:
        engRemoved.append(word)
    else:
        eng.append(word)
        
# Search TIW for Javanese lexical items

javInTIW = []

for word in TIWlexicon:
    if word in googleJavLex:
        javInTIW.append(word)

print(javInTIW[200:300])
              

count = 0
for word in minus3Ind:
    if word == 'kliwon':
        count = count + 1
        #print('enari found')
    else:
        print('word not found')
