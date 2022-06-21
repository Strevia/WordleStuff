from collections import defaultdict
import heapq
import math
import time
import pymp
from numpy import argmax, argmin, array, square
import pickle, sys
class Tree:
    def __init__(self, data):
        self.children = {}
        self.data = data
    def __str__(self):
        return self.data

def zero():
    return 0
def getBestHard(wordListGuess, wordListPoss, calcFunc, recursionLength=0):
    out = defaultdict(int)
    for c, guess in enumerate(wordListGuess):
        contain = defaultdict(list)
        for poss in wordListPoss:
            if not isinstance(poss, dict):
                contain[calcFunc(guess, poss)].append(poss)
            else:
                cats = set()
                for word in poss:
                    cats.add(calcFunc(guess, poss[word]))
                for cat in cats:
                    contain[cat].append(poss)          
        equalOne = []
        for cont in contain:
            if len(contain[cont]) == 1:
                equalOne.append(contain[cont][0])
        out[guess] = equalOne
        print(f"{(c)}/{len(wordListGuess)}", end='\r')
    wordFreqSort = dict(sorted(out.items(), key=lambda item: len(item[1])))
    return wordFreqSort
    
def getBestThree(wordListGuess, wordListPoss, calcFunc):
  out = defaultdict(int)
  if not isinstance(wordListPoss[0], list):
      wordListPoss = [wordListPoss]
  for c, guess in enumerate(wordListGuess):
    for wordlist in wordListPoss:
        contain = defaultdict(zero)
        for poss in wordlist:
            if guess != poss:
                contain[calcFunc(guess, poss)] += 1
        out[guess] += sum(square(array(list(contain.values())))/len(wordlist))/len(wordListPoss)
    print(f"{(c)}/{len(wordListGuess)}", end='\r')
  wordFreqSort = dict(sorted(out.items(), key=lambda item: item[1]))
  return wordFreqSort
def getBestTwo(wordListPoss, wordListGuess):
    wordFreq = defaultdict(zero)
    for i in wordListGuess:
      wordFreq[i] = bestTwoScore(i, wordListPoss)
    wordFreqSort = dict(sorted(wordFreq.items(), key=lambda item: item[1]))
    return wordFreqSort
def bestTwoScore(guesses, wordListPoss, freq):
    summ1, summ2 = 0, 0
    letters = "abcdefghijklmnopqrstuvwxyz"
    guessFreq = defaultdict(int)
    for i in letters:
        guessFreq[i] = [0] * 5
    for i in guesses:
        for c, j in enumerate(i):
            guessFreq[j][c] += 1.0
    letters = "abcdefghijklmnopqrstuvwxyz"
    for guess in guesses:
        for c, j in enumerate(guess):
            summ1 -= freq[j][c] / float(guessFreq[j][c])
        for c, j in enumerate(guess):
            summ2 -= sum(freq[j]) / float(sum(guessFreq[j]))
    return summ1 + summ2 / (1.0 + len(i) - len(set(i)))
betterCalc = {}
def betterWord(chosenWords, wordListPoss, calcFunc, returnList = False):
    global betterCalc
    output = []
    for guess in chosenWords:
        if guess in betterCalc:
            output.append(betterCalc[guess])
            continue
        out = dict()
        for word in wordListPoss:
            calc = calcFunc(guess, word)
            out[word] = calc
        output.append(out)
        betterCalc[guess] = out
    if returnList:
        inverted = defaultdict(list)
    else:
        inverted = defaultdict(int)
    for word in wordListPoss:
        x = ""
        for c in range(len(chosenWords)):
            x += output[c][word]
        if returnList:
            inverted[x].append(word)
        else:
            inverted[x] += 1
    return inverted
