from collections import defaultdict
from numpy import array, square
import pickle, sys
class Tree:
    def __init__(self, data):
        self.children = {}
        self.data = data
    def __str__(self):
        return self.data

def zero():
    return 0
def fourthWord(wordList):
    words = ["forge", "pluck"]
    banned = "qxzvwj"
    letters = set()
    for w in words:
        for c in w:
            letters.add(c)
    for word in wordList:
        good = True
        for c in word:
            if c in letters or c in banned:
                good = False
                break
        if good and len(set(word)) == 5:
            for word2 in wordList:
                good2 = True
                for c in word2:
                    if c in letters or c in banned:
                        good2 = False
                        break
                if good2 and len(set(word+word2)) == 10:
                    print(word, word2)
def getBestHard(wordList, calcFunc, recursionLength=0):
    if len(wordList) <= 2:
        return (len(wordList), Tree(wordList[0]))
    print(wordList, recursionLength)
    out = defaultdict(dict)
    if len(set(wordList)) <= 1:
        return (1, Tree(wordList[0]))
    heuristic = ["lares"]
    smallest = len(wordList)
    for guess in wordList:
        if guess in heuristic or recursionLength > 0:
            done = False
            contain = defaultdict(list)
            for poss in wordList:
                if guess != poss:
                    contain[calcFunc(guess, poss)].append(poss)
                    if len(contain[calcFunc(guess, poss)]) > smallest:
                        done = True
                        break
            if not done:
                for output, words in contain.items():
                    down = getBestHard(words, calcFunc, recursionLength+1)
                    out[guess][output] = down
                    smallest = max(smallest, len(words))
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
def getBestTwo(wordList1, wordList2, calcFunc = calcWord): #wordlist1 guess wordlist2 possible
  words = list()
  best = "lares"
  words.append(best)
  print(best)
  print()
  containers = defaultdict(list)
  for word in flatten(wordList2):
    calculations = calcWord(word, best)
    containers[calculations].append(word)
  best2 = list(getBestThree(wordList1, list(containers.values()), calcFunc).keys())[0]
  print(best2)
  print()
  words.append(best2)
  done = False
  while not done:
    done = True
    containers2 = defaultdict(list)
    for cont in containers:
      for word in containers[cont]:
        calculations = calcWord(word, best2)
        containers2[(cont, calculations)].append(word)
        if len(containers2[(cont, calculations)]) > 1:
          done = False
    best2 = list(getBestThree(wordList1, list(containers2.values()), calcFunc).keys())[0]
    words.append(best2)
    print(best2)
    print()
    containers = dict(containers2)
    if len(words) == 4:
      done = True
  count = 0
  for cont in containers2.values():
      if list(getBestThree(wordList1, [cont]).values())[0] > 1:
          count += 1
  print(count, len(wordList2[0]), count/len(wordList2[0]))
  return words
def flatten(t):
    return [item for sublist in t for item in sublist]
def driverHard(fileName, wordLen = -1, calcFunc = calcWord):
    WORDLENGTH = int(wordLen)
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
def driver(fileGuess, filePoss, wordLen = -1, calcFunc = calcWord):
    WORDLENGTH = int(wordLen)
    numWords = 1
    words = list()
    wordsGuess = list()
    with open(filePoss, "r") as file:
        for i in file:
            if len(i.strip()) == WORDLENGTH or WORDLENGTH == -1:
                words.append(i.strip())
    with open(fileGuess, "r'") as file:
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
        driverHard(args[2], args[3])
    elif "-i" in args:
        if len(args) < 3:
            print("Please enter a file name")
            return
        driverInfinite(args[2], args[3], args[4])
    else:
        if len(args) < 3:
            print("Please enter a file name")
            return
        driver(args[1], args[2], args[3])
    

if __name__ == "__main__":
    main(sys.argv)