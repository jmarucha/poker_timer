#!/usr/bin/python3
import pygame
import csv
import sys
from datetime import datetime, timedelta

INTERVAL =  timedelta(minutes = 20)
BGCOLOR = (32,32,32)
FONTCOLOR = (240, 240, 240)
STOPPEDCOLOR = (240, 30, 30)


def render_time(time):
	return "%02d:%02d" % (time.seconds//60, round(time.seconds % 60))

def render_frame(time, small_blind, players, timer_done = False):
	big_blind = 2*small_blind
	screen.fill(BGCOLOR)

	if timer_done:
		time_surface = small_font.render("TIMER DONE!", True, STOPPEDCOLOR)
	else:
		time_surface = big_font.render(render_time(time), True, STOPPEDCOLOR if paused else FONTCOLOR)
	blind_surface = small_font.render("%d / %d" % (big_blind, small_blind), True, FONTCOLOR)
	player_surface = very_small_font.render("%d players tournament:" % (players), True, FONTCOLOR)
	screen.blit(time_surface,(60,150))
	screen.blit(blind_surface,(60,450))
	screen.blit(player_surface,(60,60))

def pause():
	global paused, time, start
	if not paused:
		# start pause
		paused = True
	else:
		#stop pause
		paused = False
		paused_for_time = datetime.now() - time
		start = start + paused_for_time

def timer_done(sound = True):
	global alert_sound, start, blind_level
	if sound:
		alert_sound.play()
	start = datetime.now()
	blind_level = blind_level + 1


blinds = {}
with open('blinds.csv', 'r') as csvfile:
	blinds_file = csv.reader(csvfile, delimiter=',', quotechar='|')
	for row in blinds_file:
		row = [int(i) for i in row if i]
		player_count = row[0]
		blinds_list = row[1:]
		blinds[player_count] = blinds_list


pygame.mixer.init()
alert_sound = pygame.mixer.Sound(file = "tiauo.ogg")

screen = pygame.display.set_mode((1024, 768))
# infoObject = pygame.display.Info()
# screen =  pygame.display.set_mode((infoObject.current_w, infoObject.current_h))

pygame.font.init()
big_font = pygame.font.SysFont('DejaVu Sans', 240)
small_font = pygame.font.SysFont('DejaVu Sans', 120)
very_small_font = pygame.font.SysFont('DejaVu Sans', 30)
start = datetime.now()

blind_level = 0
players = 4

paused = False

while 1:
	if not paused:
		time = datetime.now()

	if (INTERVAL < time - start):
		timer_done()

	try:
		render_frame(INTERVAL - (time - start), blinds[players][blind_level], players)
	except IndexError:
		render_frame(0, blinds[players][-1], players, timer_done = True)



	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_RETURN:
				timer_done()
			elif event.key == pygame.K_SPACE:
				pause()
			elif event.key == pygame.K_ESCAPE:
				sys.exit()
			else:
				# change number of players
				if event.key == pygame.K_UP:
					new_players = players + 1
				elif event.key == pygame.K_DOWN:
					new_players = players - 1
				else:
					new_players = event.key - ord('0')

				if new_players in blinds.keys():
					players = new_players
					print(players)

		if event.type == pygame.QUIT:
			sys.exit()
	pygame.display.flip()
