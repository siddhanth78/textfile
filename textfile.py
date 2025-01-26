import pygame, sys
from pygame.locals import *

pygame.init()
pygame.key.set_repeat(250, 25)

clock = pygame.time.Clock()

screen = pygame.display.set_mode((1000, 500))
cursorx = 48
cursory = 25
font = pygame.font.SysFont("Courier", 20)
lines = [""]
line_num = 0
line_index = 0
indent = 0
clip = ""
rel = 0
clips = []

view_start = 0
view_end = 18

view_hs = 0
view_he = 75

while True:
    clock.tick(20)
    screen.fill((0,0,0))
    if rel == 0:
        pygame.draw.rect(screen, (255,255,255), [cursorx, cursory, 12, 20], 2)
    
    if rel < 0:
        pygame.draw.rect(screen, (128,128,128), [cursorx+12, cursory, 12*(-rel), 20], 2)
    elif rel > 0:
        pygame.draw.rect(screen, (128,128,128), [cursorx-12*rel, cursory, 12*rel, 20], 2)

    in_view = lines[view_start:view_end]

    for i in range(len(in_view)):
        txt_surf = font.render(in_view[i][view_hs:view_he], True, (255,255,255))
        screen.blit(txt_surf, (48,25+i*25))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                if indent > 0 and lines[line_num].strip() == "":
                    indent -= 1
                    cursorx -= 12*4
                    line_index -= 4
                elif lines[line_num] == "":
                    if line_num != 0:
                        lines = lines[:line_num] + lines[line_num+1:]
                        line_num -= 1
                        cursory -= 25
                        if line_num < view_start: 
                            view_start -= 1
                            view_end -= 1
                            cursory = 25
                        cursorx = 48 + len(lines[line_num])*12
                        line_index = len(lines[line_num])
                    elif line_num == 0:
                        if cursorx < 48:
                            cursorx = 48
                        line_index = 0
                    if cursory < 25:
                        cursory = 25
                else:
                    lines[line_num] = lines[line_num][:line_index-1] + lines[line_num][line_index:] if line_index != 0 else lines[line_num]
                    if line_index == 0 and line_num!=0:
                        lines[line_num-1] = lines[line_num-1]+lines[line_num]
                        cursorx = 48 + len(lines[line_num-1])*12 - len(lines[line_num])*12
                        cursory -= 25
                        line_index = len(lines[line_num-1]) - len(lines[line_num])
                        lines = lines[:line_num] + lines[line_num+1:]
                        line_num -= 1
                    else:
                        cursorx -= 12
                        line_index -= 1
                        if cursorx < 48:
                            cursorx = 48
                            line_index = 0
            
            elif event.key == pygame.K_RETURN:
                cursorx = 48
                cursory += 25
                lines.insert(line_num+1, lines[line_num][line_index:])
                lines[line_num] = lines[line_num][:line_index]
                line_num += 1
                view_hs = 0
                view_he = 75
                if indent > 0:
                    lines[line_num] = "    "*indent + lines[line_num]
                    line_index = 4*indent
                    cursorx += 12*4*indent
                else:
                    line_index = 0
                if line_num > view_end-1:
                    view_start += 1
                    view_end += 1            
                if cursory > 450:
                    cursory = 450

            elif event.key == pygame.K_LEFT:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                    cursorx -= 12
                    line_index -= 1
                    rel -= 1
                    if cursorx < 36:
                        cursorx = 36
                        line_index = -1
                        rel += 1
                else:
                    cursorx -= 12
                    line_index -= 1
                    if cursorx < 48:
                        cursorx = 48
                        view_hs -= 1
                        if view_hs < 0: view_hs = 0
                        view_he -= 1
                        if view_he < 75: view_he = 75

                    if rel != 0:
                        rel -= 1
                        if cursorx < 36:
                            cursorx = 36
                            line_index = -1
                            rel += 1
                    if line_index < 0: line_index = 0 
            
            elif event.key == pygame.K_RIGHT:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                    cursorx += 12
                    line_index += 1
                    rel += 1
                    if cursorx > 48+len(lines[line_num])*12:
                        cursorx = 48+len(lines[line_num])*12
                        line_index = len(lines[line_num])
                        rel -= 1
                else:
                    cursorx += 12
                    line_index += 1
                    if cursorx > 48+75*12:
                        cursorx = 48+75*12
                        view_hs += 1
                        if line_index > len(lines[line_num]):
                            line_index = len(lines[line_num])
                            view_hs -= 1
                        else:
                            view_he += 1
                        
                    if rel != 0:
                        rel += 1
                    if cursorx > 48+len(lines[line_num][view_hs:view_he])*12:
                        cursorx = 48+len(lines[line_num][view_hs:view_he])*12
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
                if cursorx < 48:
                    cursorx = 48
                    line_index = 0
                if cursorx > 48+len(lines[line_num])*12:
                    cursorx = 48+len(lines[line_num])*12
                    line_index = len(lines[line_num])
            
            elif rel != 0 and event.key == pygame.K_c:
                if rel < 0:
                    clip = lines[line_num][line_index+1:line_index-rel+1]
                elif rel > 0:
                    clip = lines[line_num][line_index-rel:line_index]
                rel = 0
                if cursorx < 48:
                    cursorx = 48
                    line_index = 0
                if cursorx > 48+len(lines[line_num])*12:
                    cursorx = 48+len(lines[line_num])*12
                    line_index = len(lines[line_num])

            elif event.key == pygame.K_UP:
                cursory -= 25
                line_num -= 1
                if line_num < 0:
                    line_num = 0
                if cursory < 25:
                    cursory = 25
                if line_num == view_start-1:
                    view_start -= 1
                    view_end -= 1
                if len(lines[line_num]) < line_index:
                    cursorx = 48+len(lines[line_num])*12
                    line_index = len(lines[line_num])
            
            elif event.key == pygame.K_DOWN:
                cursory += 25
                line_num += 1
                if line_num > len(lines)-1:
                    line_num = len(lines)-1
                    cursory -= 25
                if cursory > 450:
                    cursory = 450
                if line_num == view_end:
                    view_start += 1
                    view_end += 1
                if len(lines[line_num]) < line_index:
                    cursorx = 48+len(lines[line_num])*12
                    line_index = len(lines[line_num])
            
            elif event.key == pygame.K_TAB:
                lines[line_num] = lines[line_num][:line_index] + "    " + lines[line_num][line_index:]
                if lines[line_num].strip() == "":
                    indent += 1
                line_index += 4
                cursorx += 12*4
            
            elif event.key == pygame.K_ESCAPE:
                sys.exit(0)
            
            elif (event.key == pygame.K_v) and (event.mod & pygame.KMOD_CTRL):            
                lines[line_num] = lines[line_num][:line_index] + clip + lines[line_num][line_index:]
                line_index += len(clip)
                cursorx += 12*len(clip)

            elif (event.key == pygame.K_a) and (event.mod & pygame.KMOD_CTRL):
                cursorx = 48
                lines.insert(line_num, "")
                line_index = 0

            elif (event.key == pygame.K_b) and (event.mod & pygame.KMOD_CTRL):
                cursorx = 48
                cursory += 25
                if cursory > 450:
                    cursory = 450
                lines.insert(line_num+1, "") 
                line_num += 1
                if line_num == view_end:
                    view_start += 1
                    view_end += 1
                line_index = 0

            elif (event.key == pygame.K_d) and (event.mod & pygame.KMOD_CTRL):
                if line_num != 0:
                    lines = lines[:line_num] + lines[line_num+1:]
                    if line_num == len(lines):
                        line_num -= 1
                        cursory -= 25
                        if cursory < 25:
                            cursory = 25
                else:
                    if len(lines) > 1:
                        lines = lines[1:]
                    else:
                        lines[line_num] = ""
                cursorx = 48 + len(lines[line_num])*12

            elif event.unicode:
                lines[line_num] = lines[line_num][:line_index] + event.unicode + lines[line_num][line_index:]
                line_index += 1
                cursorx += 12
                if cursorx > 48+75*12:
                    cursorx = 48+75*12
                    view_hs += 1
                    view_he += 1
                        
    pygame.display.flip()

