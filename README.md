# undercover
Undercover multiplayer game in Python

This video helped me a lot to have some basic knowledge of the use of socket and threadings:
https://www.youtube.com/watch?v=McoDjOCb2Zo

To test it, it is necessary to add server and port value in server.py (lines 6-7) and network.py (lines 7-8).

It is my first try at an online multiplayer game, and it is still a WIP.

Notes:
The players will have to use a vocal application to talk with each other, the game only distributes the roles, show to each player theirs, and show everybody the order in which they should play.
The players who create a room have to choose a number for the words with which they will play. It is to be sure that when they play another time they can pick from where they left and do not get the same words.

Edit 14/12: 
- I have added the possibility to create a room/game. It works with one room (players cannot join a room which does not exist, they have to type once again the room name if it is not found, and all the information (words_nb, players_roles) is stocked in a dictionary with the id of the game in order to separate the different games and their information), but I have not tested the creation of different rooms yet.
- I have automatically added numbers at the beginning of each information which is sent from clients to the server. Players won't be able to make the game bug by inputting key words that I was previously using to trigger some actions anymore. Since it is then sliced in data_id (int) and data_content (str), the condition is only on the int data_id, and it should be a little faster than when it was on a string.
    0: player name initialization
    1: send the client player_name, check if the player is not already in the list, return the players names in the room to display
    2: create a room
    3: join a room
    4: name of the room the player wants to create
    5: name of the room the player wants to join
    6: words couple to begin to play with (only asked to the launcher)
    7: check if the game_id launch is True or not
    8: the launcher launches the game: game_id launch becomes True
    9: game starts
    10: launch reset to False for all clients
    11: play with next words

Next steps:
- add a back button
- get rid of some variables not used
- not allow two same player names in the same game_id
