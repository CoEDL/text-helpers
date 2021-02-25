#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Zara
"""

#############################################################

'''Compares Indonesian teaching resources to English, Indonesian, Javanese, Sundanese lexicons
Created by Zara Maxwell-Smith'''

######### Read in various lexicons. English, Indonesian, Javanese, Sundanese.

import csv

# create list of words from system dict/words file

engTokens = []

with open('/usr/share/dict/words','r') as inFile:
            for line in inFile:
                for word in line.split():
                    engTokens.append(word)
            inFile.close()

engTokens = [w.lower() for w in engTokens]

# create list of words from CMU pronunciation dictionary
# http://www.speech.cs.cmu.edu/cgi-bin/cmudict?in=complex

engCMUTokens = []

with open('/Volumes/Backup_Plus/TIW_Experiments/cmudict-0.7b.txt', 'r', encoding='latin-1') as inFile:
    for line in inFile:
        engCMUTokens.append(line.split()[0])
    inFile.close()

engCMUTokens = [w.lower() for w in engCMUTokens]

# create list of words from Australian English pronunciation dictionary
#https://github.com/twocs/australian-lexicon/find/master

engAusTokens = []

with open('/Volumes/Backup_Plus/TIW_Experiments/australian-english-lexicon.txt', 'r', encoding='latin-1') as inFile:
    for line in inFile:
        engAusTokens.append(line.split()[0])
    inFile.close()

engAusTokens = [w.lower() for w in engAusTokens]


# creates a list of English from marked up strings in a csv to be removed

manEngRemove = []
       
with open('/Users/zara/remnants_ann.csv', 'r') as csvFile:
        csvReader = csv.reader(csvFile)
        for row in csvReader:
            if row[2] == '1':
                manEngRemove.append(row[0])
        inFile.close()


# create lists of words from Bahasa Wordnet .tab file
#https://sourceforge.net/p/wn-msa/tab/HEAD/tree/trunk/wn-msa-all.tab

wordnetInd = []

with open('/Volumes/Backup_Plus/TIW_Experiments/wn-msa-all.tab', 'r') as tsvFile:            
        tsvReader = csv.reader(tsvFile, delimiter='\t')
        for row in tsvReader:
            wordnetInd.append(row[3])
        inFile.close()

#print(wordnetInd[(len(wordnetInd)-2):])            
#print(wordnetInd[0:1])
    
wordnetInd = [w.lower() for w in wordnetInd]
  
# create lists of words from CSV of slang Indonesian
#https://github.com/nasalsabila/kamus-alay/blob/master/colloquial-indonesian-lexicon.csv

collIndInternet = []
collIndInternetFormal = []
        
with open('/Volumes/Backup_Plus/TIW_Experiments/colloquial-indonesian-lexicon.csv', 'r') as csvFile:
        csvReader = csv.reader(csvFile)
        for row in csvReader:
            collIndInternet.append(row[0])
            collIndInternetFormal.append(row[1])
        inFile.close()
    
collIndInternet = [w.lower() for w in collIndInternet]
collIndInternetFormal = [w.lower() for w in collIndInternetFormal]
    
# create list of words from Korpus Indonesia
#https://korpusindonesia.kemdikbud.go.id

KOINInd = []

with open('/Volumes/Backup_Plus/TIW_experiments/KOIN/30000_KOIN.txt', 'r') as inFile:
    for line in inFile:
        KOINInd.append(line.split()[1])
inFile.close()
    
KOINInd = [w.lower() for w in KOINInd]

# create list of words from Google Javanese tsv
#https://github.com/google/language-resources/blob/master/jv/data/lexicon.tsv

googleJav = []

with open('/Volumes/Backup_Plus/TIW_Experiments/jav_lexicon.tsv', 'r') as tsvFile:            
        tsvReader = csv.reader(tsvFile, delimiter='\t')
        for row in tsvReader:
            googleJav.append(row[0])
        tsvFile.close()

googleJav = [w.lower() for w in googleJav]

# create list of words from Google Sundanese tsv
#https://github.com/google/language-resources/blob/master/su/data/lexicon.tsv

googleSund = []

with open('/Volumes/Backup_Plus/TIW_Experiments/sund_lexicon.tsv', 'r') as tsvFile:            
        tsvReader = csv.reader(tsvFile, delimiter='\t')
        for row in tsvReader:
            googleSund.append(row[0])
        tsvFile.close()

googleSund = [w.lower() for w in googleSund]



###### Read in teaching resource

teachR = []

with open('/Volumes/Backup_Plus/TIW_experiments/manCleanTIW.txt', 'r') as inFile:
    for line in inFile:
        teachR.append(line.split()[0])
inFile.close()





### All wordlists are converted to sets for faster processing to remove any duplicates after lowercase normalisation

teachRLex = set(teachR)

##English wordlists
# engLex is can be used early on to shorten the residual list - but contains 
# many Indoensian tokens which should not be removed
#engLex = set(engTokens)

engCMULex = set(engCMUTokens)
engAusLex = set(engAusTokens)
engManualLex = set(manEngRemove)

engManual2 = ['playscript', 'jungled', 'inviter', 'unspontaneous', 'locative', 'calendric', 'skillfulness', 'benefactive', 'birdnest', 'unirrigated', 'slangily', 'nosey', 'chinky', 'negator', 'pastness', 'stative', 'agglutinative', 'undergoer', 'matchlessly', 'mistakingly', 'unaspirated', 'illustratory', 'equational', 'subdistrict', 'darkish', 'comparer', 'memorization', 'continuer', 'singularize', 'addresser', 'answerer', 'weigher', 'substitutional', 'bisyllabic', 'streetside', 'methodologist']
engManual2Lex = set(engManual2)

engAllDict = list(engCMULex) + list(engAusLex) + list(engManualLex) + list(engManual2Lex)
engAllDictLex = set(engAllDict)

removeFromEngList = ['yang', 'aku', 'saya', 'lu', 'gue', 'jawab']
engAll = []
removedEng = []

for token in engAllDictLex:
    if token not in removeFromEngList:
        engAll.append(token)
    else:
        removedEng.append(token)
        

engAllLex = set(engAll)

## Indonesian wordlists
                                                                  
KOINIndLex = set(KOINInd)
wordnetIndLex = set(wordnetInd)
collIndInternetLex = set(collIndInternet)
collIndInternetFormalLex = set(collIndInternetFormal)

## Other langauges of Indonesian wordlists
googleJavLex = set(googleJav)
googleSundLex = set(googleSund)

## Remove English and Indonesian wordlists with more formal tendency

residMinusEng = teachRLex - engAllLex
residMinusKOIN = residMinusEng - KOINIndLex
residMinuswordnet = residMinusKOIN - wordnetIndLex
# Creates subset 'Residual Types'
residMinuscollIndInternetFormal = residMinuswordnet - collIndInternetFormalLex

len(list(residMinuscollIndInternetFormal))





c = {'a', 'b', 'z'}
d = {'a', 'b', '11', 'v'}

b = d - c
b = list(c) - list(d)
e = set(b)

len(list(e))

'''#Staged removal of wordlists

minusEng = teachRLex - engLex
minus2Eng = teachRLex - engCMULex
minus3Eng = minus2Eng - engAusLex
minus4Eng = minus3Eng - engManualLex
minusAllEng = teachRLex - engAllLex

minusInd = minus4Eng - KOINIndLex
minus2Ind = minusInd - collIndInternetFormalLex
minus3Ind = minus2Ind - wordnetIndLex'''

'''finds words in common between Indonesian lists and English lists 
to create a list of words which are more likely to be Indonesian.
These can then be added back in to the Indonesian list/removed from
the English list so that they don't get subtracted later on'''

shared = []

for word in wordnetIndLex:
    if word in engAllDictLex:
        if word in collIndInternetFormalLex: 
            shared.append(word)

'''#######
###############
#######################

'''Write leftovers to file
        
with open('engSet.txt', 'w') as outFile:
    outFile.write('\n'.join(engSet))
    outFile.close()


######################
#############
########



# Remove English from corpus.

engRemoved = []
eng = []

for word in teachR:
    if word not in engAllLex:
        engRemoved.append(word)
    else:
        eng.append(word)

engSet = set(eng)
        

# % of eng tokens

percenEngTokens = len(eng)/len(teachR)
        
# % of eng types 
## does not work - not sure how to write maths in python

percenEngTypes = ((len(list[(teachRLex)]-len(minus4Eng))//(len(teachR)))        
        
        
# Search TIW for Javanese lexical items

javInTIW = []

for word in engRemoved:
    if word in googleJavLex:
        javInTIW.append(word)
        
javInTIWLex = []

for word in minus4Eng:
    if word in googleJavLex:
        javInTIWLex.append(word)        

javInEng = []

for word in engAllLex:
    if word in googleJavLex:
        javInEng.append(word)        
        

'''print(javInTIW[200:300])

count = 0
for word in javInTIW:
    if word == 'kliwon':
        count = count + 1
        print('word found')'''
        
# Search TIW for Sundanese lexical items

sundInTIW = []

for word in engRemoved:
    if word in googleSundLex:
        sundInTIW.append(word)
        
sundInTIWLex = []

for word in minus4Eng:
    if word in googleSundLex:
        sundInTIWLex.append(word)

print(sundInTIW[200:300])


'''Checking''' 

x = ['sok', 'bola', 'iman', 'ning', 'dewan', 'di', 'sepeda', 'jawab', 'sama', 'kira', 'dia', 'yang', 'aku', 'saya', 'lu', 'gue']

count = 0
for word in minus4Eng:
    if word in x:
        count = count + 1
        print(word)
        
        
count = 0
for word in engRemoved:
    if word == 'gua':
        count = count + 1
        #print('enari found')
        
for word in minus4Eng:
    if word not in minusAllEng:
        print(word)        
        

c = list(engLex - engCMULex -engAusLex)
cz = sorted(c)
print(cz[0:100])

engManualLex = set(manEngRemove)

removeFromEngList = ['yang', 'aku', 'saya', 'lu', 'gue']
    

'''Plotting'''

import nltk
from nltk import FreqDist

fdist1 = FreqDist(engRemoved)
fdist1
fdist1['tidak']
fdist1['aku']
fdist1['aku']
fdist1['yang']
fdist1.plot(20, cumulative=True)

from nltk.corpus import webtext
from nltk.probability import FreqDist
from wordcloud import WordCloud
import matplotlib.pyplot as plt
 
words = ['data', 'science', 'dataset']
 
nltk.download('webtext')
wt_words = webtext.words('testing.txt')  # Sample data
 
points = [(x, y) for x in range(len(wt_words))
          for y in range(len(words)) if wt_words[x] == words[y]]
 
if points:
    x, y = zip(*points)
else:
    x = y = ()
 
plt.plot(x, y, "rx", scalex=.1)
plt.yticks(range(len(words)), words, color="b")
plt.ylim(-1, len(words))
plt.title("Lexical Dispersion Plot")
plt.xlabel("Word Offset")
plt.show()
