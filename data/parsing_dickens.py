import re
import random

f = open('1400-0.txt') #great expectations
f2 = open('98-0.txt') #a tale of 2 cities
f3 = open('1342-0.txt') #pride and prejudice
f4 = open('158-0.txt') #emma
out_f = open('parsed_dickens_austen.txt', 'w')
out_f_training = open('training_austen_dickens.txt', 'w')
out_f_testing = open('testing_austen_dickens.txt', 'w')


text = f.read()
text = text.replace('Dr.','Dr')
text = text.replace('Mr.','Mr')
text = text.replace('Mrs.','Mrs')
text = text.replace('\n', ' ')
text = text.replace('...', '^')
text=text.replace('.','.\n')
text=text.replace('!','!\n')
text=text.replace('?','?\n')
text=text.replace('\r','')
text=text.replace('-','')
text=text.replace('_','')
text=text.replace('"','')
text=text.replace('[','')
text=text.replace(']','')
text = text.replace('^', '...')
text=text.replace("'",'')
text=text.replace("(",'')
text=text.replace(')','')
text=text.replace(':','')
text=text.replace('*','')
text=text.split('\n')
final_d=[]
for each in text:
	count=0
	for begin in each:
		if begin==' ':
			count+=1
		else:
			break
	final_d.append(each[count:])


text2 = f2.read()
text2 = text2.replace('Dr.','Dr')
text2 = text2.replace('Mr.','Mr')
text2 = text2.replace('Mrs.','Mrs')
text2 = text2.replace('\n', ' ')
text2 = text2.replace('...', '^')
text2=text2.replace('.','.\n')
text2=text2.replace('!','!\n')
text2=text2.replace('?','?\n')
text2=text2.replace('\r','')
text2=text2.replace('-','')
text2=text2.replace('_','')
text2=text2.replace('"','')
text2=text2.replace('[','')
text2=text2.replace(']','')
text2 = text2.replace('^', '...')
text2=text2.replace("'",'')
text2=text2.replace("(",'')
text2=text2.replace(')','')
text2=text2.replace(':','')
text2=text2.replace('*','')
text2=text2.split('\n')

for each in text2:
	count=0
	for begin in each:
		if begin==' ':
			count+=1
		else:
			break
	final_d.append(each[count:])


random.shuffle(final_d)


text3 = f3.read()
text3 = text3.replace('Dr.','Dr')
text3 = text3.replace('Mr.','Mr')
text3 = text3.replace('Mrs.','Mrs')
text3 = text3.replace('\n', ' ')
text3 = text3.replace('...', '^')
text3=text3.replace('.','.\n')
text3=text3.replace('!','!\n')
text3=text3.replace('?','?\n')
text3=text3.replace('\r','')
text3=text3.replace('-','')
text3=text3.replace('_','')
text3=text3.replace('"','')
text3=text3.replace('[','')
text3=text3.replace(']','')
text3 = text3.replace('^', '...')
text3=text3.replace("'",'')
text3=text3.replace("(",'')
text3=text3.replace(')','')
text3=text3.replace(':','')
text3=text3.replace('*','')
text3=text3.split('\n')
final_a=[]
for each in text3:
	count=0
	for begin in each:
		if begin==' ':
			count+=1
		else:
			break
	final_a.append(each[count:])

text4 = f4.read()
text4 = text4.replace('Dr.','Dr')
text4 = text4.replace('Mr.','Mr')
text4 = text4.replace('Mrs.','Mrs')
text4 = text4.replace('\n', ' ')
text4 = text4.replace('...', '^')
text4=text4.replace('.','.\n')
text4=text4.replace('!','!\n')
text4=text4.replace('?','?\n')
text4=text4.replace('\r','')
text4=text4.replace('-','')
text4=text4.replace('_','')
text4=text4.replace('"','')
text4=text4.replace('[','')
text4=text4.replace(']','')
text4 = text4.replace('^', '...')
text4=text4.replace("'",'')
text4=text4.replace("(",'')
text4=text4.replace(')','')
text4=text4.replace(':','')
text4=text4.replace('*','')
text4=text4.split('\n')

for each in text4:
	count=0
	for begin in each:
		if begin==' ':
			count+=1
		else:
			break
	final_a.append(each[count:])

random.shuffle(final_a)

final_final = []
for sentence in final_d:
	final_final.append('dickens|'+sentence)
for sentence in final_a:
	final_final.append('austen|'+sentence)

random.shuffle(final_final)


#randomize final (shuffle) before doing this 
print len(final_d), "is number of dickens sentences"
print len(final_a), "is number of austen sentences"
print len(final_final)
# 32,329 sentences total
# 22,630 for training (about 70%)
# 9,699 for testing (about 30%)

training = final_final[:22630]
testing = final_final[22630:]

for auth_sent in testing:
	if 'Chapter' not in auth_sent:
		out_f_testing.write(auth_sent)
		out_f_testing.write('\n')

for auth_sent in training:
	if 'Chapter' not in auth_sent:
		out_f_training.write(auth_sent)
		out_f_training.write('\n')



#for auth_sent in final_final:
	#if 'Chapter' not in auth_sent:
		#out_f.write(auth_sent)
		#out_f.write('\n')








