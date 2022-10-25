import os
import random
import pygame
import time
import threading
import re
import csv
import pandas

#Player Class#####################################
class Player(object):
    def __init__(self):
        self.rect = pygame.Rect(30,30,60,60)

    def move(self,dx,dy):
        if dx != 0:
            self.move_single_axis(dx,0)
        if dy != 0:
            self.move_single_axis(0,dy)

    def move_single_axis(self,dx,dy):

        self.rect.x += dx
        self.rect.y += dy

        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if dx > 0:
                    self.rect.right = wall.rect.left
                if dx < 0:
                    self.rect.left = wall.rect.right
                if dy > 0:
                    self.rect.bottom = wall.rect.top
                if dy < 0:
                    self.rect.top = wall.rect.bottom

#WALL CLASS#########################################

class Wall(object):
    def __init__(self, wx, wy):
        walls.append(self)
        self.rect = pygame.Rect(wx,wy,30,30)

    def reset_wall(self):
        self.active = False

#ENEMY CLASS########################################

class Enemy(object):
    def __init__(self, ex, ey):
        enemies.append(self)
        self.rect = pygame.Rect(ex,ey,30,30)
    def reset_enemy(self):
        self.active = False

#BUFF CLASS#########################################

class Buff(object):
    def __init__(self, bx, by):
        buffs.append(self)
        self.rect = pygame.Rect(bx,by,30,30)
    def reset_enemy(self):
        self.active = False

#BUTTON CLASS#######################################

class Button:
    def __init__(self,image,buttonx,buttony,event):
        self.image = image
        self.buttonx = buttonx
        self.buttony = buttony
        self.event = event

        self.rect = self.image.get_rect()

    #DRAWING THE BUTTON#    
    def draw(self):
        self.rect.center = (self.buttonx,self.buttony)
        screen.blit(self.image,self.rect)
    #WHEN CLICKING A BUTTON#
    def Click(self):
        global gamestate
        global fadeav
        global fact
        global start
        global sortav
        #IF THE EVENT IS X DO y
        if self.event == "showSettingsScreen" and gamestate == "MainMenu":
            fadeIn(1440, 750)
            fadeav = 0
            gamestate = "Settings"

        if self.event == "showHighScore" and gamestate == "MainMenu":
            scores = pandas.read_csv("score.csv")
            sorted_scores = scores.sort_values(by=["Time"], ascending = True)
            sorted_scores.to_csv('sortedscores.csv', index=False)
            fadeIn(1440, 750)
            fadeav = 0
            gamestate = "HighScore"
            

        if self.event == "showMainMenu" and gamestate == "Settings":
            fadeIn(1440, 750)
            fadeav = 0
            gamestate = "MainMenu"

        if self.event == "goHomeFromHS" and gamestate == "HighScore":            
            fadeIn(1440, 750)
            fadeav = 0
            gamestate = "MainMenu"


        if self.event == "startGame" and gamestate == "MainMenu":
            start = time.time()
            fadeIn(1440, 750)
            fadeav = 0
            fact = random.choice(facts)
            gamestate = "Facts"

        if self.event == "ExitGame" and (gamestate == "MainMenu" or gamestate == "GameOver" or gamestate == "GameWon2"):
            fadeIn(1440, 750)
            pygame.quit()

        if fadeav == 0:
            fadeOut(1440,750)
            fadeav = 1

            
#FOR SUBMITTING NAME AT THE END OF THE GAME: INPUT BOX

