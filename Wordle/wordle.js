function sum(arr) {
    return arr.reduce(function (pv, cv) { return pv + cv; }, 0);
}
function square(arr) {
    return arr.map(function (x) { return x * x; });
}
function getBestNormal(wordListGuess, wordListPoss, calcFunc) {
    var out = {};
    for (var i = 0; i < wordListGuess.length; i++) {
        var guess = wordListGuess[i];
        var contain = {};
        for (var j = 0; j < wordListPoss.length; j++) {
            var poss = wordListPoss[j];
            if (guess != poss) {
                var calc = calcFunc(guess, poss);
                if (contain[calc] == undefined) {
                    contain[calc] = 0;
                }
                contain[calc]++;
            }
        }
        //out[guess] = sum(square(Object.values(contain)))/wordListPoss.length;
        out[guess] = Math.max.apply(Math, Object.values(contain));
    }
    var sorted = [];
    for (var key in out) {
        sorted.push([key, out[key]]);
    }
    sorted.sort(function (a, b) { return a[1] - b[1]; });
    console.log(sorted);
    return sorted;
}
function calcWord(theWord, guess) {
    var counts = {};
    var i;
    var out = {};
    for (i = 0; i < theWord.length; i++) {
        var char = theWord[i];
        if (!(char in counts)) {
            counts[char] = 0;
        }
        counts[char]++;
        if (char == guess[i]) {
            out[i] = "g";
            counts[char]--;
        }
    }
    for (i = 0; i < guess.length; i++) {
        if (out[i] == "g") {
            continue;
        }
        else if (counts[guess[i]] > 0) {
            out[i] = "y";
            counts[guess[i]]--;
        }
        else {
            out[i] = "r";
        }
    }
    var output = "";
    for (i = 0; i < guess.length; i++) {
        output += out[i];
    }
    return output;
}
function remove(wordList, output, guess, calcFunc) {
    var newList = [];
    for (var word in wordList) {
        if (calcFunc(wordList[word], guess) == output) {
            newList.push(wordList[word]);
        }
    }
    return newList;
}
function deepCopy(obj) {
    return JSON.parse(JSON.stringify(obj));
}
var getWordList = function (url, resolve, reject) {
    fetch(url)
        .then(function (response) {
        if (response.status !== 200) {
            console.log('Looks like there was a problem. Status Code: ' +
                response.status);
            reject(response.status);
        }
        response.text()
            .then(function (data) {
            var wordArray = data.split('\n');
            resolve(wordArray);
        });
    })["catch"](function (err) {
        console.log('Fetch Error :-S', err);
        reject(err);
    });
};
function onlyUnique(value, index, self) {
    return self.indexOf(value) === index;
}
//POSSIBLE WORDS, THEN GUESSING WORDS
var possibles = "https://gist.githubusercontent.com/cfreshman/a03ef2cba789d8cf00c08f767e0fad7b/raw/28804271b5a226628d36ee831b0e36adef9cf449/wordle-answers-alphabetical.txt";
var guesses = "https://gist.githubusercontent.com/cfreshman/cdcdf777450c5b5301e439061d29694c/raw/b8375870720504ecf89c1970ea4532454f12de94/wordle-allowed-guesses.txt";
var firstLookup = localStorage.getItem("firstLookup") == undefined ? {} : JSON.parse(localStorage.getItem("firstLookup"));
getWordList(possibles, function (words) {
    getWordList(guesses, function (wordsGuess) {
        //THE CODE
        initializeGame(words, wordsGuess);
    }, function (error) {
        console.log(error);
        window.alert("Something went wrong: " + error);
    });
}, function (error) {
    console.log(error);
    window.alert("Something went wrong: " + error);
});
function submitWord(best, wordsEdit) {
    var outputField = document.getElementById("output");
    var output = outputField.value;
    return remove(wordsEdit, output, best, calcWord);
}
function initializeGame(words, wordsGuess) {
    wordsGuess = words.concat(wordsGuess).filter(onlyUnique);
    var wordsEdit = deepCopy(words);
    var wordsGuessEdit = deepCopy(wordsGuess);
    var bestNormal;
    if (possibles + guesses in firstLookup) {
        bestNormal = firstLookup[possibles + guesses];
    }
    else {
        bestNormal = getBestNormal(wordsGuess, words, calcWord);
        firstLookup[possibles + guesses] = bestNormal;
        localStorage.setItem("firstLookup", JSON.stringify(firstLookup));
    }
    var best = bestNormal[0][0];
    document.getElementById("guess").innerHTML = best;
    document.getElementById("ready").innerHTML = "Ready";
    document.getElementById("submit").addEventListener("click", function (event) {
        event.preventDefault();
        submit();
    });
    document.addEventListener("keyup", function (event) {
        if (event.code == "Enter") {
            event.preventDefault();
            submit();
        }
    });
    function submit() {
        wordsEdit = submitWord(best, wordsEdit);
        var outputField = document.getElementById("output");
        var output = outputField.value;
        wordsGuessEdit = remove(wordsGuessEdit, output, best, calcWord);
        if (wordsEdit.length == 1) {
            window.alert("The word is " + wordsEdit[0]);
            wordsEdit = deepCopy(words);
            wordsGuessEdit = deepCopy(wordsGuess);
            bestNormal = firstLookup[possibles + guesses];
            best = bestNormal[0][0];
        }
        else if (wordsEdit.length == 0) {
            window.alert("Something wrong, reload");
        }
        else {
            console.log(wordsGuessEdit);
            bestNormal = getBestNormal(wordsGuessEdit, wordsEdit, calcWord);
            best = bestNormal[0][0];
        }
        document.getElementById("guess").innerHTML = best;
        outputField = document.getElementById("output");
        outputField.value = "";
    }
}
