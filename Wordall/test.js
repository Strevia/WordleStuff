var Color;
(function (Color) {
    Color[Color["green"] = 0] = "green";
    Color[Color["yellow"] = 1] = "yellow";
    Color[Color["black"] = 2] = "black";
})(Color || (Color = {}));
;
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
            out[i] = Color.green;
            counts[char]--;
        }
    }
    for (i = 0; i < guess.length; i++) {
        if (out[i] == Color.green) {
            continue;
        }
        else if (counts[guess[i]] > 0) {
            out[i] = Color.yellow;
            counts[guess[i]]--;
        }
        else {
            out[i] = Color.black;
        }
    }
    return out;
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
getWordList("https://raw.githubusercontent.com/redbo/scrabble/master/dictionary.txt", function (words) {
    var theWord = words[Math.floor(Math.random() * words.length)];
    document.getElementById("submit").addEventListener("click", function (event) {
        var word = document.getElementById("word");
        var guess = word.value.toUpperCase();
        if (words.includes(guess)) {
            var output = "";
            var output2 = "";
            var feedBack = calcWord(theWord, guess);
            var i = void 0;
            var table = document.getElementById("out");
            for (i = 0; i < guess.length; i++) {
                output += ("<span style='color: " + Color[feedBack[i]] + ";'>" + guess[i] + "</span>");
                switch (feedBack[i]) {
                    case Color.green:
                        output2 += 'g';
                        break;
                    case Color.yellow:
                        output2 += 'y';
                        break;
                    case Color.black:
                        output2 += 'r';
                        break;
                }
            }
            var cell = table.insertRow();
            cell.innerHTML = output;
            document.getElementById("forAlg").innerHTML = output2;
            if (guess == theWord) {
                window.alert("You win!");
            }
        }
        else {
            console.log(guess, words);
            window.alert("Invalid word");
        }
    });
}, function (error) {
    console.log(error);
    window.alert("Something went wrong: " + error);
});
