<p align="center">  
  <img src="gui\icon.png" width=150 height=150>
</p>

<h1 align="center">AnkiVocabHelper</h1>

The Anki Vocabulary Helper is a free tool designed to assist learners in expanding their vocabulary in foreign languages. It leverages the wordfreq python library to assess the difficulty of foreign words. The application aids in determining which words should be added to Anki next. Typically, learners prefer to start with words that are easier, more common, and frequently used. This is where wordfreq library comes into play - it evaluates the complexity of words, allowing users to prioritize learning words based on their difficulty level.

![Screenshot](Screenshot_1.png)

The primary purpose of this application is to facilitate the tracking of new words for users, particularly those who use Anki for learning languages. 

By using this application, learners can streamline their vocabulary learning process and focus on the most relevant words first.

## Getting Started

To get started with this project, follow these steps:

1. Clone this repository to your local machine.
```
git clone https://github.com/kuronekozero/AnkiVocabHelper.git
```
2. Navigate to the `gui` folder in project directory.

3. Run main.exe file.

That's it!
Optionally you can create a shortcut of main.exe and put it on your desktop for quicker access.

Also for some reason it may tell you that this program may be a virus. No idea how to fix it... In earlier versions of this program everything worked fine.

## Running the Application

To run the application, simply execute the built exe file. You can add new tables and words to assess their difficulty and review them later. 
After adding some words just sort the table by difficulty.

![Screenshot](Screenshot_2.png)

## How to use it?

1. Find a new word that you want to add to your Anki deck in the future. You can find words by watching content on youtube or reading books on the language that you are trying to learn.
  
2. Add this word to the table in AnkiVocabHelper.

3. Whenever you want to add new words to your Anki deck just copy first words from AnkiVocabHelper and make new cards out of it. The first words that you are going to see in the table will be the one that are the most popular among natives in your targeted language. If you want to see the hardest words first, just sort the table by difficulty by clicking on the button "difficulty".

4. Repeat until C2.

## Supported Languages

- **English**
- **Spanish**
- **German**
- **Japanese**
- **Korean**
- **Chinese**
- **Franch**
- **Arabic**
- **Russian**
- **Czech**
- **Hebrew**
- **Polish**
- **Swedish**
- **Norwegian**
- **Dutch**
- **Italian**
- **Bengali**
- **Portuguese**
- **Catalan**

And 20 more languages!

You can check the full list of supported languages on wordfreq's page: 
<a href="https://pypi.org/project/wordfreq/">Wordfreq library page.</a>

PS: I removed slovak and slovenian because this 2 languages didn't work properly for some reason, sorry;( 

Ukranian coming soon.

## Development Updates

### Fixes and Improvements

- ~~**Issue 1**: Fix sorting order.~~ (Completed)
- ~~**Issue 2**: Fix upper case lower case problem.~~ (Completed)
- **Issue 3**: Fix sorting words by date.
- **Issue 4**: Fix colors of tables menu.  

### Planned Additions and Changes

- ~~**Addition/Change 2**: Add option to add sentences of phrases.~~ (Completed)
- ~~**Addition/Change 1**: Add other languages support.~~ (Completed)
- ~~**Addition/Change 3**: Add option to create more than one table.~~ (Completed)
- ~~**Addition/Change 4**: Add stars near each word so the word will be in priority while sorting.~~  (Completed)

## FAQ

### How to delete tables?
Well...:point_right::point_left: I never really managed to add the delete button to the "List of tables" window. But I'll try to add it in the future. For now just go to `gui` folder and delete any table you don't want from there.

### I just installed a newer version of AnkiVocabHelper. How can I move my words from the old version to the new one?
Just copy .db files from the gui folder in the old version of the program and paste them into the new version of the program in the same folder.

### Why do some of my words get a 101 when I add them?
It happens when the WordFreq library can't define the difficulty of a word. It may happen if the word that you are trying to add was written incorrectly or if this is a very unpopular word, like slang, for example. This problem may also occur if you are trying to add words, for example, in Japanese, to the Chinese table. If you created a new table and selected Bosnian as the main language, you can add only Bosnian words to this table. If you want to have more than one language, you need to create a saparate table.

### What does (small) mean near some of the languages?
That means that this language doesn't have a huge database of words, and there are higher chances that you will encounter a word with a score of 101 (even if this word actually exists). You can still use this language, especially if you are not using any complex words or slang. Just keep in mind that there is a chance to encounter words that the program couldn't score occasionally.

### I'm tired of clicking "Add" every time; are there any other ways of adding words?
Yes, instead of clicking "Add," you can just press Enter instead. Also, if you want to add more than one word, you can write a list of words divided by ','. It is supposed to look something like this: "dog, cat, car, language". After that, you can just press Enter and wait until all the words are added to the table.

### What is the purpose of the 'Favorite' field?
Sometimes you want to learn more difficult words first, like, for example, because you have an exam soon and you need to know a specific list of words. In this case, you can just go through the list of words and click on the star icon, so these words will be shown first, no matter how difficult they are.

## Tips 
1. To add a new word you can just press ENTER after typing the word, you don't have to click "add" all the time.
2. If you want to add more than one word at ones you can just write the list of words that you want ot add devided by ",". The program will rate each word separately.
3. You can sort words in each direction from the simplest to the most difficult and in the opposite way by just clicking twice on the "difficulty" button.
4. The word's difficulty varies from 1 to 100. If you are getting the word with number 101 that means that the API doesn't have this word. It happens very rare, usually with some very unpopular words and slang.

## License

This project is licensed under the MIT License.
