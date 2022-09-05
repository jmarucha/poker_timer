#!/usr/bin/python3
import csv
import sys
import time
from datetime import datetime, timedelta
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame

def render_time(time):
	return "%2d:%02d" % (time.seconds//60, round(time.seconds % 60))

def render_frame(time, big_blind, next_big_blind, players, timer_done):
	small_blind = big_blind/2
	next_small_blind = next_big_blind/2
	screen.fill(BGCOLOR)

	if timer_done == True:
		time_surface = small_font.render("TIMER DONE!", True, STOPPEDCOLOR)
		blind_surface = small_font.render("Blinds: %d / %d" % (big_blind, small_blind), True, FONTCOLOR)
		player_surface = very_small_font.render("Player Count: %d" % (players), True, FONTCOLOR)
		stack_surface = very_small_font.render("Average Stack: %d" % (total_chips/players), True, FONTCOLOR)
		screen.blit(time_surface,(60,200))
		screen.blit(blind_surface,(60,450))
		screen.blit(player_surface,(60,60))
		screen.blit(stack_surface,(60,100))
		
	else:
		time_surface = big_font.render(render_time(time), True, STOPPEDCOLOR if paused else FONTCOLOR)
		blind_surface = small_font.render("Blinds: %d / %d" % (big_blind, small_blind), True, FONTCOLOR)
		player_surface = very_small_font.render("Player Count: %d" % (players), True, FONTCOLOR)
		stack_surface = very_small_font.render("Average Stack: %d" % (total_chips/players), True, FONTCOLOR)
		next_blind_surface = very_small_font.render("Next Blinds: %d / %d" % (next_big_blind, next_small_blind), True, FONTCOLOR)
		screen.blit(time_surface,(60,150))
		screen.blit(blind_surface,(60,450))
		screen.blit(player_surface,(60,60))
		screen.blit(stack_surface,(60,100))
		screen.blit(next_blind_surface,(60,700))


def pause():
	global paused, time, start
	if not paused:
		# start pause
		paused = True
	else:
		# stop pause
		paused = False
		paused_for_time = datetime.now() - time_now
		start = start + paused_for_time

def timer_done(sound = True):
	global alert_sound, start, blind_level, next_blind_level
	if sound:
		alert_sound.play()
	start = datetime.now()
	blind_level = blind_level + 1
	next_blind_level = next_blind_level + 1


players = int(input('How Many Players? '))
starting_stack = int(input("How many chips in each player's starting stack? "))
blind_duration = int(input('How many minutes will each rounds be? '))
blind_list = input("List Big Blinds in order with a space between like '20 40 60 ...' ")
blind_level = 0
next_blind_level = 1
total_chips = (players * starting_stack)
blinds = (blind_list.split(" "))

start = datetime.now()
paused = False
INTERVAL =  timedelta(minutes = blind_duration)
BGCOLOR = (32,32,32)
FONTCOLOR = (240, 240, 240)
STOPPEDCOLOR = (240, 30, 30)

pygame.display.init()
pygame.display.set_caption("Poker Timer")
screen = pygame.display.set_mode((1024, 768))

pygame.mixer.init()
alert_sound = pygame.mixer.Sound(file = "tiauo.ogg")

pygame.font.init()
big_font = pygame.font.SysFont('DejaVu Sans', 240)
small_font = pygame.font.SysFont('DejaVu Sans', 120)
very_small_font = pygame.font.SysFont('DejaVu Sans', 30)

while 1:
	if not paused:
		time_now = datetime.now()

	if (INTERVAL < time_now - start):
		timer_done()

	try:
		render_frame(INTERVAL - (time_now - start), int(blinds[(blind_level)]), int(blinds[(next_blind_level)]), players, False)	

	except IndexError:
		render_frame(0, int(blinds[(blind_level)]), 0, players, True)

	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_RETURN:
				timer_done(sound = False)
			elif event.key == pygame.K_SPACE:
				pause()
			elif event.key == pygame.K_ESCAPE:
				sys.exit()
			else:
				# change number of players
				if event.key == pygame.K_UP:
					players = players + 1
				elif event.key == pygame.K_DOWN:
					if players > 1:
						players = players - 1
				else:
					new_players = event.key - ord('0')
	
		if event.type == pygame.QUIT:
			sys.exit()
	pygame.display.flip()
	time.sleep(0.2)
