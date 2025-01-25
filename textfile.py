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
indent = 0
clip = ""
rel = 0
clips = []

while True:
    clock.tick(30)
    screen.fill((0,0,0))
    if rel == 0:
        pygame.draw.rect(screen, (255,255,255), [cursorx, cursory, 18, 30], 2)
    
    if rel < 0:
        pygame.draw.rect(screen, (128,128,128), [cursorx+18, cursory, 18*(-rel), 30], 2)
    elif rel > 0:
        pygame.draw.rect(screen, (128,128,128), [cursorx-18*rel, cursory, 18*rel, 30], 2)

    for i in range(len(lines)):
        txt_surf = font.render(lines[i], True, (255,255,255))
        screen.blit(txt_surf, (50,50+i*50))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                if indent > 0 and lines[line_num].strip() == "":
                    indent -= 1
                    cursorx -= 18*3
                    line_index -= 3
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
                if indent > 0:
                    lines[line_num] = "    "*indent + lines[line_num]
                    line_index = 4*indent
                    cursorx += 18*4*indent
                else:
                    line_index = 0
            
            elif event.key == pygame.K_LEFT:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                    cursorx -= 18
                    line_index -= 1
                    rel -= 1
                    if cursorx < 32:
                        cursorx = 32
                        line_index = -1
                        rel += 1
                else:
                    cursorx -= 18
                    line_index -= 1
                    if rel != 0:
                        rel -= 1
                        if cursorx < 32:
                            cursorx = 32
                            line_index = -1
                            rel += 1
                    else:
                        if cursorx < 50:
                            cursorx = 50
                            line_index = 0
            
            elif event.key == pygame.K_RIGHT:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                    cursorx += 18
                    line_index += 1
                    rel += 1
                    if cursorx > 50+len(lines[line_num])*18:
                        cursorx = 50+len(lines[line_num])*18
                        line_index = len(lines[line_num])
                        rel -= 1
                else:
                    cursorx += 18
                    line_index += 1
                    if rel != 0:
                        rel += 1
                    if cursorx > 50+len(lines[line_num])*18:
                        cursorx = 50+len(lines[line_num])*18
                        line_index = len(lines[line_num])
                        if rel != 0:
                            rel -= 1            

            elif rel != 0 and event.key == pygame.K_x:
                if rel < 0:
                    clip = lines[line_num][line_index+1:line_index-rel+1]
                    lines[line_num] = lines[line_num][:line_index+1] + lines[line_num][line_index-rel+1:]
                elif rel > 0:
                    clip = lines[line_num][line_index-rel:line_index]
                    lines[line_num] = lines[line_num][:line_index-rel] +lines[line_num][line_index:]
                rel = 0
                if cursorx < 50:
                    cursorx = 50
                    line_index = 0
                if cursorx > 50+len(lines[line_num])*18:
                    cursorx = 50+len(lines[line_num])*18
                    line_index = len(lines[line_num])
            
            elif rel != 0 and event.key == pygame.K_c:
                if rel < 0:
                    clip = lines[line_num][line_index+1:line_index-rel+1]
                elif rel > 0:
                    clip = lines[line_num][line_index-rel:line_index]
                rel = 0
                if cursorx < 50:
                    cursorx = 50
                    line_index = 0
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
                lines[line_num] = lines[line_num][:line_index] + "    " + lines[line_num][line_index:]
                if lines[line_num].strip() == "":
                    indent += 1
                line_index += 4
                cursorx += 18*4
            
            elif event.key == pygame.K_ESCAPE:
                sys.exit(0)
            
            elif (event.key == pygame.K_v) and (event.mod & pygame.KMOD_CTRL):            
                lines[line_num] = lines[line_num][:line_index] + clip + lines[line_num][line_index:]
                line_index += len(clip)
                cursorx += 18*len(clip)

            elif (event.key == pygame.K_a) and (event.mod & pygame.KMOD_CTRL):
                cursorx = 50
                lines.insert(line_num, "")
                line_index = 0

            elif (event.key == pygame.K_b) and (event.mod & pygame.KMOD_CTRL):
                cursorx = 50
                cursory += 50
                lines.insert(line_num+1, "") 
                line_num += 1
                line_index = 0

            elif (event.key == pygame.K_d) and (event.mod & pygame.KMOD_CTRL):
                if line_num != 0:
                    lines = lines[:line_num] + lines[line_num+1:]
                    if line_num == len(lines):
                        line_num -= 1
                        cursory -= 50
                        if cursory < 50:
                            cursory = 50
                else:
                    if len(lines) > 1:
                        lines = lines[1:]
                    else:
                        lines[line_num] = ""
                cursorx = 50 + len(lines[line_num])*18

            elif event.unicode:
                lines[line_num] = lines[line_num][:line_index] + event.unicode + lines[line_num][line_index:]
                line_index += 1
                cursorx += 18
        
    pygame.display.flip()
