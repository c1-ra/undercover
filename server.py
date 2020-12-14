import socket
from _thread import *
import pickle
import random

server = "xx.xx.xx.xx"
port = 5555

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

def roles_program(game_id):
	global roles_repartition
	roles = roles_repartition[len(games_players[game_id])]
	random.shuffle(roles)
	players_roles = dict(zip(games_players[game_id], roles))
	return players_roles


def order_program(game_id, players_roles):
	global roles_repartition
	player1 = first_player(players_roles)
	i_player1 = games_players[game_id].index(player1)
	order_ids = games_players[game_id][i_player1:] + games_players[game_id][:i_player1]
	return order_ids


def order_list_with_names(order_ids):
	global order_names, players_info
	# copy of order_ids to replace ids by names
	order_names = order_ids[:]
	for i in order_ids:
		order_names[i] = players_info[order_ids[i]][0]
	return order_names


# Variables
players_ids = []

current_player = 0

# players_info = {player_id: [0:player_name, 1.game_id, (2:launcher), 3:role]}
players_info = {}

# games_info = {game_id: [0.game_name, 1.words_nb, 2.players_roles, 3.order_names, 4.launch = False, 5.next = False]}
games_info = {}

games = []  # games[id] = room_name

games_players = {}  # {game_id : [list of players_ids in this game_id)]}

# Threads
def threaded_client(conn, player_id):
	global games, players_info, games, games_info, games_players

	room_name_create = None
	room_name_join = None

	words_nb = None

	players_names_to_display = []

	launch_prog = False

	conn.send(pickle.dumps(player_id))

	while True:
		try:
			data = str(pickle.loads(conn.recv(2048)))
			print(data)
			data_id = int(data[:2])
			print("data_id:", data_id)
			data_content = data[2:]
			print("data_content:", data_content)

			if not data:
				print("Disconnected")
				break
			else:
				if data_id == 0:
					print("data_id = ", data_id)
					players_info[player_id] = [data_content, None, None]
					conn.sendall(pickle.dumps(data_content))
				elif data_id == 1:
					print("data_id = ", data_id)
					for i in games_players[game_id]:
						if players_info[games_players[game_id][i]][0] not in players_names_to_display:
							players_names_to_display.append(players_info[games_players[game_id][i]][0])
						print("players names to display: ", players_names_to_display)
					conn.sendall(pickle.dumps(players_names_to_display))
				elif data_id == 2:
					print("data_id = ", data_id)
					players_info[player_id][1] = True
					conn.sendall(pickle.dumps(True))
				elif data_id == 3:
					print("data_id = ", data_id)
					players_info[player_id][1] = False
					conn.sendall(pickle.dumps(False))
				elif data_id == 4:
					print("data_id = ", data_id)
					conn.sendall(pickle.dumps(data_content))
					room_name_create = data_content
				elif data_id == 5:
					print("data_id = ", data_id)
					if data_content in games:
						conn.sendall(pickle.dumps(True))
						room_name_join = data_content
					else:
						conn.sendall(pickle.dumps(False))
				elif data_id == 6:
					print("data_id = ", data_id)
					print("Sending to player ", player_id, " words_nb = ", data_content)
					conn.sendall(pickle.dumps(int(data_content)))
					words_nb = int(data_content)
				elif data_id == 7:
					if games_info[game_id][4]:
						conn.sendall(pickle.dumps(True))
					else:
						conn.sendall(pickle.dumps(False))
				elif data_id == 8:
					games_info[game_id][4] = True
					launch_prog = True
					conn.sendall(pickle.dumps(True))
				elif data_id == 9:
					player_info = [games_info[game_id][2][player_id], games_info[game_id][1], games_info[game_id][3]]
					conn.sendall(pickle.dumps(player_info))
				elif data_id == 10:
					games_info[game_id][4] = False
					conn.sendall(pickle.dumps(False))
				elif data_id == 11:
					games_info[game_id][1] += 1
					conn.sendall(pickle.dumps(words_nb))

				# for debugging purposes:
				# print("Received from player ", player_id, ": ", data)
				# print("Sending to player ", player_id, ": ", reply)

		except:
			break

		if room_name_create != None:
			game_id = len(games)
			games.append(room_name_create)
			games_info[game_id] = [room_name_create, None, [], [], False, False]
			games_players[game_id] = [player_id]
			print("games_id: ", game_id)
			print ("games_info: ", games_info)
			print ("games players: ", games_players[game_id])
			room_name_create = None
		elif room_name_join != None:
			print("index: ", games.index(room_name_join))
			game_id = games.index(room_name_join)
			games_players[game_id].append(player_id)
			print ("games players: ", games_players[game_id])
			room_name_join = None
		elif words_nb != None:
			games_info[game_id][1] = words_nb
			words_nb = None
		elif launch_prog:
			players_roles = roles_program(game_id)
			games_info[game_id][2] = players_roles
			print("players_roles dans games_info", games_info[game_id][2])
			order_ids = order_program(game_id, players_roles)
			order_list_to_add = order_list_with_names(order_ids)
			print("order_lis to add: ", order_list_to_add)
			games_info[game_id][3] = order_list_to_add
			print("games_infos_players_order", games_info[game_id][3])
			launch_prog = False
		else:
			pass



	print("Lost connection", player_id)
	conn.close()


while True:
	conn, addr = s.accept()
	print("Connected to:", addr)

	start_new_thread(threaded_client, (conn, current_player))
	players_ids.append(current_player)
	current_player += 1
