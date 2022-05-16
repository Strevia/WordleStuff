from collections import defaultdict
from random import shuffle
from os.path import exists
import pickle

from numpy import square

WORDLENGTH = 5
numWords = 1
file = open("scrabble.txt", "r")
file2 = open("scrabble.txt", "r")
words = list()
wordsGuess = list()
try:
    with open("differences.pickle", "rb") as f:
        wordsDict = pickle.load(f)
except:
    wordsDict = dict()

for i in file:
    if len(i.strip()) == WORDLENGTH or WORDLENGTH == -1:
        words.append(i.strip())
for i in file2:
    if len(i.strip()) == WORDLENGTH or WORDLENGTH == -1:
        wordsGuess.append(i.strip())
file.close()
file2.close()
#theWord = random.choice(words)
def noSame(word1, word2):
    for i in word1:
        if i in word2:
            return False
    return True


def flatten(t):
    return [item for sublist in t for item in sublist]


def getBest(wordList1, wordList2):
    letters = set()
    freq = dict()
    wordFreq = defaultdict(zero)
    for i in wordList1:
        for j in i:
          letters = letters.union(set(j))
    for i in wordList2:
      letters = letters.union(set(i))
    for i in letters:
        freq[i] = [0] * len(max(wordList2, key=len))
    for wordList in wordList1:
        if len(wordList) == 0:
            print("SOMETHING WRONG")
            quit()
        elif len(wordList) == 1:
            continue
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
    for i in wordList2:
      summ1, summ2 = 0, 0
      for c, j in enumerate(i):
          summ1 -= freq[j][c]
      for c, j in enumerate(i):
          summ2 -= sum(freq[j])
      wordFreq[i] += (summ1 + summ2 / (1.0 + len(i) - len(set(i))))
    wordFreqSort = dict(sorted(wordFreq.items(), key=lambda item: item[1]))
    return wordFreqSort
def getBestTwo(wordList1, wordList2): #wordlist1 guess wordlist2 possible
  words = list()
  #best = list(getBestThree(wordList1,wordList2).keys())[0]
  best = "lares"
  words.append(best)
  print(best)
  print()
  containers = defaultdict(list)
  for word in flatten(wordList2):
    calculations = calcWord(word, best)
    containers[calculations].append(word)
  best2 = list(getBestThree(wordList1, list(containers.values())).keys())[0]
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
    best2 = list(getBestThree(wordList1, list(containers2.values())).keys())[0]
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

def getBestThree(wordListGuess, wordListPoss):
  global wordsDict
  shuffle(wordListGuess)
  out = defaultdict(zero)
  word = ""
  for c, guess in enumerate(wordListGuess):
    for wordlist in wordListPoss:
        contain = defaultdict(zero)
        for poss in wordlist:
            if guess != poss:
                contain[calcWord(guess, poss)] += 1
        out[guess] += (sum(square(list(contain.values())))/len(wordlist))/len(wordListPoss)
    print(f"{(c)}/{len(wordlist)}")
  wordFreqSort = dict(sorted(out.items(), key=lambda item: item[1]))
  return wordFreqSort

def calcWord(guess, word, file = None):
  global wordsDict
  if (guess, word) in wordsDict:
    return wordsDict[(guess, word)]
  else:
    counts = defaultdict(zero)
    out = [0] * len(guess)
    for i, char in enumerate(word):
      counts[char] += 1
      if char == guess[i]:
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
  wordsDict[(guess, word)] = tuple(out)
  return tuple(out)
def getBestHard(wordList):
    letters = set()
    freq = dict()
    wordFreq = defaultdict(zero)
    for i in wordList:
      letters = letters.union(set(i))
    for i in letters:
        freq[i] = [0] * len(max(wordList, key=len))
    for i in wordList:
        for c, j in enumerate(i):
          freq[j][c] += 1.0
    for i in wordList:
      summ1, summ2 = 0, 0
      for c, j in enumerate(i):
          summ1 -= freq[j][c]
      for c, j in enumerate(i):
          summ2 -= sum(freq[j])
      wordFreq[i] += (-summ1 + summ2 / (1.0 + len(i) - len(set(i))))
    wordFreqSort = dict(sorted(wordFreq.items(), key=lambda item: item[1]))
    return wordFreqSort




def zero():
    return 0


def remove(wordList, greens, yellows, reds):
    newList = list()
    counts = defaultdict(zero)
    for i in greens + yellows:
        counts[i[0]] += 1
    for word in wordList:
        bad = False
        toIgnore = list()
        for green in greens:
            if len(word) < green[1] or word[green[1]] != green[0]:
                bad = True
            for y in yellows:
                if y[0] == green[0]:
                    if word.count(y[0]) < counts[y[0]]:
                        bad = True
            for c, r in enumerate(reds):
                if r[0] == green[0]:
                    if word.count(r[0]) > counts[r[0]] or word[r[1]] == r[0]:
                        bad = True
                    toIgnore.append(r[0])
        for yellow in yellows:
            if (len(word) > yellow[1]
                    and word[yellow[1]] == yellow[0]) or not yellow[0] in word:
                bad = True
            for y in yellows:
                if y[0] == yellow[0] and y[1] != yellow[1]:
                    if word.count(y[0]) < counts[y[0]]:
                        bad = True
            for c, r in enumerate(reds):
                if r[0] == yellow[0]:
                    if word.count(r[0]) > counts[r[0]]:
                        bad = True
                    toIgnore.append(r[0])
        for red in reds:
            if (red[0] in word and len(word) - 1 >= red[1]) and (
                    not red[0] in toIgnore or word[red[1]] == red[0]):
                bad = True
        if not bad:
            #if bad:
            newList.append(word)
    return newList


wordsEdit = list()
for i in range(numWords):
    wordsEdit.append(list(words))
theWord = ""


def maxTwo(wordList):
    file3 = open("noSameDict.txt", "a")
    output = dict()
    for c1 in range(len(wordList)):
        noLetters = list()
        for c2 in range(c1 + 1, len(wordList)):
            if noSame(wordList[c1], wordList[c2]):
                noLetters.append(wordList[c2])
        output[wordList[c1]] = noLetters
        file3.write(wordList[c1]+","+",".join(noLetters)+"\n")
        print(wordList[c1], c1)
    return output
first = True
firstTime = True
while wordsEdit[0] != theWord:
    if not first or firstTime:
      wordBest = getBestThree(wordsGuess, wordsEdit)
    else:
      wordBest = firstWord
      first = False
    if firstTime:
          firstWord = wordBest
          firstTime = False
          first = False
    word = list(wordBest.keys())[0]
    val = 0
    print(word, len(flatten(wordsEdit)), wordBest[word])
    for j in range(len(wordsEdit)):
        if len(wordsEdit[j]) == 1:
            continue
        greens = list()
        yellows = list()
        reds = list()
        x = input("Output for word %d: " % (j))
        while x == "":
            val += 1
            word = list(wordBest.keys())[val]
            print(word)
            x = input("Output for word %d: " % (j))
        if x == "quit":
            with open("differences.pickle", "wb") as f:
                pickle.dump(wordsDict, f)
            exit()
        for c, i in enumerate(x):
            if i == 'g':
                greens.append((word[c], c))
            elif i == 'y':
                yellows.append((word[c], c))
            elif i == 'r':
                reds.append((word[c], c))
        wordsEdit[j] = remove(wordsEdit[j], greens, yellows, reds)
        if len(wordsEdit[j]) == 0:
            print("ZERO WORDS")
            quit()
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
        quit()
    
