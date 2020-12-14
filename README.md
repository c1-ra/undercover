# undercover
Undercover multiplayer game in Python

This video helped me a lot to have some basic knowledge of the use of socket and threadings:
https://www.youtube.com/watch?v=McoDjOCb2Zo

To test it, it is necessary to add server and port value in server.py (lines 6-7) and network.py (lines 7-8).

It is my first try at an online multiplayer game, and it is still a WIP.

Notes:
The players will have to use a vocal application to talk with each other, the game only distributes the roles, show to each player theirs, and show everybody the order in which they should play.
The players who create a room have to choose a number for the words with which they will play. It is to be sure that when they play another time they can pick from where they left and do not get the same words.

Edit 12/14: I have added the possibility to create a room. It works with one room (players cannot join a room which does not exist, they have to type once again the room name if it is not found, and all the information (words_nb, players_roles) is stocked in a dictionary with the id of the game in order to separate the different games and their information), but I have not tested the creation of different rooms yet. 

Next steps:
- test if it works with different rooms
- add a back button
- get rid of some variables not used
- not allow two same player names (in the same game_id only?)
