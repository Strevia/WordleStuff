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
var possibles = "https://gist.githubusercontent.com/cfreshman/a03ef2cba789d8cf00c08f767e0fad7b/raw/28804271b5a226628d36ee831b0e36adef9cf449/wordle-answers-alphabetical.txt";
var guesses = "https://gist.githubusercontent.com/cfreshman/cdcdf777450c5b5301e439061d29694c/raw/b8375870720504ecf89c1970ea4532454f12de94/wordle-allowed-guesses.txt";
getWordList(possibles, function (words) {
    getWordList(guesses, function (wordsGuess) {
        //THE CODE
        var item = words[Math.floor(Math.random()*words.length)];
        window.alert("Your starting word is " + item)
    }, function (error) {
        console.log(error);
        window.alert("Something went wrong: " + error);
    });
}, function (error) {
    console.log(error);
    window.alert("Something went wrong: " + error);
});
