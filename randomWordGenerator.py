#This a random word generator made with a balance of consonants and vowels to make it seem like an actual word
import random
vowels = ["a","e","i","o","u"]
consonants = ["b", "c", "d", "f", "g", "h", "j", "k", "l", "m", "n", "p", "q", "r", "s", "t", "v", "w", "x", "y", "z"]

commonCons = ["b", "c", "d", "f", "g", "h", "j", "k", "l", "m", "n", "p", "q", "r", "s", "t", "v", "w"]
rareCons = ["x","y","z"]
#WHEN QUE HAPPENS, MAKE NEXT LETTER CONS
#MAYBE A RARE LIST? (X,Y,Z)DONE
#MAYBE A NO ENDING WORD?(words cant end in j,q,v)DONE
run = True
allCons = False
def construct():
    startLetter = random.randint(1,2)
    wordLen = random.randint(3,5)
    word = ""
    vowConBalance = 0
    yFound = False
    consonantOveride = False
    if startLetter == 1:
        word = random.choice(vowels)
        #print(word)
        vowConBalance = 2
    else:
        word = random.choice(consonants)
        #print(word)
        vowConBalance = 1
    i = 0
    doubleVowelRarity = 5
    while i<wordLen:
        if consonantOveride:
            vowConBalance = 2
            consonantOveride = False
        if vowConBalance == 1:
            word += random.choice(vowels)
            secondVowel = random.randint(1,doubleVowelRarity)
            if secondVowel == 1:
                vowConBalance = 1
                doubleVowelRarity = 1000
            else:
                vowConBalance += 1
            #print(vowConBalance)
            #print(word)
        elif vowConBalance == 2:
            if allCons == True:
                currentCons = random.choice(consonants)
            elif allCons == False:
                xyzPick = random.randint(1,25)
                if xyzPick == 1:
                    currentCons = random.choice(rareCons)
                else:
                    currentCons = random.choice(commonCons)
            #did this for "y" check system
            word += currentCons
            vowConBalance -= 1
            #print(vowConBalance)
            #print(word)
        if "q" in word and not "qu" in word:
            badLetter = word.index("q")+1
            word = word[:badLetter] + "u" + word[badLetter+1:]
        if "aa" in word:
            badLetter = word.index("a")
            word = word[:badLetter] + random.choice(vowels) + word[badLetter+1:]
            #print("changed!")
        if "ii" in word:
            badLetter = word.index("i")
            word = word[:badLetter] + random.choice(vowels) + word[badLetter+1:]
            #print("changed!")
        if "uu" in word and not "quu" in word:
           badLetter = word.index("u")
           word = word[:badLetter] + random.choice(vowels) + word[badLetter+1:]
           #print("changed!")
        elif "quu" in word:
            badLetter = word.index("q")+2
            word = word[:badLetter] + "e" + word[badLetter+1:]
            consonantOveride = True
        
        i+=1
    endingCheck = True
    while endingCheck: 
        if word[wordLen] == "j" or word[wordLen] == "v" or word[wordLen] == "q":
            word = word[:wordLen] + random.choice(consonants)
            continue
        if word[wordLen] == "qu":
            word = word[:wordLen+2] + "e"
            continue
        break
    return word
'''
while run:
	start = input("Start random word generator?")		
	if "no" in start:
		run = False
	elif "set" in start:
	    print("1.Make x,y and z more common\nAdditional rules coming in future")
	    setting = input("Choose setting(Can choose multiple)")
	    if "1" in setting:
	        allCons = True
	else:
		print(construct())
		print("----------")
'''
