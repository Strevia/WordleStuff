enum Color {"green", "yellow", "black"};
function calcWord(theWord: string, guess: string): {[key: number]: Color} {
    let counts: { [name: string]: number } = {};
    let i: number;
    let out: {[key: number]: Color} = {};
    for (i = 0; i < theWord.length; i++){
        let char = theWord[i];
        if (!(char in counts)){
            counts[char] = 0;
        }
        counts[char]++;
        if (char == guess[i]){
            out[i] = Color.green;
            counts[char]--;
        }
    }
    for (i = 0; i < guess.length; i++){
        if (out[i] == Color.green){
            continue
        }
        else if (counts[guess[i]] > 0){
            out[i] = Color.yellow;
            counts[guess[i]]--;
        } else {
            out[i] = Color.black;
        }
    }
    return out;
}
const getWordList = (url: string, resolve: Function, reject: Function) => { 
    fetch(url)
    .then(
        function(response) {
        if (response.status !== 200) {
            console.log('Looks like there was a problem. Status Code: ' +
            response.status);
            reject(response.status)
        }
        response.text()
        .then(function(data) {
            let wordArray: string[] = data.split('\n')
            resolve(wordArray)
        })
        }
    )
    .catch(function(err) {
        console.log('Fetch Error :-S', err);
        reject(err)
    });
};
getWordList("https://raw.githubusercontent.com/redbo/scrabble/master/dictionary.txt", function(words: string[]){
    let theWord = words[Math.floor(Math.random()*words.length)];
    document.getElementById("submit").addEventListener("click", function(event){
        let word = document.getElementById("word") as HTMLInputElement;
        let guess = word.value.toUpperCase();
        if (words.includes(guess)){
            let output = "";
            let output2 = "";
            let feedBack = calcWord(theWord, guess);
            let i: number;
            let table = document.getElementById("out") as HTMLTableElement;
            for (i = 0; i < guess.length; i++){
                output += ("<span style='color: " + Color[feedBack[i]] + ";'>" + guess[i] + "</span>");
                switch (feedBack[i]){
                    case Color.green:
                        output2 += 'g'
                        break
                    case Color.yellow:
                        output2 += 'y'
                        break
                    case Color.black:
                        output2 += 'r'
                        break
                }
            }
            let cell = table.insertRow();
            cell.innerHTML = output;
            document.getElementById("forAlg").innerHTML = output2;
            if (guess == theWord){
                window.alert("You win!");
            }
        } else {
            console.log(guess, words)
            window.alert("Invalid word")
        }
    })
    
}, function(error){
    console.log(error);
    window.alert("Something went wrong: " + error)
})