class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x,y,w,h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, BLACK)
        self.active = False
    #WHAT THE BOX CAN DO:
    def handle_event(self, event):
        global text_av
        global gamestate
        if gamestate == "GameWon" and text_av == 0:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.active = not self.active
                    self.color = COLOR_ACTIVE
                
                else:
                    self.active = False
                    self.color = COLOR_INACTIVE

            if event.type == pygame.KEYDOWN:
                if self.active:
                    if event.key == pygame.K_RETURN:
                        #APPENDING NAME TO CSV FILE
                        with open('score.csv', mode='a', newline = "") as score:
                            score = csv.writer(score, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

                            score.writerow([self.text, gametime])
                        self.text = ''
                        text_av = 1
                        gamestate = "GameWon2"
                    elif event.key == pygame.K_BACKSPACE:
                        self.text = self.text[:-1]
                    else:
                        if len(self.text) < 10:
                            self.text += event.unicode
                    self.txt_surface = FONT.render(self.text, True, BLACK)

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(screen, self.color, self.rect, 3)

#USED TO REDRAW WINDOW FOR FADE IN AND FADE OUT EFFECTS:

def redrawWindow():
    if gamestate == "MainMenu":
        screen.blit(MainMenu_image, (0,0))
        settingsButton.draw()
        exitButton.draw()
        playButton.draw()
        highScoreButton.draw()

    if gamestate == "Settings":
        screen.blit(SettingsScreen_image, (0,0))
        settingsHomeButton.draw()

    if gamestate == "Game":
        screen.blit(background_image,(0,0)) 

    
        for wall in walls:
            pygame.draw.rect(screen,wall_colour,wall.rect)

        for enemy in enemies:
            screen.blit(eImage, enemy.rect)

        for buff in buffs:
            screen.blit(pillImage, buff.rect)

        pygame.draw.rect(screen,(255,0,0),end_rect)
        screen.blit(playerImage, player.rect)
        screen.blit(buffcd, (40,40))
        screen.blit(dashp, (1250,40))

    if gamestate == "Loading":
        screen.blit(background_image,(0,0)) 

    
        for wall in walls:
            pygame.draw.rect(screen,wall_colour,wall.rect)

        for enemy in enemies:
            screen.blit(eImage, enemy.rect)

        for buff in buffs:
            screen.blit(pillImage, buff.rect)

        pygame.draw.rect(screen,(255,0,0),end_rect)
        screen.blit(playerImage, player.rect)
        screen.blit(buffcd, (40,40))
        screen.blit(dashp, (1250,40))

    if gamestate == "Loading2":
        screen.blit(gameover_image, (0,0))
        GOEbutton.draw()

    if gamestate == "GameOver":
        screen.blit(gameover_image, (0,0))
        GOEbutton.draw()

    if gamestate == "Facts":
        screen.blit(fact, (0,0))

    if gamestate == "Loading5":
        screen.blit(fact, (0,0))

    if gamestate == "Loading3":
        screen.blit(background_image,(0,0)) 

    
        for wall in walls:
            pygame.draw.rect(screen,wall_colour,wall.rect)

        for enemy in enemies:
            screen.blit(eImage, enemy.rect)

        for buff in buffs:
            screen.blit(pillImage, buff.rect)

        pygame.draw.rect(screen,(255,0,0),end_rect)
        screen.blit(playerImage, player.rect)
        screen.blit(buffcd, (40,40))
        screen.blit(dashp, (1250,40))

    if gamestate == "Loading4":
        screen.blit(background_image,(0,0)) 

    
        for wall in walls:
            pygame.draw.rect(screen,wall_colour,wall.rect)

        for enemy in enemies:
            screen.blit(eImage, enemy.rect)

        for buff in buffs:
            screen.blit(pillImage, buff.rect)

        pygame.draw.rect(screen,(255,0,0),end_rect)
        screen.blit(playerImage, player.rect)
        screen.blit(buffcd, (40,40))
        screen.blit(dashp, (1250,40))


    if gamestate == "Facts2":
        screen.blit(fact, (0,0))

    if gamestate == "Loading6":
        screen.blit(background_image,(0,0)) 

    
        for wall in walls:
            pygame.draw.rect(screen,wall_colour,wall.rect)

        for enemy in enemies:
            screen.blit(eImage, enemy.rect)

        for buff in buffs:
            screen.blit(pillImage, buff.rect)

        pygame.draw.rect(screen,(255,0,0),end_rect)
        screen.blit(playerImage, player.rect)
        screen.blit(buffcd, (40,40))
        screen.blit(dashp, (1250,40))

    if gamestate == "Loading7":
        screen.blit(gamewon_image, (0,0))
        namebox.draw(screen)

    if gamestate == "GameWon2":
        screen.blit(gamewon_image2, (0,0))
        gameWonEbutton.draw()

    if gamestate == "HighScore":
        screen.blit(highscore_screen, (0,0))
        hsHomeButton.draw()
        hsblitting()
        

        
        
        
#FADE IN AND OUT FOR TRANSITIONS AND DEATHS#########################
def fadeIn(width, height): 
    fade = pygame.Surface((width, height))
    fade.fill((0,0,0))
    for alpha in range(0, 200):
        fade.set_alpha(alpha)
        redrawWindow()
        screen.blit(fade, (0,0))
        pygame.display.update()
        pygame.time.delay(1)

def fadeOut(width, height):
    fade = pygame.Surface((width, height))
    fade.fill((0,0,0))
    for alpha in range(0, 200):
        gradient = 200 - alpha
        fade.set_alpha(gradient)
        redrawWindow()
        screen.blit(fade, (0,0))
        pygame.display.update()
        pygame.time.delay(1)

def fadeInDeath(width, height): 
    fade = pygame.Surface((width, height))
    fade.fill((126,25,27))
    for alpha in range(0, 250):
        fade.set_alpha(alpha)
        redrawWindow()
        screen.blit(fade, (0,0))
        pygame.display.update()
        pygame.time.delay(1)

def fadeOutDeath(width, height): 
    fade = pygame.Surface((width, height))
    fade.fill((126,25,27))
    for alpha in range(0, 250):
        gradient = 250 - alpha
        fade.set_alpha(gradient)
        redrawWindow()
        screen.blit(fade, (0,0))
        pygame.display.update()
        pygame.time.delay(1)

#MAKE TEXT APPEAR
def textRender(textToRender,textx,texty):
    textSurface = fontt.render(textToRender,True,BLACK)
    textRect = textSurface.get_rect()
    textRect.center = (textx,texty)
    screen.blit(textSurface,textRect)

#BLIT CSV TEXT TO SCREEN
def hsblitting():
    scoreshow = []
    xname = 900
    xtime = 1169
    y = 130
    with open('sortedscores.csv', mode='r') as sortedscores:
        csvRead = csv.reader(sortedscores)
        for row in csvRead:
            scoreshow.append(row)
        if len(scoreshow) <= 5:
            for i in range(1,len(scoreshow)):
                for j in range(1,2):
                    textRender(scoreshow[i][j], xtime, y)

                for j in range(0,1):
                    textRender(scoreshow[i][j], xname, y)

                y += 70

        elif len(scoreshow) > 5:
            for i in range(1,6):
                for j in range(1,2):
                    textRender(scoreshow[i][j], xtime, y)

                for j in range(0,1):
                    textRender(scoreshow[i][j], xname, y)

                y += 70
            
            
            

            
            
            
os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()
pygame.mixer.init()

#BASICALLY DISPLAY AND IMAGES
pygame.display.set_caption("Demon Samurai")
width = 1440
height = 750
screen = pygame.display.set_mode((width, height))
fact1_image = pygame.image.load("Facts1.png").convert()
fact2_image = pygame.image.load("Facts2.png").convert()
fact3_image = pygame.image.load("Facts3.png").convert()
fact4_image = pygame.image.load("Facts4.png").convert()
fact5_image = pygame.image.load("Facts5.png").convert()
fact6_image = pygame.image.load("Facts6.png").convert()
fact7_image = pygame.image.load("Facts7.png").convert()
fact8_image = pygame.image.load("Facts8.png").convert()
fact9_image = pygame.image.load("Facts9.png").convert()
fact10_image = pygame.image.load("Facts10.png").convert()
background_image = pygame.image.load("floor.png").convert()
gameover_image = pygame.image.load("GameOverImage.jpg").convert()
MainMenu_image = pygame.image.load("MainMenu.png").convert()
gamewon_image2 = pygame.image.load("GameWon2.png").convert()
gameoverbutton_image = pygame.image.load("GWEbutton.png").convert()
SettingsScreen_image = pygame.image.load("Settings.jpg").convert()
settings_button = pygame.image.load("settingsbutton.png").convert()
SettingsHome_button = pygame.image.load("settingshomebutton.jpg").convert()
highscoreHome_button = pygame.image.load("hshbutton.jpg").convert()
highscore_button = pygame.image.load("highscorebutton.png").convert()
Exit_button = pygame.image.load("exitbutton.png").convert()
highscore_screen = pygame.image.load("hScreen.jpg").convert()
Play_button = pygame.image.load("playgamebutton.png").convert()
GOE_button = pygame.image.load("GOEbutton.jpg").convert()
eImage = pygame.image.load("enemyImage.png")
pillImage = pygame.image.load("pill.png")
gamewon_image = pygame.image.load("GameWon1.png").convert()
global playerImage
playerImage = pygame.image.load("playerImage.png")
global buffcd
buffcd = pygame.image.load("0cd.png")
global dashp
dashp = pygame.image.load("DashIcon.png")


#Here are the buttons
settingsButton = Button(settings_button, 192, 336,"showSettingsScreen")
settingsHomeButton = Button(SettingsHome_button, 1320, 702, "showMainMenu")
exitButton = Button(Exit_button, 1244, 345, "ExitGame")
playButton = Button(Play_button, 1245, 134, "startGame")
GOEbutton = Button(GOE_button, 710, 395, "ExitGame")
gameWonEbutton = Button(gameoverbutton_image, 710, 555, "ExitGame")
highScoreButton = Button(highscore_button, 192, 130, "showHighScore")
hsHomeButton = Button(highscoreHome_button, 1388, 706, "goHomeFromHS")
#Buttons Stop Here

#VARIABLES, LISTS AND STUFF
clock = pygame.time.Clock()
gamestate = "MainMenu"
buttons = [settingsButton, highScoreButton, settingsHomeButton, hsHomeButton, exitButton, playButton, GOEbutton, gameWonEbutton]
facts = [fact1_image, fact2_image, fact3_image, fact4_image, fact5_image, fact6_image, fact7_image, fact8_image, fact9_image, fact10_image]
background_music = "MainMusic.mp3"
pygame.mixer.music.load(background_music)
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.1)
walls = []
enemies = []
buffs = []
player = Player()
colour = (0,128,255)
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
BLACK = (0,0,0)
FONT = pygame.font.Font(None, 32)
fontt = pygame.font.Font(None, 46)
wall_colour = (0,0,0)
enemy_colour = (255,255,51)
current_score = 0
namebox = InputBox(600, 400, 200, 32)
global text_av
text_av = 0
global dash_cooldown
dash_cooldown = 0
global level_count
level_count = -1
global exvel
global eyvel
global fadeav
global gametime
global sortav
global buffav
global buffstart
buffstart = time.time()
global buffend
buffend = time.time()
buffav = False
sortav = 0
fadeav = 1

