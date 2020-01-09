import csv

with open('simpsons_script_lines.csv', newline='') as csvfile:
	spamreader = csv.reader(csvfile)
	dia_data=[]
	for row in spamreader:
		#print(row)
		comma_count=0
		sentence=''
		name=''
		quote_begin=False
		#print(row[8])
		#print(row[10])
		#print(len(dia_data),row)
		sentence=row[10]

		#sentence=row[3]
		sentence
		sentence=sentence.replace('Dr.','Dr')
		sentence=sentence.replace('Mr.','Mr')
		sentence=sentence.replace('Mrs.','Mrs')
		sentence=sentence.replace('\n','')

		sentence=sentence.replace('?',' ? ')
		sentence=sentence.replace("..."," ^ ")
		sentence=sentence.replace("…"," ^ ")
		sentence=sentence.replace('.',' . ')
		sentence=sentence.replace('!',' ! ')
		sentence=sentence.replace(',',' , ')
		sentence=sentence.replace(';',' ; ')


		sentence=sentence.replace('-','')
		sentence=sentence.replace('—','')
		sentence=sentence.replace('_','')
		sentence=sentence.replace('"','')
		sentence=sentence.replace("(",'')
		sentence=sentence.replace(')','')
		sentence=sentence.replace(':','')



		sentence=sentence.split()
		sub_sentence=[]
		for i in range(len(sentence)):
			word=sentence[i].lower()
			sub_sentence.append(word)
			if word in "?.!^;":
				if len(sub_sentence)==1:
					sub_sentence=[]
				else:
					#print((row[2],sub_sentence))
					dia_data.append((row[8].lower(),sub_sentence))
					sub_sentence=[]

		#dia_data.append((row[2],sentence))
#print(len(dia_data))
#print(dia_data)
word_list=[]
name_count={}
for name,dialogue in dia_data:
	#word_list.append(name) # some names have spaces. not sure how to handle that
	if name in name_count:
		name_count[name]+=1
	else:
		name_count[name]=1
	'''
	for word in dialogue:
		if word not in ".,?!^":
			word_list.append(word)
	'''
most_common_chars=sorted(name_count, key=name_count.get)[-5:]

most_common=[]
max_len=0
for name,dialogue in dia_data:
	if (name in most_common_chars and len(dialogue)<=17):
		most_common.append((name,dialogue))
#print(most_common)

dialogue_count={}
for name,dialogue in most_common:
	if name not in dialogue_count:
		dialogue_count[name]=[dialogue]
	else:
		dialogue_count[name].append(dialogue)
	#dialogue_count.append((len(dialogue),dialogue))
#print(dialogue_count)

# sen_len={}
# for name in dialogue_count:
# 	print(name)
# 	for sentence in dialogue_count[name]:
# 		if len(sentence) not in sen_len:
# 			sen_len[len(sentence)]=1
# 		else:
# 			sen_len[len(sentence)]+=1
# print(sen_len)
# #print([(v, k) for k, v in sen_len.items()])

# print(sorted([(k, v) for k, v in sen_len.items()], key=lambda x: x[0]))

#print(dialogue_count['homer simpson'])
#print(sorted(dialogue_count,key=lambda x: x[0]))

f = open('training_data_hl.txt','w')
p = open('testing_data_hl.txt','w')


for name in dialogue_count:
	print(name)
	if name != "homer simpson" and name != "lisa simpson":
		print(name,'skipped')
		continue
	count=0
	training_split=len(dialogue_count[name])*.7
	for sentence in dialogue_count[name]:
		count+=1
		if count<training_split:
			f.write(name+'|'+' '.join(sentence).replace("^","...")+'\n')
		else:
			p.write(name+'|'+' '.join(sentence).replace("^","...")+'\n')

f.close()
p.close()
'''
print(len(most_common))
f = open('top-dialogue.txt','w')
for date_pair in most_common:
	f.write(str(date_pair)+'\n')
f.close()
'''

#print(name_count)
#print(sorted(name_count, key=name_count.get)[-5:])
#print(len(word_set))
'''
f = open('word_set.txt','w')
for word in word_list:
	f.write(word+' ')
f.close()

f = open('char-dialogue.txt','w')
for date_pair in dia_data:
	f.write(str(date_pair)+' ')
f.close()

print(len(set(word_list)))
'''


'''
with open('All-seasons.csv', newline='') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
	p=set()
	l=[]
	for row in spamreader:

		if len(row)<3:
			continue
		row=' '.join(row)
		period=0
		period_count=True
		name=''
		sentence=''
		comma_count=0
		for i in range(len(row)):
			letter=row[i]
			if letter==',':
				comma_count+=1
				continue
			if comma_count<2:
				continue
			if comma_count==2:
				name+=letter
			if comma_count>2:
				sentence+=letter
			if letter in '.?!':
				try:
					row[i+1]
					period_count=False
					#make a new sentence
					#p.add((name,sentence.replace('"','').lstrip()))
					l.append((name,sentence.lstrip()))

					#p.add((name,sentence))
					sentence=''
				except:
					#end of the line of dialoge
					period_count=True
		if period_count:
			#p.add((name,sentence))
			#p.add((name,sentence.replace('"','').lstrip()))
			l.append((name,sentence.replace('(','').lstrip()))
filtered_l=[]
for name,sentence in l:
	#print(name,':',sentence.replace('"','').lstrip())
	if len(sentence)<2 or sentence==[]:
		continue
	if sentence[0]=='"':
		sentence=sentence[1:]
	sentence=sentence.replace("."," ")
	sentence=sentence.replace("!"," ")
	sentence=sentence.replace("?"," ")
	sentence=sentence.replace(","," ")
	sentence=sentence.split()
	filtered_l.append((name,sentence))
	#print(name,':',sentence.split())
	#p.add((name,sentence.split()))
print(len(l))
print(len(filtered_l),filtered_l[0])
#print(len(p))
word_set=set()
for name,sentence in filtered_l:
	#print(sentence)
	for word in sentence:
		word_set.add(word.lower())
		#print(word)
print(len(word_set))
#print(word_set)
'''