calcs = {}
def calcWord(guess, word):
    global calcs
    if (guess, word) in calcs:
        return calcs[(guess, word)]
    counts = defaultdict(int)
    out = [0] * len(guess)
    for i, char in enumerate(word):
        counts[char] += 1
        if i < len(guess) and char == guess[i]:
            out[i] = "g"
            counts[char] -= 1
    for i in range(len(guess)):
        if out[i] == "g":
            continue
        elif counts[guess[i]] > 0:
            out[i] = "y"
            counts[guess[i]] -= 1
        else:
            out[i] = "r"
    calcs[(guess, word)] = ''.join(out)
    return ''.join(out)
def remove(wordList, output, guess, calcFunc):
    newList = list()
    for word in wordList:
        if calcFunc(guess, word) == output:
            newList.append(word)
    return newList
def flatten(t):
    return [item for sublist in t for item in sublist]
calcs = dict()
def noSame(word1, word2):
    return len(set(word1)) + len(set(word2)) == len(set(word1 + word2))
calced = dict()
def nextWord(guesses, wordList, calcFunc):
    #global calced
    #bestWords = pymp.shared.list([None] * 5)
    bestWords = [0]
    #with pymp.Parallel(5) as p:
    if True:
        letters = "abcdefghijklmnopqrstuvwxyz"
        localWords = [len(wordList)] * len(wordList)
        freq = dict()
        for i in letters:
            freq[i] = [0] * 5
        gsindex = list()
        gss = list()
        gs = list()
        for i in range(len(max(wordList, key=len))):
            theSame = True
            if len(wordList[0]) - 1 >= i:
                letter = wordList[0][i]
            else:
                continue
            for j in wordList:
                if len(j) - 1 < i or j[i] != letter:
                    theSame = False
                    break
            if theSame:
                gsindex.append(i)
                gss.append(letter)
                gs.append((letter, i))
        for i in wordList:
            for c, j in enumerate(i):
                if not (j, c) in gs:
                    freq[j][c] += 1.0
        for c in range(len(wordList)):
            word = wordList[c]
            #if tuple(sorted(guesses + [word])) in calced:
                #localWords[c] = calced[tuple(sorted(guesses + [word]))]
                #continue
            x = bestTwoScore(guesses + [word], wordList, freq)
            #y = array(list(x.values()))
            #localWords[c] = sum(square(y))/len(wordList)
            localWords[c] = x
            #calced[tuple(sorted(guesses + [word]))] = localWords[c]
        bestWords[0] = (min(localWords), argmin(localWords))
    bestWord = min(bestWords)
    return (wordList[bestWord[1]], bestWord[0])
def score(guesses, wordList, calcFunc):
    x = betterWord(guesses, wordList, calcFunc)
    score = sum(square(list(x.values())))/len(wordList)
    return score
def getLeftovers(guesses, wordList, calcFunc):
    x = betterWord(guesses, wordList, calcFunc, True)
    count = 0
    for words in x.values():
        if len(words) > 1:
            count += len(words)
        if len(words) > 2:
            print(words, list(getBestThree(wordList, words, calcFunc).items())[len(words) - 1])
    print(count)
    return score(guesses, wordList, calcFunc)
def powerset(s):
    x = len(s)
    out = []
    for i in range(1 << x):
        out.append([s[j] for j in range(x) if (i & (1 << j))])
    return out