#in the level, W means Wall, E mean Exit, X means enemies and B means buff:

level = [
"WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
"W         W                                    W",
"W         W                                    W",
"W         W                                    W",
"W         W                            X       W",
"W         W                       W            W",
"W         W                       W            W",
"W         W                       W            W",
"W         WWWWWWWWWWWWW           W            W",
"W         W                       W            W",
"W         W       X               W            W",
"W  B      W                       W            W",
"W         W                       W            W",
"W         W                       W            W",
"W         W                       W    X       W",
"W         W                       W            W",
"W         W       X               W            W",
"W         W                       W            W",
"W         W                       W            W",
"W         WWWWWWWWWWWWW           W            W",
"W                                 W            W",
"W                                 W            W",
"W              X                  W EE         W",
"W                                 W EE         W",
"WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
]

levels = [[
"WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
"W        W                                     W",
"W   E    W                          X          W",
"W        W                                     W",
"W        W                                     W",
"W        W                                     W",
"W        W                                     W",
"W        W             X                       W",
"W        W                                     W",
"W        W                                     W",
"W        W                                     W",
"W        W                                     W",
"W        W                                     W",
"W        W                                     W",
"W                 X                            W",
"W                                    B         W",
"W                                              W",
"W   X                                          W",
"W                                              W",
"W                                              W",
"W                                              W",
"W                                              W",
"W      X                                       W",
"W                                              W",
"WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
],[
"WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
"W                         W                    W",
"W                         W        X           W",
"W                         W                    W",
"W                         W                    W",
"W                         W                    W",
"W                         W          W         W",
"W              X          W          W         W",
"W                         W          W         W",
"W  B                      W          W         W",
"W                         W     B    W         W",
"W                                    W    X    W",
"W                                    W         W",
"W                                    W         W",
"W                                    W         W",
"W                            X       W         W",
"W                                    W         W",
"W                                    W         W",
"W                                    W         W",
"WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW         W",
"W                                              W",
"W    E                  X                X     W",
"W                                              W",
"W                                              W", 
"WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
],[
"WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
"W         W                                    W",
"W         W                                    W",
"W         W               X                    W",
"W         W                                    W",
"W    B    W           WWWWWWWWWWWWW            W",
"W         W                       W            W",
"W         W     X                 W            W",
"W         W                       W            W",
"W         W                       W        X   W",
"W    X    W                       W            W",
"W         W                       W            W",
"W         W             X         W            W",
"W         W                       W            W",
"W         W                       W            W",
"W         W                       W            W",
"W         W                       W            W",
"W         W                       W            W",
"W              WWWWWWWWW          W      X     W",
"W                                 W            W",
"W            B                    W            W",
"W                                 W            W",
"W                                 W EE         W",
"W                                 W EE         W",
"WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
],[
"WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
"W                                              W",
"W                    X                   X     W",
"W                                              W",
"W                                              W",
"W     X                                        W",
"W                                              W",
"W                                              W",
"W                             W                W",
"W                             W                W",
"W                             W                W",
"W                             W                W",
"W                             W                W",
"W   X                         W                W",
"W                          E  W                W",
"W    WWWWWWWWWWWWWWWWWWWWWWWWWW                W",
"W    W                   X    W                W",
"W    W                        W                W",
"W    W                        W                W",
"W  B W          X                              W",
"W    W                            B            W",
"W    W                                         W",
"W    W                                         W",
"W    W                                         W",
"WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
],[
"WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
"W                                              W",
"W                                       X      W",
"W                                              W",
"W   X                                          W",
"W                                              W",
"W                                        B     W",
"W             WWWWWWWWWWWWWWWWWWWWWWWW         W",
"W             W                      W         W",
"W             W                      W         W",
"W             W                      W         W",
"W             W      B               W         W",
"W             W                      W         W",
"W             W                      W         W",
"W             W            W         W    X    W",
"W       B     W            W         W         W",
"W             W            W         W         W",
"W             W            W         W         W",
"W             W            W         W         W",
"W   X         W            W         W         W",
"W             WWWWWWWWWWWWWW         W         W",
"W              X                     W         W",
"W                               X    W     E   W",
"W                                    W         W",
"WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
]]



