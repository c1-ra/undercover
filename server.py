import socket
from _thread import *
import pickle
import random

server = "xx.xx.xx.xx"
port = 0000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
	s.bind((server, port))
except socket.error as e:
	str(e)

s.listen(6)
print("Waiting for a connection, Server Started")

# Game
undercover = "Undercover"
civilian = "Civilian"
mr_white = "Mr. White"

roles_repartition = {
	# 2 for testing purposes only
	2: [civilian] + [undercover],
	3: 2 * [civilian] + [undercover],
	4: 3 * [civilian] + [undercover],
	5: 3 * [civilian] + [undercover] + [mr_white],
	6: 3 * [civilian] + 2 * [undercover] + [mr_white]
}


def first_player(players_roles):
	players = list(players_roles)
	while True:
		player1 = random.choice(players)
		if players_roles[player1] != mr_white:
			break
	return player1


def game_program():
	global roles, roles_repartition, players_ids, players_roles, order_ids
	roles = roles_repartition[len(players_ids)]
	random.shuffle(roles)
	players_roles = dict(zip(players_ids, roles))
	player1 = first_player(players_roles)
	i_player1 = players_ids.index(player1)
	order_ids = players_ids[i_player1:] + players_ids[:i_player1]


def order_list_with_names():
	global order_ids, order_names, players_info
	# copy of order_ids to replace ids by names
	order_names = order_ids[:]
	for i in order_ids:
		order_names[i] = players_info[order_ids[i]][0]


# Variables
players_roles = {}
order_ids = []
order_names = []

players_ids = []
players_names = []

words_nb = 0

current_player = 0

launch = False
next = False

# players_info = {player_id: [0:player_name, (1:launcher), 2: role]} (launcher will be useful when there are different rooms)
players_info = {}

# Threads
def threaded_client(conn, player_id):
	global players_ids, players_names, players_info, words_nb, launch, next, order_ids, order_names

	conn.send(pickle.dumps(player_id))
	reply = ""

	while True:
		try:
			data = pickle.loads(conn.recv(2048))

			if not data:
				print("Disconnected")
				break
			else:
				if data == "launch":
					if player_id == 0:
						launch = True
						game_program()
						order_list_with_names()
						reply = True
					elif launch == True:
						reply = True
					else:
						reply = False
				elif data == "launch_false":
					launch = False
					reply = False
				elif data == "game-start":
					player_info = [players_roles[player_id], words_nb, order_names]
					reply = player_info
				elif data == "next" and player_id == 0:
					words_nb += 1
					reply = words_nb
				else:
					if isinstance(data, str):
						if data not in players_names:
							player_name = data
							players_info[player_id] = [player_name, None, None]
							players_names.append(player_name)
						reply = players_names
					elif isinstance(data, int) and player_id == 0:
						words_nb = data
						reply = words_nb

				print("Received from player ", player_id, ": ", data)
				print("Sending to player ", player_id, ": ", reply)

			conn.sendall(pickle.dumps(reply))

		except:
			break

	print("Lost connection", player_id)
	conn.close()


while True:
	conn, addr = s.accept()
	print("Connected to:", addr)

	start_new_thread(threaded_client, (conn, current_player))
	players_ids.append(current_player)
	current_player += 1
