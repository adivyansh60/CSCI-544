import string
import sys

outputfile = sys.argv[1]

guessspam = 0
originalspam = 0
correctspam = 0
guessham = 0
originalham = 0
correctham = 0
correcttotal = 0
total = 0

nboutput = open(outputfile, "r", encoding = "latin1")
for line in nboutput:
	total = total +1
	words = line.split("\t")
	temp = []
	for word in words:
		temp.append(word)
	if temp[0] == "ham":
		guessham = guessham + 1
		if "ham" in temp[1]:
			originalham = originalham +1
			correctham = correctham + 1
			correcttotal = correcttotal + 1
		if "spam" in temp[1]:
			originalspam = originalspam + 1
	if temp[0] == "spam":
		guessspam = guessspam + 1
		if "spam" in temp[1]:
			originalspam = originalspam +1
			correctspam = correctspam + 1
			correcttotal = correcttotal + 1
		if "ham" in temp[1]:
			originalham = originalham + 1

print((correcttotal/total)*100)

precspam = correctspam/guessspam
print(precspam)
recallspam = correctspam/originalspam
print(recallspam)
f1spam = (2*precspam*recallspam)/(precspam+recallspam)
print(f1spam)

precham = correctham/guessham
print(precham)
recallham = correctham/originalham
print(recallham)
f1ham = (2*precham*recallham)/(precham+recallham)
print(f1ham)