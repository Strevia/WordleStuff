function sum(arr: Array<number>): number {
    return arr.reduce((pv, cv) => pv + cv, 0);
}
function square(arr: Array<number>): Array<number> {
    return arr.map(x => x * x);
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
        getBestFast(words, wordsGuess)
    }, function(error){
        console.log(error);
        window.alert("Something went wrong: " + error)
    })
}, function(error){
    console.log(error);
    window.alert("Something went wrong: " + error)
})
function press(key: string){
    const keyboard = ["qwertyuiop", "asdfghjkl", "zxcvbnm"];
    let i: number;
    let j: number;
    if (key == "enter"){
        i = 2;
        j = 8;
    }
    else if (keyboard[0].includes(key)){
        i = 0;
        j = keyboard[0].indexOf(key);
    } else if (keyboard[1].includes(key)){
        i = 1;
        j = keyboard[1].indexOf(key);
    } else if (keyboard[2].includes(key)){
        i = 2;
        j = keyboard[2].indexOf(key) + 1;
    }
    let button = document.getElementsByClassName("Game-keyboard")[0].children[i].children[j] as HTMLButtonElement;
    button.click()
}
function getBestFast(words: Array<string>, wordsGuess: Array<string>): void {
    const guessing = ["grand", "spicy", "thumb", "vowel"]
    setInterval(function() {
        press("enter")
        let outputs: string = "";
        let wordsEdit = deepCopy(words)
        for (let guess in guessing){
            let guessWord = guessing[guess];
            for (var i = 0; i < guessWord.length; i++) {
            press(guessWord.charAt(i))
            }
            press("enter")
        }
        let rows = document.getElementsByClassName("Row-locked-in")
        for (i = 0; i < rows.length; i++){
            let row = rows[i].children as HTMLCollection;
            for (let j = 0; j < row.length; j++){
                let letter = row[j] as HTMLElement
                if (letter.getAttribute("class").includes("letter-absent")){
                    outputs += "r"
                } else if (letter.getAttribute("class").includes("letter-correct")){
                    outputs += "g"
                } else {
                    outputs += "y"
                }

            }
            outputs += ","
        }
        let outputSplits = outputs.split(",")
        outputSplits.pop()
        for (let i = 0; i < outputSplits.length; i++){
            wordsEdit = remove(wordsEdit, outputSplits[i], guessing[i], calcWord)
        }
        let word = wordsEdit[0]
        if (wordsEdit.length > 1){
            for (let i = 0; i < word.length; i++){
                press(word.charAt(i))
            }
            press("enter")
            let output: string;
            let row = document.getElementsByClassName("Row-locked-in")[4].children as HTMLCollection;
            outputs = "";
            for (let j = 0; j < row.length; j++){
                let letter = row[j] as HTMLElement
                if (letter.getAttribute("class").includes("letter-absent")){
                    outputs += "r"
                } else if (letter.getAttribute("class").includes("letter-correct")){
                    outputs += "g"
                } else {
                    outputs += "y"
                }

            }
            wordsEdit = remove(wordsEdit, outputs, word, calcWord)
        }
        word = wordsEdit[0]
        for (let i = 0; i < word.length; i++){
            press(word.charAt(i))
        }
        press("enter")
    }, 0);
}