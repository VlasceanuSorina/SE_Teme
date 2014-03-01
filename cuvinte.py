import string
import re

f = open('fisier.txt', 'r')
filecontents= f.read()
regex = re.compile('[%s]' % re.escape(string.punctuation))
filecontents = regex.sub('', filecontents)

wordcount = {}

for word in (filecontents).split():
    length=len(word)
    if not length in wordcount:
        wordcount[length]= []
    wordcount[length].append(word)

for nr_letters, words in wordcount.items() :
    print(nr_letters, words)
