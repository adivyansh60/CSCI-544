import string
import glob
import math
import sys
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

mydir = sys.argv[1]

textFileList = glob.glob(mydir + '/**/*.txt', recursive = True)

ham = dict()
spam = dict()
n_spam = 0
n_ham = 0
vocab = 0
spamdoc = 0
hamdoc = 0
uniquelist = []
stop_words = set(stopwords.words('english'))
ps = PorterStemmer()

for eachfile in textFileList:
	data = open(eachfile, "r", encoding = "latin1")
	if "spam" in eachfile:
		spamdoc = spamdoc + 1
	if "ham" in eachfile: 
		hamdoc = hamdoc + 1
	for line in data:
		line = line.strip()
		line = line.lower()
		line = line.translate(line.maketrans("","", string.punctuation))
		words = line.split(" ")
		for word in words:
			stemword = ps.stem(word)
			if word not in stop_words:
				if "spam" in eachfile:
					if stemword in spam:
						spam[stemword] = spam[stemword] + 1
						n_spam = n_spam + 1
					else:
						spam[stemword] = 1
						n_spam = n_spam + 1
						if stemword not in ham:
							vocab = vocab + 1
							uniquelist.append(stemword)
				if "ham" in eachfile:
					if stemword in ham:
						ham[stemword] = ham[stemword] + 1
						n_ham = n_ham + 1
					else:
						ham[stemword] = 1
						n_ham = n_ham + 1
						if stemword not in spam:
							vocab = vocab + 1
							uniquelist.append(stemword)		
	data.close()

pspam = math.log(spamdoc/(spamdoc + hamdoc))
pham = math.log(hamdoc/(spamdoc + hamdoc))

with open("nbmodel.txt", "a", encoding = "latin1") as outf:
	outf.write("%s, %f, %f\n" % ('spamhamprobability',pspam,pham))
	for word in uniquelist:
		if word in ham.keys():
			hamp = math.log((ham[word] + 1)/(n_ham + vocab))
		else:
			hamp = math.log(1/(n_ham + vocab))
		if word in spam.keys():
			spamp = math.log((spam[word] + 1)/(n_spam + vocab))
		else:
			spamp = math.log(1/(n_spam + vocab))
		outf.write("%s, %f, %f\n" % (word,spamp,hamp))