x = y = 0
for row in level:
    for col in row:
        if col == "W":
            Wall(x, y)
        if col == "E":
            end_rect = pygame.Rect(x,y,30,30)
        if col == "X":
            Enemy(x,y)
        if col == "B":
            Buff(x,y)
        x += 30
    y += 30
    x = 0  



#MAIN GAME LOOP STARTS HERE

running = True

while running:
    clock.tick(60)
    mousePos = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                for button in buttons:
                    if button.rect.collidepoint(mousePos):
                        button.Click()

        namebox.handle_event(event)

#MAIN MENU

    if gamestate == "MainMenu":
        screen.blit(MainMenu_image, (0,0))
        settingsButton.draw()
        exitButton.draw()
        playButton.draw()
        highScoreButton.draw()

#SETTINGS MENU

    if gamestate == "Settings":
        screen.blit(SettingsScreen_image, (0,0))
        settingsHomeButton.draw()


#GAME OVER MENU GAMESTATE
    if gamestate == "GameOver":
        screen.blit(gameover_image, (0,0))
        GOEbutton.draw()


#GAME WON GAMESTATE

    if gamestate == "GameWon":
        screen.blit(gamewon_image, (0,0))
        namebox.draw(screen)

    if gamestate == "GameWon2":
        screen.blit(gamewon_image2, (0,0))
        gameWonEbutton.draw()

