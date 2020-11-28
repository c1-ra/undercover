# undercover
Undercover multiplayer game in Python

This video helped me a lot to have some basic knowledge of the use of socket and threadings:
https://www.youtube.com/watch?v=McoDjOCb2Zo

To test it, it is necessary to add server and port value in server.py (lines 6-7) and network.py (lines 7-8).

It is my first try at an online multiplayer game, and it is still a WIP.

Notes:
The first player to connect have to choose a number for the words with which they will play. It is to be sure that when they play another time they can pick from where they left and do not get the same words.

Next steps:
- add a back button
- get rid of some global variables
- not allow two same player_names
- not allow the words used to get game information back from the server to be used as player_names / find another way to get these information without sending strings -> maybe trigger it from the server.py file
- add the possibility to create or join a room
- add a "ready" button for everybody and wait for everybody to click on it before starting the game
