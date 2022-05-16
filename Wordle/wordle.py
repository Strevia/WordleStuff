from collections import defaultdict
from numpy import array, square
import pickle
class Tree:
    def __init__(self, data):
        self.children = {}
        self.data = data
    def __str__(self):
        return self.data

def zero():
    return 0
def getBestHard(wordList, calcFunc, ):
    print(wordList)
    out = defaultdict(dict)
    if len(set(wordList)) <= 1:
        return (1, Tree(wordList[0]))
    for guess in wordList:
        contain = defaultdict(list)
        for poss in wordList:
            if guess != poss:
                contain[calcFunc(guess, poss)].append(poss)
        for output, words in contain.items():
            down = getBestHard(words, calcFunc)
            out[guess][output] = down
    mini = float('inf')
    for guess, results in out.items():
        maxi = float('-inf')
        for item in results.values():
            if item[0] > maxi:
                maxi = item[0]
        if maxi < mini:
            mini = maxi
            miniItem = guess
    output = Tree(miniItem)
    for key in out[miniItem]:
        output.children[key] = out[miniItem][key][1]
    return (1 + mini, output)
    
def getBestThree(wordListGuess, wordListPoss, calcFunc):
  out = defaultdict(zero)
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
def calcWord(guess, word):
    counts = defaultdict(zero)
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
    return ''.join(out)
def remove(wordList, output, guess, calcFunc):
    newList = list()
    for word in wordList:
        if calcFunc(guess, word) == output:
            newList.append(word)
    return newList
def flatten(t):
    return [item for sublist in t for item in sublist]
def driverHard(fileName, calcFunc = calcWord, wordLen = -1, firstGuess = None):
    WORDLENGTH = wordLen
    numWords = 1
    file = open(fileName, "r")
    words = list()
    for i in file:
        if len(i.strip()) == WORDLENGTH or WORDLENGTH == -1:
            words.append(i.strip())
    file.close()
    x = getBestHard(words, calcFunc)[1]
    with open("hardmode.pickle") as f:
        pickle.dump(x, f)
    while len(x.children) > 0:
        inp = input(f"Output from {x.data}: ")
        x = x.children[inp]
    print(f"The word is {x.data}")
def driver(fileGuess, filePoss, calcFunc = calcWord, wordLen = -1, firstGuess = None):
    WORDLENGTH = wordLen
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
            wordBest = firstWord
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
            if x != "redo":
                print("The word is ", end="")
                print(wordsEdit)
            wordsEdit = list()
            numWords = input("Num words: ")
            for i in range(int(numWords)):
                wordsEdit.append(list(words))
            first = True
            turn = 0
        elif len(flatten(wordsEdit)) == 0:
            print("No words left, something gone wrong")
            return
wordsDict = dict()