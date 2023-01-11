# WordleStuff
A few Wordle programs I wrote. One (Wordle) solves them, while Wordall allows you to solve wordles with a custom wordlist.
# Wordle
To run, first cd to the directory /WordleStuff/Wordle. Then, use the following syntax:
For regular mode:
> python ./wordle.py \<Guessable Words\> \<Possible Words\> \<WordLength\>

\<Guessable Words\> and \<Possible Words\> should be names of files in the /Wordle directory. These files should be txt files with one word on each line. 

"Guessable Words" should be the list of words that are accepted as valid, while "Possible Words" should be the list of words that could possibly be the answer.

\<WordLength> should be an integer. Only words with the given word length will be counted from the wordlists. Use -1 to count every word.

Wordle also contains a program for generating the best multi-word combinations.
The scoring system for determining how good a word is is based on all possible words still allowed. Guessable words are tested against all current possible words,
and the one with the lowest score is chosen.
