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

# game
# Variables
undercover = "Undercover"
civil = "Civil"
mr_white = "M. White"
sep = ";"  # separator in the JSON file

# Dictionaries
players_roles = {}
roles_repartition = {
	3: 2 * [civil] + [undercover],
	4: 3 * [civil] + [undercover],
	5: 3 * [civil] + [undercover] + [mr_white],
	6: 3 * [civil] + 2 * [undercover] + [mr_white]
}
order = []


def retrieve_words(files_name):
	return [tuple(word.strip().split(sep)) for word in open(files_name, "r").readlines()]


def show_list(lst):
	"""display a list in 'indice+1. item' format"""
	for i, item in enumerate(lst):
		print("{}. {}".format(i + 1, item))


def first_player(players_roles):
	players = list(players_roles)
	while True:
		player1 = random.choice(players)
		if players_roles[player1] != mr_white:
			break
	return player1


# Program logic
def game_program():
	global roles, roles_repartition, players, players_roles, player1, order
	roles = roles_repartition[len(players)]
	random.shuffle(roles)
	players_roles = dict(zip(players, roles))
	player1 = first_player(players_roles)
	i_player1 = players.index(player1)
	order = players[i_player1:] + players[:i_player1]



players = []
players.clear()
current_player = 0
players_ids_names = {}
launch = False
words_nb = 0
next = False


def threaded_client(conn, player_id):
	global words_nb, players, launch, next, players_ids_names   # players ne semble pas nécessaire dans global
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
						reply = True
						game_program()
					elif launch == True:
						reply = True
					else:
						reply = False
				elif data == "launch_false":
					launch = False
					reply = False
				elif data == "game":
					reply = players_roles[player_name]
				elif data == "order":
					reply = order
				elif data == "words_couple":
					reply = words_nb
					print("words nb for player", player_id, "est egal a", words_nb)
				elif data == "next" and player_id == 0:
					words_nb += 1
					reply = words_nb
				else:
					if isinstance(data, str):
						if data not in players:
							player_name = data
							players.append(player_name)
							players_ids_names[player_id] = player_name
						reply = players
					elif isinstance(data, int) and player_id == 0:
						words_nb = data
						reply = words_nb

				print("Received: ", player_id, data)
				print("Sending : ", player_id, reply)

			conn.sendall(pickle.dumps(reply))

		except:
			break

	print("Lost connection", player_id)
	conn.close()


while True:
	conn, addr = s.accept()
	print("Connected to:", addr)

	start_new_thread(threaded_client, (conn, current_player))
	current_player += 1
