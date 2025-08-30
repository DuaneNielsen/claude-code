---
description: play a game of hangman
---

# algorithm

create a new hangman session

while (game_is_playable) todo:
   create the following todo list
   1. restate what is known
   2. guess 5 words
   3. consider which letter
   4. guess a letter 


## game_is_playable
the game of hangman is won or lost

## guess 5 words
the words should have the same number of letters as the target does

## consider which letter
look at the words you guessed and calculate which letter will reveal the most information
prefer vowels over consonants

## output format

if game won

    I won! 🎉🎉🎉 I won! The word was <the_word>! 
 
else

    I lost :(  I should have guessed the word <the_word>