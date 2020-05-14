#Robert Genega
#CS471 project 4
#TF-IDF

import sys
import io
from textblob import TextBlob
import re

import math


def tf(word, blob):
    return blob.words.count(word) / len(blob.words)

def n_containing(word, bloblist):
    return sum(1 for blob in bloblist if word in blob.words)

def idf(word, bloblist):
    return math.log(len(bloblist) / (1 + n_containing(word, bloblist)))

def tfidf(word, blob, bloblist):
    return tf(word, blob) * idf(word, bloblist)


csv1 = sys.argv[1]
csv2 = sys.argv[2]
csv3 = sys.argv[3]

blobList = []


file = io.open(csv1, mode="r", encoding="utf-8")

maxLine = 200

for line in file:

    if maxLine == 0:
        break

    finalLine = ""
    i = 0

    quoteSeparated = line.split("\"")



    for element in quoteSeparated:

        if i%2 == 1:
            finalLine += element.replace(",", "")
        else:
            finalLine += element

        i+=1
        

    brokenLine = finalLine.split(",")
    articleText = brokenLine[-1]

    articleText = articleText.lower()
    articleText = re.sub(r'\W+ ', ' ', articleText)
    articleText = articleText.replace("'", "")
    articleText = articleText.replace("’", "")
    articleText = articleText.replace("\"", "")
    articleText = articleText.replace("“", "")
    articleText = articleText.replace(".", "")
    articleText = articleText.replace(" s ", " ")
    

    #print(brokenLine[2])
    print(articleText)
    blob = TextBlob(articleText)
    blobList.append(blob)

    #print( tf("content", blob) )
    maxLine -= 1




file.close()
blobList.pop(0)

for i, blob in enumerate(blobList):

    print("Top words in document {}".format(i + 1))
    scores = {word: tfidf(word, blob, blobList) for word in blob.words}
    sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    for word, score in sorted_words[:10]:
        print("\tWord: {}, TF-IDF: {}".format(word, round(score, 5)))