#HIGHSCORE MENU

    if gamestate == "HighScore":
        screen.blit(highscore_screen, (0,0))
        hsHomeButton.draw()
        hsblitting()
        

#LOADING SCREENS FOR TRANSITIONS WITH FADE

    if gamestate == "Loading":
        fadeInDeath(1440, 750)
        gamestate = "Loading2"

    if gamestate == "Loading2":
        fadeOutDeath(1440, 750)
        gamestate = "GameOver"

    if gamestate == "Loading3":
        fadeOut(1440, 750)
        gamestate = "Game"

    if gamestate == "Loading4":
        fadeIn(1440, 750)
        gamestate = "Loading5"

    if gamestate == "Loading5":
        fadeOut(1440, 750)
        gamestate = "Facts2"

    if gamestate == "Loading6":
        fadeIn(1440, 750)
        gamestate = "Loading7"

    if gamestate == "Loading7":
        fadeOut(1440, 750)
        gamestate = "GameWon"


    



#FACTS SCREEN FOR START GAME BUTTON
    if gamestate == "Facts":
        screen.blit(fact, (0,0))
        user_input = pygame.key.get_pressed()
        if user_input[pygame.K_k]:
            fadeIn(1440, 750)
            gamestate = "Loading3"



#FACTS SCREEN FOR SWITCHING BETWEEN LEVELS (LEVEL SWITCHING CODE INVOLVED)
    if gamestate == "Facts2":
        screen.blit(fact, (0,0))
        user_input = pygame.key.get_pressed()
        if user_input[pygame.K_k]:
            level_count = level_count + 1
            del walls[:]
            del enemies[:]
            del buffs[:]
            level = levels[level_count]
            x = y = 0
            for row in level:
                for col in row:
                    if col == "W":
                        Wall(x, y)
                    if col == "E":
                        end_rect = pygame.Rect(x,y,30,30)
                    if col == "X":
                        Enemy(x, y)
                    if col == "B":
                        Buff(x,y)
                    x += 30
                y += 30
                x = 0
            fadeIn(1440, 750)
            gamestate = "Loading3"

