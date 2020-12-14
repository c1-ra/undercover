import pygame
from network import Network

# Variables
undercover = "Undercover"
civilian = "Civilian"
mr_white = "Mr. White"
sep = ";"  # separator in the txt file


def retrieve_words(files_name):
	return [tuple(word.strip().split(sep)) for word in open(files_name, "r").readlines()]


# Pygame
screen_w = 1200  # img size: 1200
screen_h = 650  # img size: 900

pygame.init()

screen = pygame.display.set_mode((screen_w, screen_h))

pygame.display.set_caption("Undercover")
# pygame.display.set_icon(pygame.image.load('icon.png'))


# Buttons
class Button:
	def __init__(self, color, x, y, w, h, txt=""):
		self.color = color
		self.x = x
		self.y = y
		self.w = w
		self.h = h
		self.txt = txt

	def draw(self, screen):
		"""Call this method to draw the button on the screen"""
		pygame.draw.rect(screen, self.color, (self.x, self.y, self.w, self.h), 0)
		if self.txt != '':
			font = pygame.font.SysFont('Charlemagne Std', 20)
			txt = font.render(self.txt, True, (0, 0, 0))
			screen.blit(txt, (self.x + (self.w // 2 - txt.get_width() // 2), self.y + (self.h // 2 - txt.get_height() // 2)))

	def click(self, pos):
		"""Pos is the mouse position or a tuple of (x, y) coordinates"""
		if pos[0] > self.x and pos[0] < (self.x + self.w):
			if pos[1] > self.y and pos[1] < (self.y + self.h):
				return True
		return False


btn_hovered_c = (255, 255, 255)
btn_inactive_c = (210, 210, 210)


# Buttons creation
margin = 125
space = (screen_w - margin * 2 - 150 * 5) / 4
bg_btn_w = 150
btn_h = 30
red_btn = Button(btn_inactive_c, margin, 15, bg_btn_w, btn_h, 'Rouge')
yellow_btn = Button(btn_inactive_c, margin + bg_btn_w + space, 15, bg_btn_w, btn_h, 'Jaune')
deep_blue_btn = Button(btn_inactive_c, margin + bg_btn_w * 2 + space * 2, 15, bg_btn_w, btn_h, 'Bleu foncé')
blue_btn = Button(btn_inactive_c, margin + bg_btn_w * 3 + space * 3, 15, bg_btn_w, btn_h, 'Bleu')
green_btn = Button(btn_inactive_c, margin + bg_btn_w * 4 + space * 4, 15, bg_btn_w, btn_h, 'Vert')
bg_btns = [red_btn, yellow_btn, deep_blue_btn, blue_btn, green_btn]

create_room_btn = Button(btn_inactive_c, screen_w / 2 - bg_btn_w - 100, screen_h // 2 - btn_h, bg_btn_w, btn_h, 'Lancer une partie')
join_room_btn = Button(btn_inactive_c, screen_w / 2 + 100, screen_h // 2 - btn_h, bg_btn_w, btn_h, 'Rejoindre une partie')

begin_btn = Button(btn_inactive_c, screen_w / 2 - 150 / 2, 435, 150, 30, 'Commencer')
ready_btn = Button(btn_inactive_c, screen_w / 2 - 150 / 2, 300, 150, 30, 'Prêts')
next_btn = Button(btn_inactive_c, screen_w / 2 - 150 / 2 - 25, screen_h - 90, 200, 30, 'Jouer avec les prochains mots')

all_btns = [red_btn, yellow_btn, deep_blue_btn, blue_btn, green_btn, create_room_btn, join_room_btn, begin_btn, ready_btn, next_btn]

# Backgrounds
red_com = pygame.image.load('bg1.gif')
yellow_com = pygame.image.load('bg2.gif')
deep_blue = pygame.image.load('bg3.gif')
blue_com = pygame.image.load('bg4.gif')
green_com = pygame.image.load('bg5.gif')
background = deep_blue


# Function to change the background
def change_bg(btn):
	global background
	if btn == red_btn:
		background = red_com
	elif btn == yellow_btn:
		background = yellow_com
	elif btn == deep_blue_btn:
		background = deep_blue
	elif btn == blue_btn:
		background = blue_com
	elif btn == green_btn:
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
		global step, input_content
		if event.type == pygame.MOUSEBUTTONDOWN:
			# If the user clicked on the input_box rect
			if self.rect.collidepoint(event.pos):
				#  Toggle the active variable
				self.active = not self.active
			else:
				self.active = False
			# Change the color of the input box
			self.color = txtbox_active_c if self.active else txtbox_inactive_c
		if event.type == pygame.KEYDOWN:
			if self.active:
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


def ask_sth_centered(txt=''):
	global player_name, step
	# txt
	txt_w, txt_h = FONT.size(txt)
	x = int((screen_w // 2) - (txt_w // 2))
	y = int((screen_h // 2) - (txt_h - 10))
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


def display_players(players_names):
	i = 0
	y = 180
	while i <= (len(players_names) - 1):
		display_txt(50, y, 185, 30, "{}".format(players_names[i]))
		i += 1
		y += 45

def draw_bg_btns():
	for btn in bg_btns:
		btn.draw(screen)


def display_role(role, player_name, words, words_nb):
	if role == civilian:
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

launch_ready = False

def main():
	global step, input_content, words, launch_ready
	run = True
	clock = pygame.time.Clock()
	n = Network()
	player_id = n.get_id()
	print('You are player', player_id)
	player_name = n.send("0 "+input_content)
	print("You are", player_name)
	player_launcher = None
	join_room_existing = True
	players_names = []
	words_nb = 0


	while run:
		clock.tick(60)
		screen.blit(background, (0, 0))
		if step == 2:  # retrieve words
			print("2, c'est la step", step)
			words = retrieve_words('undercover_words.txt')
			step += 1
		elif step == 3:  # choose to create a room (player_launcher) or join one
			print("3, c'est la step", step)
			display_txt_x_center(250, 30, "Bonjour {} !".format(player_name))
			create_room_btn.draw(screen)
			join_room_btn.draw(screen)
		elif step == 4:  # for tests purposes
			print("4, c'est la step", step)
			print("player launcher:", player_launcher)
			step += 1
		elif step == 5:
			print("5, c'est la step", step)
			if player_launcher:
				ask_sth_centered("Entrez le nom que vous voulez donner à la partie :")
			else:
				ask_sth_centered("Entrez le nom de la partie que vous voulez rejoindre :")
				print("join room existing? ", join_room_existing)
				if not join_room_existing:
					display_txt_x_center(155, 30, "Le nom de partie que vous avez choisi n'existe pas.")
		elif step == 6:  # send the room_name (create the info for launcher, checks if it exists for !launcher)
			print("6, c'est la step", step)
			if player_launcher:
				room_name = n.send("4 "+input_content)
				step += 1
			else:
				room_name = input_content
				join_room_existing = n.send("5 " + input_content)
				print("room existing? ", join_room_existing)
				if join_room_existing:
					step += 5
				else:
					step -= 1
		elif step == 7:  # for player_launcher only : choose the couple of words to begin from
			print("c'est la step", step)
			ask_sth_centered("Choisissez un nombre de couple de mots entre 1 et {}".format(len(words)))
		elif step == 8:  # for player_launcher only: send the words couple number
			print("c'est la step", step)
			words_nb = n.send("6 "+input_content)
			step += 1
		elif step == 9:  # for player_launcher only
			print("c'est la step", step)
			draw_bg_btns()
			display_txt_x_center(105, 30, "Couple de mots : {}".format(words_nb))
			display_txt_x_center(155, 30, "Nom de la partie : {}".format(room_name))
			ready_btn.draw(screen)
			players_names = n.send("1 " + player_name)
			if isinstance(players_names, list):
				display_players(players_names)
		elif step == 10:  # not used for the moment
			pass
		elif step == 11: # for !player_launcher only
			print("c'est la step", step)
			draw_bg_btns()
			display_txt_x_center(200, 30, "En attente du lancement du jeu")
			players_names = n.send("1 " + player_name)
			if isinstance(players_names, list):
				display_players(players_names)
			launch_ready = n.send("7 ")
			if launch_ready:
				step += 1
		elif step == 12:  # for everybody, launcher or not: get the player role and game order, reset launch_ready to False
			player_info = n.send("9 ")
			pygame.time.delay(100)  # necessary or it seems that the server global launch_ready becomes False before some of the clients have retrieved the True value and got to this step
			launch_ready = n.send("10")
			print("Test : launch_ready est pour le joueur", player_id, " ", launch_ready)
			step += 1
		elif step == 13:  # display the roles and play order, player_launcher has a next_button
			draw_bg_btns()
			display_players(players_names)
			display_role(player_info[0], player_name, words, player_info[1])
			display_list(player_info[2], screen_w / 2 - 150 / 2, 275)
			if player_launcher:
				next_btn.draw(screen)
			else:
				launch_ready = n.send("7 ")
				if launch_ready:
					step = 12

		for event in pygame.event.get():

			if event.type == pygame.QUIT:
				run = False
				pygame.quit()

			pos = pygame.mouse.get_pos()
			if event.type == pygame.MOUSEBUTTONDOWN:
				for btn in bg_btns:
					if btn.click(pos):
						change_bg(btn)
				if create_room_btn.click(pos):
					player_launcher = n.send("2 ")
					step += 1
				if join_room_btn.click(pos):
					player_launcher = n.send("3 ")
					step += 1
				if ready_btn.click(pos):  # only player_id = 0 see this button and can interact with it
					launch_ready = n.send("8 ")
					step = 12
				if next_btn.click(pos):  # only player_id = 0 see this button and can interact with it
					print("next")
					words_nb = n.send("11")
					launch_ready = n.send("8 ")
					step = 12
			if event.type == pygame.MOUSEMOTION:
				for btn in all_btns:
					if btn.click(pos):
						btn.color = btn_hovered_c
					else:
						btn.color = btn_inactive_c

		pygame.display.update()


def beginning_screen():
	global step
	run = True
	clock = pygame.time.Clock()

	while run:
		clock.tick(60)
		screen.blit(background, (0, 0))
		ask_sth_centered("Entrez votre nom")
		pygame.display.update()

		if step == 2:
			run = False

	main()

while True:
	beginning_screen()
