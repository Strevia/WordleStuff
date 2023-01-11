from collections import defaultdict
import heapq
from itertools import combinations
import math
import random
import time
import pymp
from numpy import argmax, argmin, array, square
from tqdm import tqdm
import matplotlib.pyplot as plt
import pickle, sys
class Tree:
    def __init__(self, data):
        self.children = {}
        self.data = data
    def __str__(self):
        return self.data

def zero():
    return 0
calcHard = {}
def getBestHard(wordList, calcFunc, recursion = 0):
    global calcHard
    if tuple(wordList) in calcHard:
        return calcHard[tuple(wordList)]
    if len(wordList) <= 2:
        return (wordList[0], 1)
    output = {}
    for guess in tqdm(wordList, desc=f"Hard {recursion}", leave=False):
        if recursion == 0 and len(set(guess)) < 5:
            break
        if recursion == 0:
            print(f"Guessing {guess}")
        calc = defaultdict(list)
        for poss in wordList:
            if guess != poss:
                calc[calcFunc(guess, poss)].append(poss)
        score = 0
        for i in tqdm(calc.values(), desc=f"Buckets {recursion}", leave=False):
            score = max(score, getBestHard(i, calcFunc, recursion + 1)[1] + 1)
        output[guess] = score
        if recursion == 0:
            print(f"{guess} {score}")
    calcHard[tuple(wordList)] = min(output.items(), key=lambda item: item[1])
    #print(calcHard[tuple(wordList)], wordList)
    return min(output.items(), key=lambda item: item[1])

    
def getBestThree(wordListGuess, wordListPoss, calcFunc):
  out = defaultdict(int)
  if not isinstance(wordListPoss[0], list):
      wordListPoss = [wordListPoss]
  for c, guess in tqdm(enumerate(wordListGuess), total=len(wordListGuess), desc="Guessing", leave=False):
    for wordlist in wordListPoss:
        contain = defaultdict(zero)
        for poss in wordlist:
            if guess != poss:
                contain[calcFunc(guess, poss)] += 1
        out[guess] += sum(square(array(list(contain.values())))/len(wordlist))/len(wordListPoss)
  wordFreqSort = dict(sorted(out.items(), key=lambda item: item[1]))
  return wordFreqSort
def getBestTwo(wordListPoss, wordListGuess):
    freq = {}
    for i in "abcdefghijklmnopqrstuvwxyz":
        freq[i] = [0] * 5
    for i in wordListPoss:
        for c, char in enumerate(i):
            freq[char][c] += 1
    wordFreq = defaultdict(zero)
    for i in wordListGuess:
      wordFreq[i] = bestTwoScore(i, wordListPoss, freq)
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
        #betterCalc[guess] = out
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
def nextWord(guesses, wordListPoss, wordListGuess, calcFunc):
    doneAny = False
    leeway = 0
    while not doneAny:
        localWords = [len(wordListGuess)] * len(wordListGuess)
        for c in tqdm(range(len(wordListGuess)),desc="Calculating", leave=False):
            word = wordListGuess[c]
            if len(set(''.join(guesses) + word)) < len(''.join(guesses) + word) - leeway:
                continue
            doneAny = True
            x = score(guesses + [word], wordListPoss, calcFunc)
            localWords[c] = x
        bestWords = (min(localWords), argmin(localWords))
        leeway += 1
    return (wordListGuess[bestWords[1]], bestWords[0])
scores = {}
def score(guesses, wordList, calcFunc):
    global scores
    if tuple(sorted(guesses)) in scores:
        return scores[tuple(sorted(guesses))]
    x = betterWord(guesses, wordList, calcFunc)
    #score = sum(square(list(x.values())))/len(wordList)
    score = len(wordList) - list(x.values()).count(1)
    #score = len(wordList) - list(x.values()).count(1)
    scores[tuple(sorted(guesses))] = score
    return score
def getLeftovers(guesses, wordList, calcFunc):
    x = betterWord(guesses, wordList, calcFunc, True)
    count = 0
    leftover = []
    for words in x.values():
        if len(words) > 1:
            count += len(words)
            leftover.append(words)
    return leftover
def powerset(s):
    x = len(s)
    out = []
    for i in range(1 << x):
        out.append([s[j] for j in range(x) if (i & (1 << j))])
    return out
#return everything in list except index i
def removeIndex(l, i):
    return l[:i] + l[i+1:]
#find difference between two strings
def diff(s1, s2):
    return [i for i in range(len(s1)) if s1[i] != s2[i]]
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
            if (len(i.strip()) == WORDLENGTH or WORDLENGTH == -1):
                wordsGuess.append(i.strip())
    completed = []
    fringe = [(0, [])]
    freq = betterWord(["fuzzy"], words, calcFunc)
    labels = list(freq.keys())
    sizes = list(freq.values())
    plt.pie(sizes, startangle=90)
    plt.axis('equal')
    plt.title("Fuzzy Buckets")
    plt.legend(labels,bbox_to_anchor=(2, 2))
    plt.show()
    print(freq)
    """try:
        with open("statesearch.txt", "r") as file:
            lines = file.readlines()
            for line in tqdm(lines, desc = "Reading Log", leave = False, total=len(lines)):
                lineSplit = line.split(",")
                guesses = lineSplit[0].split(" ")
                if set(guesses) in completed:
                    continue
                guesses[:] = [x for x in guesses if x != '']
                completed.append(set(guesses))
                if lineSplit[1] == wordsGuess[0] or set(guesses + [lineSplit[1]]) in completed:
                    continue
                for guess in powerset(guesses + [lineSplit[1]]):
                    if set(guess) in completed:
                        continue
                    heapq.heappush(fringe, (len(guess), float(lineSplit[2]), guess))
    except:
        fringe = [(0, [])]
        completed = []
    if len(fringe) == 0:
        fringe = [(0, [])]
    #betterWord(words, words, calcFunc)
    #print(len(betterCalc))
    stamp = time.time()
    while len(fringe) > 0:
        guesses = heapq.heappop(fringe)[-1]
        if set(guesses) in completed:
            continue
        next = nextWord(guesses, words, wordsGuess, calcFunc)
        if next[1] <= 1:
            return
        completed.append(set(guesses))
        with open("statesearch.txt", "a") as file:
            file.write(f"{' '.join(guesses)},{next[0]},{next[1]}\n")
        if next[0] == wordsGuess[0] or set(guesses + [next[0]]) in completed:
            continue
        print(guesses, next, time.time() - stamp)
        stamp = time.time()
        for guess in powerset(guesses + [next[0]]):
            if set(guess) in completed:
                continue
            heapq.heappush(fringe, (len(guess), next[1], guess))"""
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