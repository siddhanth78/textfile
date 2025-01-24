import pygame, sys
from pygame.locals import *
import os

pygame.init()

ascii_chars = [
    # Lowercase letters
    *range(97, 123),
    
    # Uppercase letters
    *range(65, 91),
    
    # Numbers
    *range(48, 58),
    
    # Common punctuation and symbols
    32, 33, 34, 35, 36, 37, 38, 39, 40, 
    41, 42, 43, 44, 45, 46, 47, 58, 59, 
    60, 61, 62, 63, 64, 91, 92, 93, 94, 
    95, 96, 123, 124, 125, 126
]

screen = pygame.display.set_mode((1000, 500))
cursorx = 50
cursory = 50

lines = [""]
font = pygame.font.SysFont("Courier", 30)
line_num = 0
line_index = 0

while True:
	screen.fill((0,0,0))	
	pygame.draw.rect(screen, (255,255,255), [cursorx, cursory, 18, 30], 2)
	for i in range(line_num+1):
		txt_surf = font.render(lines[i], True, (255,255,255))
		screen.blit(txt_surf, (50,50+i*50))
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit(0)

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_BACKSPACE:
				if lines[line_num] == "":
					if line_num != 0:
						lines = lines[:-1]
						line_num -= 1
						cursory -= 50
						cursorx = 50 + len(lines[line_num])*18
					elif line_num == 0:
						if cursorx < 50:
							cursorx = 50 
				else:
					lines[line_num] = lines[line_num][:-1]
					cursorx -= 18
			elif event.key == pygame.K_RETURN:
				cursorx = 50
				cursory += 50
				lines.append("")
				line_num += 1
			elif event.key == pygame.K_LEFT:
				cursorx -= 18
				if cursorx < 50:
					cursorx = 50
			elif event.key == pygame.K_RIGHT:
				cursorx += 18
				if cursorx > 50+len(lines[line_num])*18:
					cursorx = 50+len(lines[line_num])*18
			elif event.key == pygame.K_UP:
				cursory -= 50
				if cursory < 50:
					cursory = 50
			elif event.key == pygame.K_DOWN:
				cursory += 50
				if cursory > 50*len(lines):
					cursory = 50*len(lines)
			elif event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
				pass
			elif event.key == pygame.K_TAB:
				lines[line_num] += "    "
				cursorx += 18*4
			elif event.key == pygame.K_ESCAPE:
				sys.exit(0)
			else:
				if ord(event.unicode) in ascii_chars:
					lines[line_num] += event.unicode
					cursorx += 18	

	pygame.display.flip()			
