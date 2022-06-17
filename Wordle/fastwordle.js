function sum(arr) {
    return arr.reduce(function (pv, cv) { return pv + cv; }, 0);
}
function square(arr) {
    return arr.map(function (x) { return x * x; });
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
        getBestFast(words, wordsGuess);
    }, function (error) {
        console.log(error);
        window.alert("Something went wrong: " + error);
    });
}, function (error) {
    console.log(error);
    window.alert("Something went wrong: " + error);
});
function press(key) {
    var keyboard = ["qwertyuiop", "asdfghjkl", "zxcvbnm"];
    var i;
    var j;
    if (key == "enter") {
        i = 2;
        j = 8;
    }
    else if (keyboard[0].includes(key)) {
        i = 0;
        j = keyboard[0].indexOf(key);
    }
    else if (keyboard[1].includes(key)) {
        i = 1;
        j = keyboard[1].indexOf(key);
    }
    else if (keyboard[2].includes(key)) {
        i = 2;
        j = keyboard[2].indexOf(key) + 1;
    }
    var button = document.getElementsByClassName("Game-keyboard")[0].children[i].children[j];
    button.click();
}
function getBestFast(words, wordsGuess) {
    var guessing = ["cured", "slant", "pigmy", "howbe"];
    setInterval(function () {
        press("enter");
        var outputs = "";
        var exceptions = {};
        exceptions["yrrrr,ryyrr,rrrrr,rgrrr,"] = "falls";
        exceptions["ryrrr,rrygg,rrrrr,rrrrr,"] = "ajiva";
        var wordsEdit = deepCopy(words);
        for (var guess in guessing) {
            var guessWord = guessing[guess];
            for (var i = 0; i < guessWord.length; i++) {
                press(guessWord.charAt(i));
            }
            press("enter");
        }
        var rows = document.getElementsByClassName("Row-locked-in");
        for (i = 0; i < rows.length; i++) {
            var row = rows[i].children;
            for (var j = 0; j < row.length; j++) {
                var letter = row[j];
                if (letter.getAttribute("class").includes("letter-absent")) {
                    outputs += "r";
                }
                else if (letter.getAttribute("class").includes("letter-correct")) {
                    outputs += "g";
                }
                else {
                    outputs += "y";
                }
            }
            outputs += ",";
        }
        var outputSplits = outputs.split(",");
        outputSplits.pop();
        for (var i_1 = 0; i_1 < outputSplits.length; i_1++) {
            wordsEdit = remove(wordsEdit, outputSplits[i_1], guessing[i_1], calcWord);
        }
        var word;
        if (outputs in exceptions)
            word = exceptions[outputs];
        else
            word = wordsEdit[0];
        if (wordsEdit.length > 1) {
            for (var i_2 = 0; i_2 < word.length; i_2++) {
                press(word.charAt(i_2));
            }
            press("enter");
            var output = void 0;
            var row = document.getElementsByClassName("Row-locked-in")[4].children;
            outputs = "";
            for (var j = 0; j < row.length; j++) {
                var letter = row[j];
                if (letter.getAttribute("class").includes("letter-absent")) {
                    outputs += "r";
                }
                else if (letter.getAttribute("class").includes("letter-correct")) {
                    outputs += "g";
                }
                else {
                    outputs += "y";
                }
            }
            wordsEdit = remove(wordsEdit, outputs, word, calcWord);
        }
        word = wordsEdit[0];
        for (var i_3 = 0; i_3 < word.length; i_3++) {
            press(word.charAt(i_3));
        }
        press("enter");
    }, 0);
}
