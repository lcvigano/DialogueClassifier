def extract_patterns(person1, person2):
    print '\nExtracting syntactic patterns...'
    f=open(person1 + '_sorted_result.out')
    e=open(person2 + '_sorted_result.out')
    person1_lines=f.read().split('\n')
    person2_lines=e.read().split('\n')
    pattern_compare={}
    for pattern_line in person1_lines:
        if len(pattern_line.split('|'))==2:
            pattern=pattern_line.split('|')[0].strip()
            value=pattern_line.split('|')[1].strip()
            pattern_compare[pattern]=[value]

    for pattern_line in person2_lines:
        if len(pattern_line.split('|'))==2:
            pattern=pattern_line.split('|')[0].strip()
            value=pattern_line.split('|')[1].strip()
        if pattern in pattern_compare:
            pattern_compare[pattern].append(value)
        else:
            pattern_compare[pattern]=[0,0,value]

    person1_only=[]
    person2_only=[]
    both=[]
    strange=[]
    for pattern in pattern_compare:
        value=pattern_compare[pattern]
        if len(value)==1: # person1 only
            person1_only.append((pattern,value[0]))
        elif len(value)==3: # person2 only
            person2_only.append((pattern,value[2]))
        elif len(value)==2: # both
            val1 = int(value[0])
            val2 = int(value[1])
            difference = (abs(val1-val2)/(abs(val1+val2)/2.0))
            both.append((pattern, difference, [val1, val2]))
        else:
            strange.append((pattern,value))
    filtered_both = filter(lambda x: abs(x[1]) >= 0.5, both)
    filtered_both = filter(lambda x: max(x[2]) >= 20, filtered_both)
    person1_filtered = filter(lambda x: x[2][0] > x[2][1], filtered_both)
    person1_map = map(lambda x: x[0], person1_filtered)

    person2_filtered = filter(lambda x: x[2][0] < x[2][1], filtered_both)
    person2_map = map(lambda x: x[0], person2_filtered)

    new=open(person1 + '_' + person2 + '_binaries.txt','w')
    new.write(person1 + '\n')
    for subtree in person1_map:
        new.write(subtree + '\n')
    new.write(person2 + '\n')
    for subtree in person2_map:
        new.write(subtree + '\n')

    new.close()