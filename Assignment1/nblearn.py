import string
import glob
import math
import sys

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

for eachfile in textFileList:
	data = open(eachfile, "r", encoding = "latin1")
	if "spam" in eachfile:
		spamdoc = spamdoc + 1
	if "ham" in eachfile: 
		hamdoc = hamdoc + 1
	for line in data:
		line = line.strip()
		line = line.lower()
		words = line.split(" ")
		for word in words:
			if "spam" in eachfile:
				if word in spam:
					spam[word] = spam[word] + 1
					n_spam = n_spam + 1
				else:
					spam[word] = 1
					n_spam = n_spam + 1
					if word not in ham:
						vocab = vocab + 1
						uniquelist.append(word)
			if "ham" in eachfile:
				if word in ham:
					ham[word] = ham[word] + 1
					n_ham = n_ham + 1
				else:
					ham[word] = 1
					n_ham = n_ham + 1
					if word not in spam:
						vocab = vocab + 1
						uniquelist.append(word)		
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