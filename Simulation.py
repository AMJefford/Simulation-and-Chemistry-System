import time as Time
import pygame
from pygame import *
import random
pygame.init()
import pygame
f=pygame.font.SysFont(None,60)

class Simulation:
    def RunSimulation():
        pygame.display.set_caption("A Level: Ideal Gas Simulation")
        BLACK = (0, 0, 0)
        RED = (255, 0, 0)
        WHITE = (255,255,255)
        GREEN = (0, 255, 0)
        RADIUS = 5
        BRIGHTRED= (200,0,0)
        BRIGHTGREEN = (0,200,0)

        def DecreaseSpeed(ChangeSpeed, ATOMS):
            for n in range(len(ATOMS)):
                if ATOMS[n][2] < 0:
                    ATOMS[n][2] = (ATOMS[n][2]) + ChangeSpeed
                else:
                    ATOMS[n][2] = (ATOMS[n][2]) - ChangeSpeed

                if ATOMS [n][3] < 0:
                    ATOMS [n][3] = (ATOMS[n][3]) + ChangeSpeed
                else:
                    ATOMS [n][3] = (ATOMS[n][3]) - ChangeSpeed
                if ATOMS[n][2] == -1:#to stop movement all together
                    ATOMS[n][2] = 0
                if ATOMS[n][3] == -1:
                    ATOMS[n][3] = 0
                
            Time.sleep(0.1)
            return ChangeSpeed
        
        def IncreaseSpeed(ChangeSpeed, ATOMS):
            
            
            for n in range (len(ATOMS)):
                if -5 < ATOMS[n][2] < 5 and -5 < ATOMS[n][3] < 5:
                    if ATOMS[n][2] < 0:
                        ATOMS[n][2] = (ATOMS[n][2]) - ChangeSpeed#increases at the same value for each, temp affects equally to atoms
                        
                    else:
                        ATOMS[n][2] = (ATOMS[n][2]) + ChangeSpeed
                        
                    if ATOMS [n][3] < 0:
                        ATOMS [n][3] = (ATOMS[n][3]) - ChangeSpeed
                        
                    else:
                        ATOMS [n][3] = (ATOMS[n][3]) + ChangeSpeed
                        
                    if ATOMS[n][3] == 0 or ATOMS[n][2] == 0:
                        ATOMS[n][3] = 1
                        ATOMS[n][2] = 1
                        
            Time.sleep(0.1)
            return ChangeSpeed


        def initATOMS(ATOMS, Size, IncreaseMoles):
            
            WIDTH = (list(Size))[0]
            HEIGHT = (list(Size))[1]
            if IncreaseMoles == True:
                x = 1
            else:
                x = 20
            for n in range(x):
                Props = [
                    random.randint(0, WIDTH),
                    random.randint(0, HEIGHT),
                    random.randint(-2, 2),#at standard conditions x
                    random.randint(-2, 2),]#different speeds depending on temp/press/vol y
                ATOMS.append(Props)
     
                
        def ButtonTIncrease(ChangeSpeed,ATOMS,x,y,w,h,action = None):
            Mouse = pygame.mouse.get_pos()
            Click = pygame.mouse.get_pressed()
            if x+w > Mouse[0] > x and y+h > Mouse[1] > y:
                if Click[0] == 1 and action == None:
                    ChangeSpeed = IncreaseSpeed(ChangeSpeed+1,ATOMS)  

        def ButtonTDecrease(ChangeSpeed,ATOMS,x,y,w,h,action = None):
            Mouse = pygame.mouse.get_pos()
            Click = pygame.mouse.get_pressed()
            if x+w > Mouse[0] > x and y+h > Mouse[1] > y:
                if Click[0] == 1 and action == None:
                    ChangeSpeed = DecreaseSpeed(ChangeSpeed+1,ATOMS)   


        def IncreaseN(Size, ATOMS,x,y,w,h,action = None):
            Mouse = pygame.mouse.get_pos()
            Click = pygame.mouse.get_pressed()
            if x+w > Mouse[0] > x and y+h > Mouse[1] > y:
                if Click[0] == 1 and action == None and len(ATOMS) < 200:
                    initATOMS(ATOMS, Size, True)     
                
        def DecreaseN(ATOMS,x,y,w,h,action = None):
            Mouse = pygame.mouse.get_pos()
            Click = pygame.mouse.get_pressed()
            if x+w > Mouse[0] > x and y+h > Mouse[1] > y:
                if Click[0] == 1 and action == None and len(ATOMS) > 0:
                    DecreaseMoles(ATOMS)

        def DecreaseMoles(ATOMS):
            del ATOMS[0]


        def DecreaseV(Size, x, y, w, h, action = None):
            Mouse = pygame.mouse.get_pos()
            Click = pygame.mouse.get_pressed()
            if x+w > Mouse[0] > x and y+h > Mouse[1] > y:
                if Click[0] == 1 and action == None:
                    WIDTH = (list(Size))[0]
                    HEIGHT = (list(Size))[1]
                    if HEIGHT - 5 > 60:
                        if (WIDTH/2) - 5 >120:
                            NEWWIDTH = WIDTH - 5
                            NEWHEIGHT = HEIGHT - 5
                            Size = ((NEWWIDTH, NEWHEIGHT))
            return Size

        def IncreaseV(Size, x, y, w, h, action = None):
            Mouse = pygame.mouse.get_pos()
            Click = pygame.mouse.get_pressed()
            if x+w > Mouse[0] > x and y+h > Mouse[1] > y:
                if Click[0] == 1 and action == None:
                    
                    WIDTH = (list(Size))[0]
                    HEIGHT = (list(Size))[1]
                    if HEIGHT + 5 < 600:
                        NEWWIDTH = WIDTH + 5
                        if (WIDTH/2) + 5 < 400:
                            NEWHEIGHT = HEIGHT + 5
                            Size = ((NEWWIDTH, NEWHEIGHT))
            return Size            

            

        def CheckCollisions(ATOMS, NoColl):
                for n in range(len(ATOMS)):
                    if ATOMS[n][2] != 0 or ATOMS[n][3] != 0:
                        Positionx = ATOMS[n][0]
                        Positiony = ATOMS[n][1]
                        for x in range(len(ATOMS)):
                            if x == n:
                                continue
                            elif (Positionx-(RADIUS/2)) <= ATOMS[x][0] <=(Positionx + (RADIUS/2)):
                                if (Positiony - (RADIUS/2)) <= ATOMS[x][1] <= (Positiony + (RADIUS/2)):
                                    
                                    NoColl += 1
                        
                return NoColl
                    
        def DrawScreen(ChangeSpeed, ATOMS, Size, Screen, NoColl, InitialTime):

            draw.rect(Screen, WHITE, (0, 0, 800, 600))
            Now = Time.time()
            if Now > InitialTime + 10 and Now < InitialTime + 11:
                    InitialTime = Time.time()
                    NoColl = 0
                    
           
            WIDTH = (list(Size))[0]
            HEIGHT = (list(Size))[1]
            SizeMovement = [HEIGHT, WIDTH/2]  
            Props = (100-RADIUS, 100-RADIUS, SizeMovement[0] +(2*RADIUS), (SizeMovement[1]) + (2*RADIUS))

            pygame.draw.rect(Screen, BLACK, Props, 1)
            
            NoColl = CheckCollisions(ATOMS, NoColl)
            
            Text = pygame.font.SysFont(None,30).render("Temperature: ",True, (60,60,60))
            Text2 = f.render("Ideal Gas Simulation", True,(0, 0, 0))
            Text3 = pygame.font.SysFont(None,30).render("Moles: ", True, (60,60,60))
            Text4 = pygame.font.SysFont(None,30).render("Volume: ", True, (60, 60, 60))
            Text5 = pygame.font.SysFont(None,30).render("Collisions /10s: ", True, (60, 60, 60))
            Text6 = pygame.font.SysFont(None,30).render(str(NoColl), True, (60, 60, 60))
            
            Screen.blit(Text,(100,525))
            Screen.blit(Text2,(100, 600 / 20))
            Screen.blit(Text3, (350, 525))
            Screen.blit(Text4, (550, 525))
            Screen.blit(Text5, (550, 40))
            Screen.blit(Text6, (720, 40))
            
            Mouse = pygame.mouse.get_pos()
            ButtonTIncrease(ChangeSpeed,ATOMS,250,520,75,30)
            ButtonTDecrease(ChangeSpeed, ATOMS, 250, 550, 75, 30)
            IncreaseN(Size, ATOMS,450, 520, 75, 30)
            DecreaseN(ATOMS, 450, 550, 75, 30)
            Size = IncreaseV(Size, 650, 520, 75, 30)
            Size = DecreaseV(Size, 650, 550, 75, 30)
            
            if 650 + 75 > Mouse[0] > 650 and 550 + 30 > Mouse[1] > 550:
                pygame.draw.rect(Screen, RED, (650, 550, 75, 25))
            else:
                pygame.draw.rect(Screen, BRIGHTRED, (650, 550, 75, 25))


            if 650 + 75 > Mouse[0] > 650 and 520 + 30 > Mouse[1] > 520:
                pygame.draw.rect(Screen, GREEN, (650, 520, 75, 25))
            else:
                pygame.draw.rect(Screen, BRIGHTGREEN, (650, 520, 75, 25))
                        

            if 450 + 75 > Mouse[0] > 450 and 550 + 30 > Mouse[1] > 550:
                pygame.draw.rect(Screen, RED, (450, 550, 75, 25))
                
            else:
                pygame.draw.rect(Screen, BRIGHTRED,(450, 550, 75, 25))


            if 450 + 75 > Mouse[0] > 450 and 520 + 30 > Mouse[1] > 520:
                pygame.draw.rect(Screen, GREEN, (450, 520, 75, 25))

            else:
                pygame.draw.rect(Screen, BRIGHTGREEN, (450, 520, 75, 25))
            
            if 250 + 75 > Mouse[0] > 250 and 550 + 30 > Mouse[1] >550:
                pygame.draw.rect(Screen, RED,(250, 550, 75, 25))
                
            else:
                pygame.draw.rect(Screen, BRIGHTRED, (250, 550, 75, 25))
            
            if 250+75> Mouse[0] >250 and 520+30>Mouse[1]>520:
                pygame.draw.rect(Screen, GREEN,(250,520,75,25))
                
            else:
                pygame.draw.rect(Screen, BRIGHTGREEN, (250,520,75,25))
            
            for i in range(len(ATOMS)):
                draw.circle(Screen, GREEN, (ATOMS[i][:2]),RADIUS)
            display.flip()
            
            return SizeMovement, Size, NoColl, InitialTime
        


        def MoveAtoms(ATOMS, Size):#800, 600
            WIDTH = (list(Size))[0]
            HEIGHT = (list(Size))[1]
                
            for i in range(len(ATOMS)):

                if ATOMS[i][0] > int(WIDTH) + 100:
                    ATOMS[i][0] = int(WIDTH) + 100
                    ATOMS[i][2] *= -1
                elif ATOMS[i][0] < 100:
                    ATOMS[i][0] = 100
                    ATOMS[i][2] *= -1
                else:
                    ATOMS[i][0] += ATOMS[i][2]

                if ATOMS[i][1] < 100:
                    ATOMS[i][1] = 100
                    ATOMS[i][3] *= -1
                elif ATOMS[i][1] > int(HEIGHT)+ 100:
                    ATOMS[i][1] = int(HEIGHT) + 100
                    ATOMS[i][3] *= -1
                else:
                    ATOMS[i][1] += ATOMS[i][3]


        def Main():
            ATOMS = []
            Size = WIDTH, HEIGHT = 800, 600
            Screen = display.set_mode(Size)
            ChangeSpeed = 0
            initATOMS(ATOMS, Size, False)
            NoColl = 0
            InitialTime = Time.time()
            
            while True:
                for evnt in event.get():
                    if evnt.type == QUIT:
                        pygame.quit()
                        return
                
                SizeMovement, Size, NoColl, InitialTime = DrawScreen(ChangeSpeed, ATOMS, Size, Screen, NoColl, InitialTime)
                MoveAtoms(ATOMS, SizeMovement)

        
        Main()
        

