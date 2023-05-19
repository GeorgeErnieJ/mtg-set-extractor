# mtg-set-extractor

This is a tool to extract the names of all cards belonging to a specified set from the scryfall bulk data oracle-cards.json file, which can be found on their website under bulk data. 

This program is a simple json filter that searches all cards to check if they match the set you've specified and outputs a .txt file containing all of the card names associated with that set.


USAGE

Make sure you have the oracle cards downloaded, and named "orace-cards.json". Put this in the same directory as the python file.
Edit the file and change the set name on line 46 to the set of your choice, default is 'mh2'. 

After that, click run and it'll filter the list and output your cards as a .txt.

Additional, this is going to be a fun project to work on updating for a while to get the hang of git, expect to see more features cropping up in the coming weeks etc. Might turn this into a full blown app with huge filter lists, who knows? 
