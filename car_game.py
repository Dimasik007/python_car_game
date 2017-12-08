"simple car game developed in Pygame"
"win the game by getting 50 points"

import sys
import time
import random
from pygame import *
from pygame.locals import *

WIDTH = 800 # screen width
HEIGHT = 600 # screen height
BORDER = 10 # road border
RIGHTROAD = 500
LEFTROAD = 90
FRAMERATE = 60 # to put in clocktime
SENS = 5  # sensitivity of car movement
WINPOINT = 50 # points to win the game
point = 0
speed = 15 # initial speed
collision_err = 5 # to prevent collision error

init()
mixer.pre_init(44100,16,2,4096) # default parameters

# create display
screen = display.set_mode([WIDTH, HEIGHT]) # create display
display.set_caption('Fast and Furious - Winter is Coming') # name of the game at the top of display
clock = time.Clock()

# surface images
surface = image.load('background.png').convert()
start_menu = image.load('start_menu.jpg').convert()

# car images
carr3 = image.load('carOpponent03.png').convert_alpha()
carr2 = image.load('carOpponent2.png').convert_alpha()
carimage = image.load('carPlayer.png').convert_alpha()

# other images
obstaclee = image.load('9ma.png').convert_alpha()
car_crash = image.load('boom.png').convert_alpha()
starr = image.load('star.png').convert_alpha()
winner = image.load('win.png').convert()

#sounds
mixer.music.load("song.wav")
lose_point = mixer.Sound("obstacle.wav")
crash_sound =mixer.Sound("crash.wav")
get_star = mixer.Sound("gotitem.wav")
sound_win = mixer.Sound("Give_Away.wav")