def driverHard(fileGuess, filePoss, wordLen = -1, calcFunc = calcWord):
    global calcs
    WORDLENGTH = int(wordLen)
    numWords = 1
    words = []
    wordsGuess = []
    with open(filePoss, "r") as file:
        for i in file:
            if len(i.strip()) == WORDLENGTH or WORDLENGTH == -1:
                words.append(i.strip())
    with open(fileGuess, "r") as file:
        for i in file:
            if len(i.strip()) == WORDLENGTH or WORDLENGTH == -1:
                wordsGuess.append(i.strip())
    try:
        with open("fringe.p", "rb") as file:
            fringe = pickle.load(file)
    except:
        fringe = [(0, 0, [])]
    try:
        with open("completed.p", "rb") as file:
            completed = pickle.load(file)
    except:
        completed = []
    #betterWord(words, words, calcFunc)
    #print(len(betterCalc))
    stamp = time.time()
    while len(fringe) > 0:
        guesses = heapq.heappop(fringe)[2]
        if set(guesses) in completed:
            continue
        next = nextWord(guesses, words, calcFunc)
        next = list(next)
        next[1] = score(guesses + [next[0]], words, calcFunc)
        if next[1] <= 1:
            return
        completed.append(set(guesses))
        with open("statesearch.txt", "a") as file:
            file.write(f"{guesses} -> {next}\n")
        print(guesses, next, time.time() - stamp)
        stamp = time.time()
        for guess in powerset(guesses + [next[0]]):
            if set(guess) in completed:
                continue
            heapq.heappush(fringe, (len(guess), next[1], guess))
        with open("fringe.p", "wb") as file:
            pickle.dump(list(fringe), file)
        with open("completed.p", "wb") as file:
            pickle.dump(completed, file)
def driverFast(fileGuess, filePoss, wordLen = -1, calcFunc = calcWord):
    WORDLENGTH = int(wordLen)
    numWords = 1
    words = []
    wordsGuess = []
    with open(filePoss, "r") as file:
        for i in file:
            if len(i.strip()) == WORDLENGTH or WORDLENGTH == -1:
                words.append(i.strip())
    with open(fileGuess, "r") as file:
        for i in file:
            if len(i.strip()) == WORDLENGTH or WORDLENGTH == -1:
                wordsGuess.append(i.strip())
    guesses = ["cured", "slant", "pigmy", "howbe"]
    while True:
        outputs = []
        exceptions = {('yrrrr', 'ryyrr', 'rrrrr', 'rgrrr'): "falls", ('ryrrr', 'rrygg', 'rrrrr', 'rrrrr'): "ajiva"}
        wordsEdit = list(words)
        for guess in guesses:
            outputs.append(input(f"{guess}: "))
            wordsEdit = remove(wordsEdit, outputs[-1], guess, calcFunc)
        if tuple(outputs) in exceptions:
            word = exceptions[tuple(outputs)]
        else:
            word = wordsEdit[0]
        if len(wordsEdit) > 1:
            x = input(f"{word}: ")
            wordsEdit = remove(wordsEdit, x, word, calcFunc)
        print(wordsEdit[0])
def driver(fileGuess, filePoss, wordLen = -1, calcFunc = calcWord):
    WORDLENGTH = int(wordLen)
    numWords = 1
    words = list()
    wordsGuess = list()
    with open(filePoss, "r") as file:
        for i in file:
            if len(i.strip()) == WORDLENGTH or WORDLENGTH == -1:
                words.append(i.strip())
    with open(fileGuess, "r") as file:
        for i in file:
            if len(i.strip()) == WORDLENGTH or WORDLENGTH == -1:
                wordsGuess.append(i.strip())
    first = True
    firstTime = True
    wordsEdit = [words]
    while True:
        if not first or firstTime:
            if first:
                try:
                    with open(f"firsts/{fileGuess}{filePoss}{wordLen}.pickle", "rb") as f:
                        wordBest = pickle.load(f)
                except:
                    wordBest = getBestThree(wordsGuess, wordsEdit, calcFunc)
            else:
                wordBest = getBestThree(wordsGuess, wordsEdit, calcFunc)
        else:
            wordBest = firstWord
        first = False
        if firstTime:
            firstWord = wordBest
            firstTime = False
            first = False
            with open(f"firsts/{fileGuess}{filePoss}{wordLen}.pickle", "wb+") as f:
                    #pickle.dump(wordBest, f)
                    pass
        word = list(wordBest.keys())[0]
        val = 0
        print(word, len(flatten(wordsEdit)), wordBest[word])
        for j in range(len(wordsEdit)):
            if len(wordsEdit[j]) == 1:
                continue
            x = input("Output for word %d: " % (j))
            while x == "":
                val += 1
                word = list(wordBest.keys())[val]
                print(word)
                x = input("Output for word %d: " % (j))
            if x == "quit":
                return
            wordsEdit[j] = remove(wordsEdit[j], x, word, calcFunc)
            if len(wordsEdit[j]) == 0:
                print("ZERO WORDS")
                return
        if len(flatten(wordsEdit)) == len(wordsEdit) or x == "redo":
            if x != "redo":
                print(f"The word is {wordsEdit}")
            wordsEdit = list()
            numWords = input("Num words: ")
            for i in range(int(numWords)):
                wordsEdit.append(list(words))
            first = True
            turn = 0
        elif len(flatten(wordsEdit)) == 0:
            print("No words left, something gone wrong")
            return
