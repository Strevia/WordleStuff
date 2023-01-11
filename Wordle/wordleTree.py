from numpy import array
from collections import defaultdict
import pickle
from tqdm import tqdm
import scipy.cluster.hierarchy
import matplotlib.pyplot as plt

words = []
WORDLENGTH = -1
with open("possibles.txt", "r") as file:
        for i in file:
            if len(i.strip()) == WORDLENGTH or WORDLENGTH == -1:
                words.append(i.strip())
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
def distanceSet(s1, s2):
    out = set()
    letters = set(s1+s2)
    for i in letters:
        for c in range(5):
            check = "*****"
            check = check[:c] + i + check[c+1:]
            if calcWord(check, s1) != calcWord(check, s2):
                out.add((c, (i)))
    return out
dist = {}
def distance(s1, s2):
    if (tuple(s1), tuple(s2)) in dist:
        return dist[(tuple(s1), tuple(s2))]
    distan = len(distanceSet(s1, s2))
    dist[(tuple(s1), tuple(s2))] = distan
    return distan
def distanceMax(s1, l):
    out = set()
    for i in l:
        out.update(distanceSet(s1, i))
    return len(out)
with open("distanceMatrix.p", "rb") as file:
    distanceMatrix = pickle.load(file)
wordPoints = []
for word in words:
    temp = []
    for c in word:
        temp.append(ord(c) - 97)
    wordPoints.append(tuple(temp))
cluster = scipy.cluster.hierarchy.linkage(wordPoints, method="complete")
dend = scipy.cluster.hierarchy.dendrogram(cluster, labels=words)
plt.show()