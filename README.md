# pythonScripts
A bunch of python scripts to make life easier

### Email Finder
Use the site `verifyemailaddress.org` to find the professional email address of a person, given a domain. To run:

`python find_email.py`

Add `-h` flag for the help message.

### Word Streak
Generates words from a m x n character grid. Input the grid as rows, where each row is a string. Input empty line to end input.  
Example, to input 2 x 2 grid:  
w e  
r t  
  
Use the input:  
we  
rt  
  
  
#### Requirements
1. Nltk.corpus.words() for list of english words
2. `words_dictionary.json`, also contained in the same folder
(Both lists are used to confirm english words)

Useful for scoring high in the facebook game word streak!