def driverInfinite(fileGuess, filePoss, wordLen = -1, calcFunc = calcWord):
    WORDLENGTH = int(wordLen)
    numWords = 1
    file = open(filePoss, "r")
    file2 = open(fileGuess, "r")
    words = list()
    wordsGuess = list()

    for i in file:
        if len(i.strip()) == WORDLENGTH or WORDLENGTH == -1:
            words.append(i.strip())
    for i in file2:
        if len(i.strip()) == WORDLENGTH or WORDLENGTH == -1:
            wordsGuess.append(i.strip())
    file.close()
    file2.close()
    first = True
    firstTime = True
    wordsEdit = [words]
    while True:
        if not first or firstTime:
            if first:
                try:
                    with open(f"firsts/{fileGuess}{filePoss}{wordLen}.pickle", "rb") as f:
                        wordBest = pickle.load(f)
                except:
                    wordBest = getBestThree(wordsGuess, wordsEdit, calcFunc)
            else:
                wordBest = getBestThree(wordsGuess, wordsEdit, calcFunc)
        else:
            wordBest = {finalWord: firstWord[finalWord]}
        first = False
        if firstTime:
            firstWord = wordBest
            firstTime = False
            first = False
            with open(f"firsts/{fileGuess}{filePoss}{wordLen}.pickle", "wb+") as f:
                    pickle.dump(wordBest, f)
        word = list(wordBest.keys())[0]
        val = 0
        print(word, len(flatten(wordsEdit)), wordBest[word])
        for j in range(len(wordsEdit)):
            if len(wordsEdit[j]) == 1:
                continue
            x = input("Output for word %d: " % (j))
            while x == "":
                val += 1
                word = list(wordBest.keys())[val]
                print(word)
                x = input("Output for word %d: " % (j))
            if x == "quit":
                return
            wordsEdit[j] = remove(wordsEdit[j], x, word, calcFunc)
            if len(wordsEdit[j]) == 0:
                print("ZERO WORDS")
                return
        if len(flatten(wordsEdit)) == len(wordsEdit) or x == "redo":
            finalWord = wordsEdit[0][0]
            wordsEdit = list()
            for i in range(int(numWords)):
                wordsEdit.append(list(words))
            first = True
            turn = 0
        elif len(flatten(wordsEdit)) == 0:
            print("No words left, something gone wrong")
            return
def main(args):
    if len(args) == 1:
        print("Please enter a file name")
        return
    if "-h" in args:
        if len(args) < 2:
            print("Please enter a file name")
            return
        driverHard(args[2], args[3], args[4])
    elif "-i" in args:
        if len(args) < 3:
            print("Please enter a file name")
            return
        driverInfinite(args[2], args[3], args[4])
    elif "-f" in args:
        if len(args) < 3:
            print("Please enter a file name")
            return
        driverFast(args[2], args[3], args[4])
    else:
        if len(args) < 3:
            print("Please enter a file name")
            return
        driver(args[1], args[2], args[3])
    

if __name__ == "__main__":
    main(sys.argv)