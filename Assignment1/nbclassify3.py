import string
import glob
import math
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import sys

mydir = sys.argv[1]

spam = dict()
ham = dict()

nbmodel = open("nbmodel.txt", "r", encoding = "latin1")
for line in nbmodel:
	words = line.split(", ")
	temp = []
	for word in words:
		temp.append(word)
	spam[temp[0]] = float(temp[1])
	ham[temp[0]] = float(temp[2])

pspam = spam['spamhamprobability']
pham = ham['spamhamprobability']

textFileList = glob.glob(mydir + '/**/*.txt', recursive = True)

stop_words = set(stopwords.words('english'))
ps = PorterStemmer()

for eachfile in textFileList:
	data = open(eachfile, "r", encoding = "latin1")
	pspamdoc = pspam
	phamdoc = pham
	for line in data:
		line = line.strip()
		line = line.lower()
		line = line.translate(line.maketrans("","", string.punctuation))
		words = line.split(" ")
		for word in words:
			stemword = ps.stem(word)
			if word not in stop_words:
				if stemword in spam.keys():
					pspamdoc = pspamdoc + spam[stemword]
				if stemword in ham.keys():
					phamdoc = phamdoc + ham[stemword]

	if pspamdoc>phamdoc:
		ans = "spam"
	else:
		ans = "ham"
	with open("nboutput.txt", "a", encoding = "latin1") as outf:
		outf.write("%s\t%s\n" % (ans, eachfile))