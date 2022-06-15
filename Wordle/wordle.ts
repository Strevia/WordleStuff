function sum(arr: Array<number>): number {
    return arr.reduce((pv, cv) => pv + cv, 0);
}
function square(arr: Array<number>): Array<number> {
    return arr.map(x => x * x);
}
function getBestNormal(wordListGuess: Array<string>, wordListPoss: Array<string>, calcFunc: Function): Array<any[]> {
    let out: {[key: string]: number} = {};
    for (let i = 0; i < wordListGuess.length; i++) {
        let guess = wordListGuess[i];
        let contain: {[key: string]: number} = {};
        for (let j = 0; j < wordListPoss.length; j++) {
            let poss = wordListPoss[j];
            if (guess != poss){
                let calc = calcFunc(guess, poss);
                if (contain[calc] == undefined){
                    contain[calc] = 0;
                }
                contain[calc]++;
            }
        }
        //out[guess] = sum(square(Object.values(contain)))/wordListPoss.length;
        out[guess] = Math.max(...Object.values(contain));
    }
    let sorted = [];
    for (let key in out){
        sorted.push([key, out[key]]);
    }
    sorted.sort((a, b) => a[1] - b[1]);
    console.log(sorted)
    return sorted;
}
function calcWord(theWord: string, guess: string): string {
    let counts: { [name: string]: number } = {};
    let i: number;
    let out: {[key: number]: string} = {};
    for (i = 0; i < theWord.length; i++){
        let char = theWord[i];
        if (!(char in counts)){
            counts[char] = 0;
        }
        counts[char]++;
        if (char == guess[i]){
            out[i] = "g"
            counts[char]--;
        }
    }
    for (i = 0; i < guess.length; i++){
        if (out[i] == "g"){
            continue
        }
        else if (counts[guess[i]] > 0){
            out[i] = "y"
            counts[guess[i]]--;
        } else {
            out[i] = "r"
        }
    }
    let output = "";
    for (i = 0; i < guess.length; i++){
        output += out[i];
    }
    return output;
}
function remove(wordList: Array<string>, output: string, guess: string, calcFunc: Function): Array<string>{
    let newList = [];
    for (let word in wordList){
        if (calcFunc(wordList[word], guess) == output){
            newList.push(wordList[word]);
        }
    }
    return newList;
}
function deepCopy(obj: any): any {
    return JSON.parse(JSON.stringify(obj));
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
function onlyUnique(value, index, self) {
    return self.indexOf(value) === index;
}
//POSSIBLE WORDS, THEN GUESSING WORDS
const possibles = "https://gist.githubusercontent.com/cfreshman/a03ef2cba789d8cf00c08f767e0fad7b/raw/28804271b5a226628d36ee831b0e36adef9cf449/wordle-answers-alphabetical.txt"
const guesses ="https://gist.githubusercontent.com/cfreshman/cdcdf777450c5b5301e439061d29694c/raw/b8375870720504ecf89c1970ea4532454f12de94/wordle-allowed-guesses.txt"
let firstLookup: {[key: string]: Array<any>} = localStorage.getItem("firstLookup") == undefined ? {} : JSON.parse(localStorage.getItem("firstLookup"));
getWordList(possibles, function(words: Array<string>){
    getWordList(guesses, function(wordsGuess: Array<string>){
        //THE CODE
        initializeGame(words, wordsGuess);
    }, function(error){
        console.log(error);
        window.alert("Something went wrong: " + error)
    })
}, function(error){
    console.log(error);
    window.alert("Something went wrong: " + error)
})
function submitWord(best: string, wordsEdit: Array<string>): Array<string>{
    let outputField = document.getElementById("output") as HTMLInputElement;
    let output = outputField.value;
    return remove(wordsEdit, output, best, calcWord);
}
function initializeGame(words: Array<string>, wordsGuess: Array<string>){
    wordsGuess = words.concat(wordsGuess).filter(onlyUnique);
    let wordsEdit = deepCopy(words)
    let wordsGuessEdit = deepCopy(wordsGuess)
    let bestNormal: Array<any>;
    if (possibles + guesses in firstLookup){
        bestNormal = firstLookup[possibles + guesses];
    } else {
        bestNormal = getBestNormal(wordsGuess, words, calcWord);
        firstLookup[possibles + guesses] = bestNormal;
        localStorage.setItem("firstLookup", JSON.stringify(firstLookup));
    }
    let best = bestNormal[0][0];
    document.getElementById("guess").innerHTML = best;
    document.getElementById("ready").innerHTML = "Ready";
    document.getElementById("submit").addEventListener("click", function(event){
        event.preventDefault();
        submit();
        }
    );
    document.addEventListener("keyup", function(event) {
        if (event.code == "Enter") {
            event.preventDefault();
            submit();
        }
    });
    function submit(){
        wordsEdit = submitWord(best, wordsEdit);
        let outputField = document.getElementById("output") as HTMLInputElement;
        let output = outputField.value;
        wordsGuessEdit = remove(wordsGuessEdit, output, best, calcWord);
        if (wordsEdit.length == 1){
            window.alert("The word is " + wordsEdit[0]);
            wordsEdit = deepCopy(words);
            wordsGuessEdit = deepCopy(wordsGuess);
            bestNormal = firstLookup[possibles + guesses];
            best = bestNormal[0][0];
        } else if (wordsEdit.length == 0){
            window.alert("Something wrong, reload")
        } else {
            console.log(wordsGuessEdit)
            bestNormal = getBestNormal(wordsGuessEdit, wordsEdit, calcWord);
            best = bestNormal[0][0];
        }
        document.getElementById("guess").innerHTML = best;
        outputField = document.getElementById("output") as HTMLInputElement;
        outputField.value = "";
    }
}