import pygame
import random
from network import Network

# Variables
undercover = "Undercover"
civil = "Civil"
mr_white = "M. White"
sep = ";"  # separator in the JSON file

# Lists
words = []
words_nb = None  # nb chosen by the player, in order they can't get twice the same couple of words.
players_draw = []
order = []

# Dictionaries
players_roles = {}
roles_repartition = {
3: 2 * [civil] + [undercover],
4: 3 * [civil] + [undercover],
5: 3 * [civil] + [undercover] + [mr_white],
6: 3 * [civil] + 2 * [undercover] + [mr_white]
}


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


# Pygame init
screen_w = 1200  # best & max: 1200
screen_h = 650  # best & max: 900

pygame.init()

screen = pygame.display.set_mode((screen_w, screen_h))

pygame.display.set_caption("Undercover")
# pygame.display.set_icon(pygame.image.load('icon.png'))

# clock = pygame.time.Clock()

# Buttons
btn_hovered_c = (255, 255, 255)
btn_inactive_c = (230, 230, 230)


class Button():
	def __init__(self, color, x, y, w, h, txt=""):
		self.color = color
		self.x = x
		self.y = y
		self.w = w
		self.h = h
		self.txt = txt

	def draw(self, window):
		"""Call this method to draw the button on the screen"""
		pygame.draw.rect(screen, self.color, (self.x, self.y, self.w, self.h), 0)
		if self.txt != '':
			font = pygame.font.SysFont('Charlemagne Std', 20)
			txt = font.render(self.txt, True, (0, 0, 0))
			screen.blit(txt,
						(self.x + (self.w // 2 - txt.get_width() // 2), self.y + (self.h // 2 - txt.get_height() // 2)))

	def click(self, pos):
		"""Pos is the mouse position or a tuple of (x, y) coordinates"""
		if pos[0] > self.x and pos[0] < (self.x + self.w):
			if pos[1] > self.y and pos[1] < (self.y + self.h):
				return True
		return False


def btn_x_center(w):
	screen_w / 2 - w / 2


# Background buttons
margin = 125
space = (screen_w - margin * 2 - 150 * 5) / 4
bg_btn_w = 150
red_button = Button(btn_inactive_c, margin, 15, bg_btn_w, 30, 'Red')
yellow_button = Button(btn_inactive_c, margin + bg_btn_w + space, 15, bg_btn_w, 30, 'Yellow')
deep_blue_button = Button(btn_inactive_c, margin + bg_btn_w * 2 + space * 2, 15, bg_btn_w, 30, 'Deep blue')
blue_button = Button(btn_inactive_c, margin + bg_btn_w * 3 + space * 3, 15, bg_btn_w, 30, 'Blue')
green_button = Button(btn_inactive_c, margin + bg_btn_w * 4 + space * 4, 15, bg_btn_w, 30, 'Green')
quit_button = Button(btn_inactive_c, screen_w - 160, screen_h - 45, 110, 30, 'Quitter')
back_button = Button(btn_inactive_c, screen_w / 2 - 150 / 2, screen_h - 45, 150, 30, 'Retour')
bg_buttons = [red_button, yellow_button, deep_blue_button, blue_button, green_button]

begin_button = Button(btn_inactive_c, screen_w / 2 - 150 / 2, 435, 150, 30, 'Commencer')
launch_button = Button(btn_inactive_c, screen_w / 2 - 150 - 100, 495, 150, 30, 'Lancer une partie')
join_button = Button(btn_inactive_c, screen_w / 2 + 200, 495, 150, 30, 'Rejoindre une partie')
ready_button = Button(btn_inactive_c, screen_w / 2 - 150 / 2, 300, 150, 30, 'Prets')
next_button = Button(btn_inactive_c, screen_w / 2 - 150 / 2 - 25, screen_h - 90, 200, 30, 'Jouer avec les prochains mots')
all_buttons = [red_button, yellow_button, deep_blue_button, blue_button, green_button, quit_button, back_button, launch_button, join_button, begin_button, ready_button, next_button]

# Backgrounds (I used images instead of the fill method even though it is just colors for the moment because I would like to replace them by images later
red_com = pygame.image.load('bg1.gif')
yellow_com = pygame.image.load('bg2.gif')
deep_blue = pygame.image.load('bg3.gif')
blue_com = pygame.image.load('bg4.gif')
green_com = pygame.image.load('bg5.gif')
background = deep_blue


# Function to change the background
def change_bg(button):
	global background
	if button == red_button:
		background = red_com
	elif button == yellow_button:
		background = yellow_com
	elif button == deep_blue_button:
		background = deep_blue
	elif button == blue_button:
		background = blue_com
	elif button == green_button:
		background = green_com


# Input box & text classes & functions
black = (0, 0, 0)
white = (255, 255, 255)
FONT = pygame.font.Font(None, 32)
txtbox_active_c = white
txtbox_inactive_c = (150, 150, 150)
input_content = None


# Input boxes
class InputBox:
	def __init__(self, x, y, w, h, txt=''):
		self.rect = pygame.Rect(x, y, w, h)
		self.txt_color = black
		self.color = txtbox_inactive_c
		self.txt = txt
		self.txt_surface = FONT.render(txt, True, self.txt_color)
		self.active = False

	def handle_event(self, event):
		global step, player_name, room_name, words_nb, join_room, input_content
		if event.type == pygame.MOUSEBUTTONDOWN:
			# If the user clicked on the input_box rect
			if self.rect.collidepoint(event.pos):
				#  Toggle the active variable
				self.active = not self.active  # donc not False = True ? Je peux peut-être juste remplacer
			else:
				self.active = False
			# Change the color of the input box
			self.color = txtbox_active_c if self.active else txtbox_inactive_c
		if event.type == pygame.KEYDOWN:
			if self.active:
				# if len(self.txt) >= 16:
				# 	display_txt_x_center(520, 30, "15 caractères maximum")
				# else:
				# 	rect_error = pygame.Rect(x, y, txt_w, h)
				# 	txt_surface_error = FONT.render(txt, True, white)
				# 	screen.blit(txt_surface, rect)
				if event.key == pygame.K_RETURN:
					input_content = self.txt
					step += 1
				elif event.key == pygame.K_BACKSPACE:
					self.txt = self.txt[:-1]
				else:
					self.txt += event.unicode
				# Re-render the txt
				self.txt_surface = FONT.render(self.txt, True, self.txt_color)

	def draw(self, screen):
		# Blit the rect
		pygame.draw.rect(screen, self.color, self.rect, 0)
		# Blit the txt
		screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))

	def return_input(self):
		return self.txt


def ask_sth_centered(y, txt=''):
	global player_name, step
	# txt
	txt_w, txt_h = FONT.size(txt)
	x = int((screen_w // 2) - (txt_w // 2))
	y = int((screen_h // 2) - (txt_h) - 10)
	rect = pygame.Rect(x, y, txt_w, txt_h)
	txt_surface = FONT.render(txt, True, white)
	screen.blit(txt_surface, rect)
	clock = pygame.time.Clock()
	# box
	box_x = screen_w // 2 - 150 // 2 - 25
	box_y = screen_h // 2 - 50
	box_w = 200
	box_h = 30
	input_box = InputBox(box_x, box_y + 60, box_w, box_h)
	done = False
	while not done:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done = True
				running = False
			pos = pygame.mouse.get_pos()
			if quit_button.click(pos):
				done = True
				pygame.quit()
			# if event.type == pygame.MOUSEMOTION:   # ne semble pas fonctionner...
			# 	for button in all_buttons:
			# 		if button.click(pos):
			# 			button.color = btn_hovered_c
			# 		else:
			# 			button.color = btn_inactive_c
			input_box.handle_event(event)
			if step == 2 or step == 4 or step == 6 or step == 8:  # if step % 2 == 0?
				done = True
		input_box.draw(screen)
		pygame.display.flip()
		clock.tick(30)


# Texts
def display_txt(x, y, w, h, txt):
	rect = pygame.Rect(x, y, w, h)
	txt_surface = FONT.render(txt, True, white)
	screen.blit(txt_surface, rect)


def display_txt_x_center(y, h, txt):
	txt_w, txt_h = FONT.size(txt)
	x = int((screen_w // 2) - (txt_w // 2))
	rect = pygame.Rect(x, y, txt_w, h)
	txt_surface = FONT.render(txt, True, white)
	screen.blit(txt_surface, rect)


def display_players():
	global players
	i = 0
	y = 180
	while i <= (len(players) - 1):
		display_txt(50, y, 185, 30, "{}".format(players[i]))
		i += 1
		y += 45


def roles_distribution(players_roles, players, player_name, words, words_nb):
	if players_roles[player_name] == civil:
		display_txt_x_center(230, 30, "{}, votre mot est {}.".format(player_name, words[words_nb - 1][0]))
	elif players_roles[player_name] == undercover:
		display_txt_x_center(230, 30, "{}, votre mot est {}.".format(player_name, words[words_nb - 1][1]))
	elif players_roles[player_name] == mr_white:
		display_txt_x_center(230, 30, "{}, vous êtes {}.".format(player_name, mr_white))
	else:
		print("Erreur 'roles_distribution'")

def display_role(role, player_name, words, words_nb):
	if role == civil:
		display_txt_x_center(230, 30, "{}, votre mot est {}.".format(player_name, words[words_nb - 1][0]))
	elif role == undercover:
		display_txt_x_center(230, 30, "{}, votre mot est {}.".format(player_name, words[words_nb - 1][1]))
	elif role == mr_white:
		display_txt_x_center(230, 30, "{}, vous êtes {}.".format(player_name, mr_white))
	else:
		print("Erreur 'roles_distribution'")


def display_list(lst, x, y):
	"""display a list at the 'indice+1. item' format"""
	i = 0
	display_txt(x, y, 185, 30, "Ordre de jeu :")
	y += 45
	while i <= (len(lst) - 1):
		display_txt(x, y, 185, 30, "{}. {}".format(i + 1, lst[i]))
		i += 1
		y += 45


step = 1
player_id = None
player_name = None
players = []
players.clear()



def draw_bg_btns():
	for btn in bg_buttons:
		btn.draw(screen)

launch_ready = False

def main():
	global step, player_id, input_content, player_name, players, words, words_nb, launch_ready, next_ready
	run = True
	clock = pygame.time.Clock()
	n = Network()
	player_id = n.get_id()
	print('You are player', player_id)
	player_name = input_content
	print("You are", player_name)


	while run:
		clock.tick(60)
		screen.blit(background, (0, 0))
		if step == 2:
			if player_id != 0:
				step = 5
			words = retrieve_words('undercover_words.txt')  # retrieve the words tupples and add them to the dictionary
			step += 1
		elif step == 3:
			if player_id == 0:
				display_txt_x_center(250, 30, "Bonjour {} !".format(player_name))
				ask_sth_centered(screen_h / 2 - 50, "Choisissez un nombre de couple de mots entre 1 et {}".format(len(words)))
			else:
				step = 5
		elif step == 4:
			words_nb = n.send(int(input_content))
			step += 1
		elif step == 5:
			draw_bg_btns()
			if player_id == 0:
				display_txt_x_center(105, 30, "Couple de mots : {}".format(words_nb))
			players = n.send(player_name)
			display_players()
			ready_button.draw(screen)
		elif step == 6:
			step += 1
		elif step == 7:
			draw_bg_btns()
			players = n.send(player_name)
			display_players()
			display_txt_x_center(200, 30, "En attente du lancement du jeu")
			launch_ready = n.send("launch")
			if launch_ready:
				pygame.time.delay(50)
				step += 1
		elif step == 8:
			role = n.send("game")
			order = n.send("order")
			words_nb = n.send("words_couple")
			pygame.time.delay(100)  # necessary or it seems that the server global launch_ready becomes False before some of the clients had retrieve the True value and get to this step
			launch_ready = n.send("launch_false")
			print("Test : launch_ready est pour le jour", player_id, " ", launch_ready)
			step += 1
		elif step == 9:
			draw_bg_btns()
			display_players()
			display_role(role, player_name, words, words_nb)
			display_list(order, screen_w / 2 - 150 / 2, 275)
			if player_id == 0:
				next_button.draw(screen)
			if player_id != 0:
				launch_ready = n.send("launch")
				if launch_ready:
					step = 8



		# ce qu'il faut que je vérifie tt le tps
		# players pour que ça s'update en tps réel


		for event in pygame.event.get():
			pos = pygame.mouse.get_pos()

			if event.type == pygame.QUIT:
				run = False
				pygame.quit()

			if event.type == pygame.MOUSEBUTTONDOWN:
				for button in bg_buttons:
					if button.click(pos):
						change_bg(button)
				if quit_button.click(pos):
					pygame.quit()
				if ready_button.click(pos):  # only player_id = 0 see this button and can interact with it
					launch_ready = n.send("launch")
					step = 8
				if next_button.click(pos):  # only player_id = 0 see this button and can interact with it
					print("next")
					words_nb = n.send("next")
					launch_ready = n.send("launch")
					step = 8

					"""
					game_program()
					# for testing purpose
					for i in players_roles:
						print(i)
						print(players_roles[i])
					print(show_list(order))
					# end testing
					step = 9
					"""





		pygame.display.update()

def beginning_screen():
	global step
	run = True
	clock = pygame.time.Clock()

	while run:
		clock.tick(60)
		screen.blit(background, (0, 0))
		ask_sth_centered(screen_h / 2 - 50, "Entrez votre nom")
		pygame.display.update()

		"""
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				run = False
		"""

		if step == 2:
			run = False

	main()

while True:
	beginning_screen()