# create player car
class Car :
    # default car parameters
    CARWIDTH = 44
    CARHEIGHT = 89
    CARPOSY = HEIGHT-CARHEIGHT
    point = 0

    def __init__(self,x) :
        self.x = x

    def show(self) :
        screen.blit(carimage, (self.x, self.CARPOSY - (2 * collision_err)))

    def update(self) :
            global point
            newx = self.x
            if newx <= LEFTROAD or newx + self.CARWIDTH >= RIGHTROAD: # check border collision
                crash(self.x,Car.CARPOSY)

            elif star.y >= Car.CARPOSY - Star.starH - collision_err and star.y <= HEIGHT- (Star.starH//2) \
                 and (star.x + Star.starW >= newx + collision_err \
                and star.x <= newx+self.CARWIDTH - collision_err) : # check star collision
                mixer.Sound.play(get_star) # sound for get point
                self.x = newx
                star.show() # to spawn star again
                star.update()
                self.show()
                Car.point += 3 # increase point

            elif ((car2.y >= Car.CARPOSY - Car.CARHEIGHT + collision_err) and car2.y <= HEIGHT- (Car.CARHEIGHT//2)\
                  and (car2.x + Car.CARWIDTH >= newx + collision_err and car2.x <= newx+Car.CARWIDTH-collision_err)) \
                  or ((car3.y >= Car.CARPOSY - Car.CARHEIGHT + collision_err) and car3.y <= HEIGHT- (Car.CARHEIGHT//2) \
                  and (car3.x + Car.CARWIDTH >= newx+collision_err and car3.x <= newx + Car.CARWIDTH - collision_err)) :
                crash(self.x, Car.CARPOSY)  # check collision with other cars

            elif obstacle.y >= Car.CARPOSY - Obstacle.obsH - collision_err and obstacle.y <= HEIGHT- (Obstacle.obsH//2) \
                 and (obstacle.x + Obstacle.obsW >= newx and obstacle.x <= newx+Car.CARWIDTH): # check obstacle collision

                mixer.Sound.play(lose_point) #sound for lose point
                self.x = newx
                self.show()
                obstacle.show()
                obstacle.update()
                if Car.point <= 0 : # decrease it if it is not under 0
                    Car.point = 0
                else:
                    Car.point -= 1 # decrease point
            else:
                self.x = newx
                self.show()


 # create star
class Star :
    # star parameters
    starW = 33
    starH = 33

    def __init__(self,x,y) :
        self.x = x
        self.y = y
    def show(self) :
        self.x = random.randrange(LEFTROAD + BORDER, RIGHTROAD - Star.starW) # random position for star
        self.y = 0 # star position

    def update (self) :
        self.y += abs(16/4 + (Car.point/2)) # speed of star
        screen.blit(starr, (self.x, self.y)) # function to place sprite on screen
        if self.y >= HEIGHT :
            self.show()

# create obstacle
class Obstacle :
    # obstacle parameters
    obsW = 48
    obsH = 25

    def __init__(self, x, y) :
        self.x = x
        self.y = y
    def show(self) :
       self.x = random.randrange(LEFTROAD + BORDER, RIGHTROAD - Obstacle.obsW) # random x position for obstacle
       self.y = 0 # obstacle position
    def update(self) :
        self.y += 7/4 + (Car.point/3) # obstacle speed
        screen.blit(obstaclee, (self.x, self.y))
        if self.y >= HEIGHT :
            self.show()

class Opponent2 : # same sizes with own car
    def __init__(self, x, y) :
        self.x = x
        self.y = y
    def show (self) : #random x poisition for blue car
        self.x = random.randrange(LEFTROAD + BORDER, (RIGHTROAD + LEFTROAD + BORDER) //2 - Car.CARWIDTH)
        self.y = 0 # y position
    def update(self) :
        self.y += 6/4 + (Car.point/3) # speed of red car
        screen.blit(carr2,(self.x, self.y))
        if self.y >= HEIGHT :
            self.show()

class Opponent3 :
    def __init__(self, x, y) :
        self.x = x
        self.y = y
    def show (self) : #random x poisition for green car
        self.x = random.randrange((LEFTROAD + BORDER + RIGHTROAD)//2, RIGHTROAD - Car.CARWIDTH)
        self.y = 0 # y position
    def update(self) :
        self.y += 6/5 + (Car.point/3) #speed of green car
        screen.blit(carr3, (self.x, self.y))
        if  self.y >= HEIGHT :
            self.show()


class Menu :
# first two are coordinates of a button, then name of the button, color, color when active, id number
    def __init__ (self, menuItem = [0, 0, 'Button', Color("white"), Color("green"), 0]) :
        self.menuItem = menuItem

    def render (self, introScreen, font, buttonID) : # to highlight the menu buttons when they are chosen
        for i in self.menuItem :
            if buttonID == i[5] :
                introScreen.blit(font.render(i[2], 1, i[4]), (i[0], i[1])) # if activated color green
            else :
                introScreen.blit(font.render(i[2], 1, i[3]), (i[0], i[1])) # else white

    def menu (self) :
        done = True
        font_menu = font.Font(font.get_default_font(), 50) # set the font
        button = 0
        while done :
            screen.blit(start_menu, (0,0)) #put picture on the start menu

            mousePosition = mouse.get_pos()  # get mouse position
            for i in self.menuItem : # to check if mouse coordinate intersect with button coordinate
                if mousePosition[0] > i[0] and mousePosition[0] < i [0] + 100 \
                   and mousePosition[1] > i[1] and mousePosition[1] < i[1] + 50 :
                    button = i[5]
            self.render(screen, font_menu, button)

            for e in event.get() :
                if e.type == QUIT :
                    quit()
                    sys.exit()
                if e.type == KEYDOWN : # from here
                    if e.key == K_ESCAPE :
                        quit()
                        sys.exit()
                    if e.key == K_UP :
                        if button > 0 :
                            button -= 1
                    if e.key == K_DOWN :
                        if button < len(self.menuItem) - 1 :
                            button += 1
                    if e.key == K_RETURN :
                        if button == 0 :
                            done = False
                            game_loop() # enter game_loop
                        elif button == 1 :
                            quit()
                            sys.exit() # to here, keyboard navigation
                if e.type == MOUSEBUTTONDOWN and e.button == 1 : # mouse navigation
                    if button == 0 :
                        game_loop() # enter game_loop
                        done = False
                    elif button == 1 :
                        quit()
                        sys.exit()

            clock.tick(FRAMERATE)
            display.flip()


menuItem = [(60, 90, 'Play', Color("white"), Color("green"), 0),
            (60, 150, 'Exit', Color("white"), Color("green"), 1)]
game = Menu(menuItem)


def show_message(text, x, y, col) : # to show message on the screen, selecting position and color
    myFont = font.SysFont(font.get_default_font(), 50) #to use system font
    surf = myFont.render(text, False, Color(col))
    screen.blit(surf, (x, y))


def pause_game () :
    mixer.music.pause() # pause music

    pause = True
    while pause :
        for e in event.get() :
            if e.type == QUIT :
                quit()
                sys.exit()
            if e.type == KEYDOWN :
                if e.key == K_SPACE : # to pause use "space"
                    pause = False
                    mixer.music.unpause() # unpause music
                elif e.key == K_ESCAPE :
                    quit()
                    sys.exit()
        screen.blit(start_menu, (0,0))
        show_message("Game Paused", 500, 80, "red") # show pause message
        display.flip()
        clock.tick(5)


def you_win () : # lets the player win the game

    mixer.music.pause()
    screen.blit(winner, (0,0))
    show_message("Your Score: {}".format(Car.point), 280, 430, "Blue")
    display.update()
    mixer.Sound.play(sound_win)
    clock.tick(10)

    while True :
        for e in event.get() :
            if e.type == QUIT :
                quit()
                sys.exit()
        time.delay(5000)
        Car.point = 0
        game.menu()


def crash(x, y) :

    screen.blit(car_crash, ((car.x), (500))) # put crash image
    show_message("GAME OVER", (LEFTROAD+RIGHTROAD)/2 - 100,HEIGHT//2, "red")
    show_message("Your Score : {}".format(Car.point), (LEFTROAD+RIGHTROAD)/2 - 100,HEIGHT//2 + 50, "red")
    display.update() # to show crash image and score
    mixer.music.stop()
    mixer.Sound.play(crash_sound)

    while True:
        for e in event.get() :
            if e.type == QUIT :
                quit()
                sys.exit()
        time.delay(2000) # freeze the screen for 2 seconds
        Car.point = 0 # refresh car point
        car.x = ((LEFTROAD+RIGHTROAD)//2) - (Car.CARWIDTH//2) #refresh car x position
        game.menu()


# create star object
star = Star(random.randrange(LEFTROAD + Star.starW, RIGHTROAD - Star.starW), 0)

# create  obstacle object
obstacle = Obstacle(random.randrange(LEFTROAD + Obstacle.obsW, RIGHTROAD - Obstacle.obsW), 0)

# for opponent2
car2 = Opponent2(random.randrange(LEFTROAD + Star.starW, RIGHTROAD + LEFTROAD//2 - Car.CARWIDTH), 0)

# for opponent3
car3 = Opponent3(random.randrange(LEFTROAD + RIGHTROAD//2, RIGHTROAD - Car.CARWIDTH), 0)

# create player car
car = Car(((LEFTROAD + BORDER) + RIGHTROAD)//2)



def game_loop () : # main game loop
    mixer.music.play(-1)
    key.set_repeat(1, 1) # so you don't need to press arrows multiple times
    y = 0

# place objects on the screen
    car.show()
    car3.show()
    car2.show()
    obstacle.show()
    star.show()

    while True :
    # move the background
        rel_y = y % surface.get_rect().height
        screen.blit(surface, (0, rel_y - surface.get_rect().height))
        if rel_y < HEIGHT :
            screen.blit(surface, (0, rel_y))
        y += 6/4 + (Car.point/3)

    # draw road and borders
        draw.rect(screen, Color("grey"), [100,0, 400,HEIGHT])
        draw.rect(screen, Color("white"), [90,0, BORDER, HEIGHT])
        draw.rect(screen, Color("white"), [500,0, BORDER, HEIGHT])

    # draw lines
        draw.line(screen, Color("yellow"), [200,0], [200, HEIGHT], 5)
        draw.line(screen, Color("yellow"), [300,0], [300, HEIGHT], 5)
        draw.line(screen, Color("yellow"), [400,0], [400, HEIGHT], 5)

    # show points and speed on the screen
        show_message("Points = {}".format(Car.point), 550, 80,"blue")
        show_message("Speed = {}km/h".format(abs(speed + (Car.point * 5))), 515, 120,"blue")

        e = event.poll()
        if e.type == QUIT :
            break
        if e.type == KEYDOWN: # keyboard navigation for car
            if e.key == K_LEFT :
                car.x -= SENS
            elif e.key == K_RIGHT :
                car.x += SENS
            if e.key == K_SPACE :
                pause_game()
        if Car.point >= WINPOINT : # point after which you get winner image and sent to the main menu
            you_win()

    # update objects
        car.update()
        star.update()
        obstacle.update()
        car2.update()
        car3.update()
        display.update()
        clock.tick(FRAMERATE)
    quit()
    sys.exit()

game.menu() # to invoke game menu at the begining of the game
