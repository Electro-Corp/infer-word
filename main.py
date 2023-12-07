"""
    Analyzes text files and makes a database from which
    it can guess which word comes next in a word sequence
"""
from codecs import ascii_encode
import os
import random
import re
import string
import pickle
import time
letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
class Asc:
    def __init__(self, word, nums):
        self.word = word
        self.nums = nums
class Word:
    def __init__(self, word):
        self.word = word
        self.ascs = []
    def getMostAsc(self):
        best = -1
        cur = Asc("the", 0)
        max = 3
        if(len(self.ascs) < max):
            max = len(self.ascs)
        for asc in self.ascs:
            #print(asc.word + " : " + str(asc.nums))
            #if(asc.nums > best and random.randint(0, asc.nums * 2 + best + max) > asc.nums):
            if(asc.nums > best and asc.word not in self.word):
                best = asc.nums
                cur = asc
        return cur.word
class Letter:
    def __init__(self, letter):
        self.letter = letter
        self.words = []
    def work(self, goof, ascreal):
        #print(self.letter + " here... just got handed " + goof)
        # find word
        goof = goof.lower()
        #try:
        exist = False
        for tmp in self.words:
            if(tmp.word == goof):
                exist = True
                found = False
                for asc in tmp.ascs:
                    if(asc.word == ascreal):
                        asc.nums += 1
                        found = True
                    
                if not found:
                    #print("add asc " + ascreal + " | for | " + goof)
                    wow = Asc(ascreal, 1)
                    tmp.ascs.append(wow)
                    #print("On word " + tmp.word + " we got that " + str(len(tmp.ascs)))
        if exist == False:
            wow = Asc(ascreal, 1)
            bad = Word(goof)
            bad.ascs.append(wow)
            self.words.append(bad)

            #self.work(self, word, ascreal)
            #print("add word " + goof)
        #except:
    def get(self, word):
        yeah = False
        word = word.lower()
        for swag in self.words:
            if(swag.word == word):
                # it exists
                yeah = True
                #print(swag.word + ", " + word + " , " + swag.getMostAsc())
                return swag.getMostAsc()
        if(len(self.words) > 0):
            print("get most..")
            #return self.words[0].getMostAsc()
            return "NAH_NAH"
        else:
            print("=== no words ===")
            print(self.letter)
            print(len(self.words))
            print("================")
            return "NAH_NAH"
class Mak:
    def __init__(self):
        self.lets = []
        for i in range(26):
            wcool = Letter(letters[i])
            self.lets.append(wcool)
            print("Init " + letters[i]) # type: ignore
        print("Init " + str(len(self.lets)) + " letters")
    def addWord(self, word, ascreal):
        # Check if word exsits 
        #if(self.lets[string.lowercase.index(word[0])].words.__contains__(word.word) == 1):
            # Lets help its asc
        #    self.lets[string.lowercase.index(word[0])].words.index(word).ascs.nums += 1
        #print(word[0])
        word = word.lower()
        ascreal = ascreal.lower()
        word = re.sub(r'[^A-Za-z]', '', word)
        ascreal = re.sub(r'[^A-Za-z]', '', ascreal)
        #print(word)
        #print(word + " belongs at " + str(string.ascii_lowercase.index(word[0])))
        #print(word[0] + " is at " + self.lets[string.ascii_lowercase.index(word[0])].letter)
        #print(word + " belongs at " + self.lets[string.ascii_lowercase.index(word[0])].letter)
        self.lets[string.ascii_lowercase.index(word[0])].work(word, ascreal)
    def getAsc(self, word):
        word = word.lower()
        return self.lets[string.ascii_lowercase.index(word[0])].get(word)
    def getRandomWord(self):
        g = random.randint(0, 25)
        #while(len(self.lets[g].words) < 1):
        #    g = random.randint(0, 25)
        return self.lets[g].words[random.randint(0, len(self.lets[g].words))].word
    def finalDump(self):
        k = 0
        j = 0
        os.system("rm out.log")
        with open("out.log", "w") as b:
            for letter in self.lets:
                b.write("=== LETTER: " + letter.letter + " ===\n")
                for word in letter.words:
                    k += 1
                    b.write("=== WORD: " + word.word + " ===\n")
                    b.write("ASCS: " + str(len(word.ascs)) + "\n")
                    for asc in word.ascs:
                        j += 1
                        b.write("[ASC] " + asc.word + " - " + str(asc.nums) + "\n")
                    b.write("=== END WORD ===\n")
                b.write("=== END LETTER ===\n")
        print("Total words: " + str(k))
        print("Total ascs: " + str(j))
        print("Total: " + str(k + j))
print("Started")
crazy = Mak()
print("Reading")
g = 0
goof = "nah"
y = input("? ")
if("y" in y):
    goof = "yah"
if("r" in y):
    goof = "wow"
if not "yah" in goof:
    fulltime = 0
    path = input("Train Directory ? ")
    if("wow" in goof):
        crazy = pickle.load(open("dump.dump", "rb"))
    for filename in os.listdir(path):
        print("Reading: " + filename)
        tmptime = time.time()
        with open(path + "/" + filename, "r") as goof:
            l = goof.readlines()
            #print(l)
            for line in l:
                #print(line)
                c = 0
                swag = line.split(" ")
                for word in swag:
                    word = word.lower()
                    word = re.sub(r'[^A-Za-z]', '', word)
                    if(c + 1 < len(swag) and len(word) > 0):
                        if("the" not in swag[c+1] and not word == swag[c+1].lower()):
                            damn = swag[c+1].lower()
                            damn = damn.replace(" ", '')

                            crazy.addWord(word, damn)
                            g +=1
                        c+= 1
                # print("Completed:" + str((g / (len(l) * len(swag))) * 100), end='\r')
        print("Read in " + str(time.time() - tmptime))
        fulltime += time.time() - tmptime
    
    print("Finished 'train' in " + str(fulltime))
    pickle.dump(crazy, open("dump.dump", "wb"))
    print("Dump finished")
print("Load from dump")
crazy = pickle.load(open("dump.dump", "rb"))
crazy.finalDump()
#print(crazy.g)
while True:
    start = input("INPUT> ")
    word = start.split(" ")[len(start.split(" ")) - 1]
    print("Start: " + word)
    wow = []
    tmpback = []
    wow.append(start + " ")
    for i in range(300):
       # try:
        tmpword = crazy.getAsc(word)
        while len(tmpword) < 1 or tmpword in tmpback:
            tmpword = crazy.getAsc(word)
        if(tmpword == "NAH_NAH"):
            print(" [TMP->] ", end="")
            word = crazy.getRandomWord()
        else:
            word = tmpword
        print(word + " ", end="")
        wow.append(word + " ")
        tmpback.append(word)
        if(i  % 20 == 0):
            tmpback = []
            wow.append("\n")
        #except:
         #   print(" [ERROR->] ", end="")
         #   word = crazy.getRandomWord()
    print("")
    with open("out.txt", "w") as w:
        w.writelines(wow)
