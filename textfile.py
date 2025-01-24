import pygame, sys
from pygame.locals import *

pygame.init()
pygame.key.set_repeat(500, 50)

clock = pygame.time.Clock()

screen = pygame.display.set_mode((1000, 500))
cursorx = 50
cursory = 50

lines = [""]
font = pygame.font.SysFont("Courier", 30)
line_num = 0
line_index = 0

while True:
    clock.tick(30)
    screen.fill((0,0,0))
    pygame.draw.rect(screen, (255,255,255), [cursorx, cursory, 18, 30], 2)
    
    for i in range(len(lines)):
        txt_surf = font.render(lines[i], True, (255,255,255))
        screen.blit(txt_surf, (50,50+i*50))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                if lines[line_num] == "":
                    if line_num != 0:
                        lines = lines[:line_num] + lines[line_num+1:]
                        line_num -= 1
                        cursory -= 50
                        cursorx = 50 + len(lines[line_num])*18
                        line_index = len(lines[line_num])
                    elif line_num == 0:
                        if cursorx < 50:
                            cursorx = 50
                        line_index = 0
                else:
                    lines[line_num] = lines[line_num][:line_index-1] + lines[line_num][line_index:] if line_index != 0 else lines[line_num]
                    if line_index == 0 and line_num!=0:
                        lines[line_num-1] = lines[line_num-1]+lines[line_num]
                        cursorx = 50 + len(lines[line_num-1])*18 - len(lines[line_num])*18
                        cursory -= 50
                        line_index = len(lines[line_num-1]) - len(lines[line_num])
                        lines = lines[:line_num] + lines[line_num+1:]
                        line_num -= 1
                    else:
                        cursorx -= 18
                        line_index -= 1
                        if cursorx < 50:
                            cursorx = 50
                            line_index = 0
            
            elif event.key == pygame.K_RETURN:
                cursorx = 50
                cursory += 50
                lines.insert(line_num+1, lines[line_num][line_index:])
                lines[line_num] = lines[line_num][:line_index]
                line_num += 1
                line_index = 0
            
            elif event.key == pygame.K_LEFT:
                cursorx -= 18
                line_index -= 1
                if cursorx < 50:
                    cursorx = 50
                    line_index = 0
            
            elif event.key == pygame.K_RIGHT:
                cursorx += 18
                line_index += 1
                if cursorx > 50+len(lines[line_num])*18:
                    cursorx = 50+len(lines[line_num])*18
                    line_index = len(lines[line_num])            

            elif event.key == pygame.K_UP:
                cursory -= 50
                line_num -= 1
                if cursory < 50:
                    cursory = 50
                    line_num = 0
                if len(lines[line_num]) < line_index:
                    cursorx = 50+len(lines[line_num])*18
                    line_index = len(lines[line_num])
            
            elif event.key == pygame.K_DOWN:
                cursory += 50
                line_num += 1
                if cursory > 50*len(lines):
                    cursory = 50*len(lines)
                    line_num = len(lines)-1
                if len(lines[line_num]) < line_index:
                    cursorx = 50+len(lines[line_num])*18
                    line_index = len(lines[line_num])
            
            elif event.key == pygame.K_TAB:
                lines[line_num] += "    "
                cursorx += 18*4
            
            elif event.key == pygame.K_ESCAPE:
                sys.exit(0)
            
            elif event.unicode:
                lines[line_num] = lines[line_num][:line_index] + event.unicode + lines[line_num][line_index:]
                line_index += 1
                cursorx += 18

    pygame.display.flip()
