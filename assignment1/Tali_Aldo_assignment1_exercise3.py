'''
    ########################################################################################
    # Author: Aldo Tali
    # MatrikelNummer: 2572725
    # Date: 04/05/2018
    # Computer Enginnering Student
    # Purpose: The following script covers the solution of the third exercise of ASA course
    #          offered in Saarland University Summer Semester 2018.
    ########################################################################################
'''


import sys

'''
    ############################################################################################################
    # Updated Shif-And algorithm to accept a dictionary of patterns instead of just one pattern.
    # The following assumes that the len(P) << len(T) where P stands for the pattern itself and T for the text.
    # This means that the extra information being kept for the active states of each pattern iencreases
    # linearly in the order of len(P)for which it is assumed to be negligible since len(P) << len(T).
    # The algorithm here tries to make use of this in order to read the text only once. Therefore while parsing
    # the text the algorithm will try to check for each of the patterns at each character read.
    # Previously these checks were being done only for one pattern (since the lookup was intended only for 1)
    ###########################################################################################################
'''
#NOTE: This implementation considers the input of patterns to be a dictionary
def multiplePatternShiftAnd(patterns,T):

    #keep a set of masks, set of active states and a set accept states for each pattern
    multipleMasks = dict()
    accept_states = dict()
    active_states = dict()

    #initialize all three sets above accordingly for each pattern
    #the rest of the logic is same as in the normal shift-and agorithm
    for pattern in patterns:
        multipleMasks[pattern] = dict()
        bit = 1
        for c in pattern:
            if c not in multipleMasks[pattern]: multipleMasks[pattern][c] = 0
            multipleMasks[pattern][c] |= bit
            bit *= 2
        accept_states[pattern] = bit // 2
        active_states[pattern] = 0

    i = 0
    
    #look for the possible state transitions for each other character that is read from the text
    for c in T:
        for pattern in patterns:
            mask = multipleMasks[pattern].get(c)
            
            #since we deal with multiple masks that means we deal with different alphabets for each pattern (possibly!)
            #this only makes up for the letters that are in the text but not in this specific pattern.
            if mask == None: mask = 0
            
            #updates bit-mask of this pattern's active states
            active_states[pattern] = ((active_states[pattern] << 1) + 1) & mask
            if (active_states[pattern] & accept_states[pattern]) != 0:
                #store the index of this accept state and reset the DFA for the pattern
                patterns[pattern].append(i)
                active_states[pattern] = 0
        i+=1
    return patterns
###---------------------------------------------------------------------------------------------###


#get the command line arguments
patterns_txt = sys.argv[1]
text_txt = sys.argv[2]

#read out all possible patterns
pattern_file = open(patterns_txt,'r')
arrayOfPatterns = pattern_file.readlines()
pattern_file.close()

#keep this map for the final output
patterns = dict()

#for each pattern initialize a list of empty locations
for index in range (0,len(arrayOfPatterns)):
    patterns[arrayOfPatterns[index].strip('\n')] = list()

#read the text
text_file = open(text_txt,'r')

for line in text_file:
    patterns = multiplePatternShiftAnd(patterns,line)

text_file.close()

#solely for printing 3
for pattern in patterns :
    s = ""
    s += pattern + " "
    comma = False
    for index in patterns[pattern]:
        if comma:
            s+= "," + `index`
        else:
            s+= `index`
            comma = True

    print(s)

#solely for ooutputing results
output = open('patternOccurrancesResults.txt',"w+")

for pattern in arrayOfPatterns:
    output.write(pattern)
    first = True
    for indeces in patterns[pattern.strip("\n")]:
        if first == False :
            output.write(",")
        output.write(format(indeces))
        first = False
    output.write("\n")