#BASICALLY THE MAIN GAME (AFTER PRESSING START GAME)

    if gamestate == "Game":

        user_input = pygame.key.get_pressed()

        #CHECK INPUTS FROM USER
        #MOVEMENT KEYS
        if user_input[pygame.K_w]:
            if buffav:
                player.move(0,-10)
            else:
                player.move(0,-5)

        if user_input[pygame.K_s]:
            if buffav:
                player.move(0,10)
            else:
                player.move(0,5)

        if user_input[pygame.K_a]:
            if buffav:
                player.move(-10,0)
            else:
                player.move(-5,0)
            if player.rect.x < 0:
                player.rect.x= width -1

        if user_input[pygame.K_d]:
            if buffav:
                player.move(10,0)
            else:
                player.move(5,0)
            if player.rect.x > width:
                player.rect.x= -59

        #DASHING COMBINATIONS
        if user_input[pygame.K_w] and user_input[pygame.K_SPACE]:
            if dash_cooldown == 0:
                player.move(0,-150)
                dash_cooldown = 1
                if player.rect.y < 0:
                    player.rect.y = 60


        if user_input[pygame.K_s] and user_input[pygame.K_SPACE]:
            if dash_cooldown == 0:
                player.move(0,150)
                dash_cooldown = 1
                if player.rect.y > height:
                    player.rect.y = height - 60
       

        if user_input[pygame.K_a] and user_input[pygame.K_SPACE]:
            if dash_cooldown == 0:
                player.move(-150,0)
                dash_cooldown = 1
                if player.rect.x < 0:
                    player.rect.x = 60

        if user_input[pygame.K_d] and user_input[pygame.K_SPACE]:
            if dash_cooldown == 0:
                player.move(150,0)
                dash_cooldown = 1
                if player.rect.x > width:
                    player.rect.x = width - 60
        #WHEN SWITCHING LEVELS, CHECK IF ENEMIES ARE ALL DEAD.
        if player.rect.colliderect(end_rect):
            if len(enemies) == 0:
                if level_count == len(levels) - 1:
                    end = time.time()
                    gametime = (end - start)//1
                    print (gametime)
                    gamestate = "Loading6"
                else:
                    fact = random.choice(facts)
                    gamestate = "Loading4"
        #CHANGING PLAYER MODEL DEPENDING ON ACTION
        if user_input[pygame.K_k]:
            playerImage = pygame.image.load("playerImage2.png")

        elif user_input[pygame.K_s]:
            playerImage = pygame.image.load("movedown2.png")

        elif user_input[pygame.K_w]:
            playerImage = pygame.image.load("moveup2.png")

        elif user_input[pygame.K_a]:
            playerImage = pygame.image.load("moveleft2.png")

        elif user_input[pygame.K_d]:
            playerImage = pygame.image.load("moveright2.png")

        else:
            playerImage = pygame.image.load("playerImage.png")
            


            
        # WHEN PLAYER ATTACKS, IF ENEMY IS IN RANGE KILL ENEMY
        for enemy in enemies:
            if (player.rect.x - enemy.rect.x < 150 and player.rect.x - enemy.rect.x >-150) and ( player.rect.y - enemy.rect.y < 150 and player.rect.y - enemy.rect.y > -150) and (user_input[pygame.K_k]):
                enemies.pop(enemies.index(enemy))
                dash_cooldown = 0

        # FOLLOW PLAYER AROUND WHEN PLAYER IN RANGE
        for enemy in enemies:
            if (player.rect.x - enemy.rect.x < 300 and player.rect.x - enemy.rect.x >-300) and (player.rect.y - enemy.rect.y < 300 and player.rect.y - enemy.rect.y > -300):
                if player.rect.x > enemy.rect.x:
                    enemy.rect.x = enemy.rect.x + 8
                else:
                    enemy.rect.x = enemy.rect.x - 8

                if player.rect.y > enemy.rect.y:
                    enemy.rect.y = enemy.rect.y + 8
                else:
                    enemy.rect.y = enemy.rect.y - 8
            #END GAME WHEN PLAYER GETS TOUCHED
            if enemy.rect.colliderect(player.rect):
                time.sleep(0.2)
                gamestate = "Loading"
        #BLOCK ENEMIES FROM GOING THROUGH WALLS
        for enemy in enemies:
            for wall in walls:
                if enemy.rect.colliderect(wall.rect):
                    if enemy.rect.x > wall.rect.x:
                        enemy.rect.left = wall.rect.right
                    if enemy.rect.x < wall.rect.x:
                        enemy.rect.right = wall.rect.left
                    if enemy.rect.y < wall.rect.y:
                        enemy.rect.bottom = wall.rect.top
                    if enemy.rect.y > wall.rect.y:
                        enemy.rect.top = wall.rect.bottom
        #CHECK FOR COLLISION WITH BUFFS
        for buff in buffs:
            if player.rect.colliderect(buff.rect):
                buffav = True
                buffs.pop(buffs.index(buff))
                buffstart = time.time()
        #MAKE COUNTDOWN FOR BUFFS APPEAR ON SCREEN WHEN PLAYER EATS A PILL
        if buffav:
            buffend = time.time()
            if buffend - buffstart > 0 and buffend - buffstart < 1:
                buffcd = pygame.image.load("Number2.png")
            elif buffend - buffstart >1 and buffend - buffstart < 2:
                buffcd = pygame.image.load("Number1.png")
            elif buffend - buffstart > 2:
                buffcd = pygame.image.load("0cd.png")
                buffav = False

        #MAKE DASH ICON APPEAR ON SCREEN IF DASH IS AVAILABLE
        if dash_cooldown == 0:
            dashp = pygame.image.load("DashIcon.png")

        else:
            dashp = pygame.image.load("0cd.png")



        #DRAW STUFF ON SCREEN
        screen.blit(background_image,(0,0)) 

    
        for wall in walls:
            pygame.draw.rect(screen,wall_colour,wall.rect)

        for enemy in enemies:
            screen.blit(eImage, enemy.rect)

        for buff in buffs:
            screen.blit(pillImage, buff.rect)

        pygame.draw.rect(screen,(255,0,0),end_rect)
        screen.blit(playerImage, player.rect)
        screen.blit(buffcd, (40,40))
        screen.blit(dashp, (1250,40))
    



    pygame.display.flip()

pygame.quit()
