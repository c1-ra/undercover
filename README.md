# undercover
Undercover multiplayer game in Python

This video helped a lot to have some basic knowledge of the use of socket and threadings:
https://www.youtube.com/watch?v=McoDjOCb2Zo

To test it, it is necessary to add server and port value in server.py (lines 6-7) and network.py (lines 7-8).

It is my first try at an online multiplayer game, and it is still a WIP.

Next steps:

- clean the files (repetitions, structure, maybe move the game logic in server.py fo another file)
- add a back button
- server.py : use a dictionary player_id:[player_name, role, words_nb] to get in one step all the information needed for the client to show the player role, instead of separate it in three different pieces od information
- not allow two same player names
- not allow the words used to get game information back from the server to be used as player_names / find another way to get these information without sending strings -> maybe trigger it from the server.py file
