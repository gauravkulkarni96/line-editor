# Line Editor

## Installation and basic usage
1. clone repository ```https://github.com/gauravkulkarni96/line-editor.git```.
2. install pyperclip ```sudo pip install pyperclip``` or ```pip install pyperclip``` inside virtualenv.
3. For Linux, install xclip ```sudo apt-get install xclip```
4. run editor with filename argument ```./ledit.py <fileName>``` or without filename ```./ledit.py```
5. Input "h" to the editor to display list of available commands

## Project Structure
The project contains 3 files-
  1. ledit.py - The main driver program
  2. operations.py - contains the functions of all the operations of editor
  3. checks.py - contains functions to check Integers, number of arguments etc.
