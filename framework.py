import pygame
import sys
import os
from menu import *

background = pygame.image.load(os.path.join('images', 'floor.png'))


class Player(pygame.sprite.Sprite):
    # constructor for this class
    def __init__(self):
        # call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        # create 50px by 50px surface
        self.image = pygame.Surface((16, 16))
        # color the surface cyan
        #self.image.fill((0, 205, 205))
        self.image = pygame.image.load(os.path.join('images', 'player.png'))
        self.rect = self.image.get_rect()
        self.speed = [0, 0]

    def left(self):
        self.speed[1]=0
        self.speed[0] = -4

    def right(self):
        self.speed[1]=0
        self.speed[0] = 4

    def up(self):
        self.speed[0]=0
        self.speed[1] = -4

    def down(self):
        self.speed[0]=0
        self.speed[1] = 4

    def move(self):
        # move the rect by the displacement ("speed")
        self.rect = self.rect.move(self.speed)

class Aisle(pygame.sprite.Sprite):
    def __init__(self, spr):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((250, 40))
        self.image = pygame.image.load(os.path.join('images', spr))
        self.rect = self.image.get_rect()
        self.speed = [0, 0]

    # Checks whether
    def detectCollision(self, sprt):
        if sprt.rect.colliderect(self.rect):
            dx = sprt.speed[0]
            dy = sprt.speed[1]
            if dx > 0 :
                sprt.speed[0]=0
                sprt.rect.x -= dx #aisle.rect.left-1
            if dx < 0 :
                sprt.speed[0]=0
                sprt.rect.x -= dx #aisle.rect.right+1
            if dy > 0 :
                sprt.speed[1]=0
                sprt.rect.y -= dy #aisle.rect.top-1
            if dy < 0 :
                sprt.speed[1]=0
                sprt.rect.y -= dy #aisle.rect.bottom+1


class Employee(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # load the PNG
        self.image = pygame.image.load(os.path.join('images', 'ball.png'))
        self.rect = self.image.get_rect()

    def move(self):
        self.rect = self.rect.move(self.speed)

    def dir_x(self):
        return 1 if self.speed[0] > 0 else -1

    def dir_y(self):
        return 1 if self.speed[1] > 0 else -1


def event_loop():
    def DrawBackground(background):
        screen.blit(background, [0, 0])
    
    class Family(pygame.sprite.Sprite):
        def __init__(self, name, hunger, thirst, heat, clean, sick, health):
            pygame.sprite.Sprite.__init__(self)
            families.append(self)
            self.name = name
            self.mhunger = hunger
            self.mthirst = thirst
            self.mheat = heat
            self.mclean = clean
            self.sick = sick
            self.mhealth = health
            self.status = "Alive"
            
            self.hunger = self.mhunger
            self.thirst = self.mthirst
            self.heat = self.mheat
            self.clean = self.mclean
            self.health = self.mhealth
        
        
    # get the pygame screen and create some local vars
    screen = pygame.display.get_surface()
    screen_rect = screen.get_rect()
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    # set up font
    basicFont = pygame.font.SysFont(None, 16)
    # initialize a clock
    clock = pygame.time.Clock()
    frame_count = 0
    frame_rate = 60
    start_time = 90
    
    # initialize the score counter
    score = 0
    
    # Game State, 0- game map, 1- results screen, 2- gameover
    game_state = 0
    game_day = 1
    
    # initialize the player and the enemy
    player = Player()
    #name, hunger, thirst, heat, clean, sick, health
    families = []
    mother = Family("Mother-in-Law", 6, 2, 5, 3, 0, 5)
    wife = Family("Wife", 8, 2, 5, 5, 0, 5)
    son = Family("Son", 7, 2, 5, 4, 0, 3)
    dog = Family("Fido", 5, 2, 7, 4, 0, 4)

    #Employees (enemies)
    emp1 = Employee()
    emp1.rect.bottomleft = 0, screen_height
    emp1.speed = [6, 0]
    

    inventory= []

    aisles = []
    spr = ['aisle_cloth.png','aisle_drink.png','aisle_food.png','aisle_game.png','aisle_med.png','aisle_soap.png']
    for i in range(0, 3):
        print i
        aisle1 = Aisle(spr[i])
        aisle2 = Aisle(spr[3+i])
        offset = i*screen_height/4
        aisle1.rect.topleft = 40, (offset+40)
        aisle2.rect.topright = (screen_width-40), (offset+40)
        aisles.append(aisle1)
        aisles.append(aisle2)

    # create a sprite group for the player and enemy
    # so we can draw to the screen
    sprite_list = pygame.sprite.Group()
    sprite_list.add(player)
    # sprite_list.add(enemy)
    for aisle in aisles:
        sprite_list.add(aisle)

    # create a sprite group for enemies only to detect collisions
    enemy_list = pygame.sprite.Group()
    enemy_list.add(emp1)

    # main game loop
    while 1:
        if game_state==0: #Main Game Room
            # custom background
            DrawBackground(background)
            
            # handle input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        player.left()
                    elif event.key == pygame.K_RIGHT:
                        player.right()
                    elif event.key == pygame.K_UP:
                        player.up()
                    elif event.key == pygame.K_DOWN:
                        player.down()
                        
                
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT and player.speed[0]<0:
                        player.speed[0]=0
                    elif event.key == pygame.K_RIGHT and player.speed[0]>0:
                        player.speed[0]=0
                    elif event.key == pygame.K_UP and player.speed[1]<0:
                        player.speed[1]=0
                    elif event.key == pygame.K_DOWN and player.speed[1]>0:
                        player.speed[1]=0
                        
            # call the move function for the player
            player.move()

            # Collision detection for aisles.
            for aisle in aisles:
                aisle.detectCollision(player)

                        
            # check player bounds
            if player.rect.left < 0:
                player.rect.left = 0
            if player.rect.right > screen_width:
                player.rect.right = screen_width
            if player.rect.top < 0:
                player.rect.top = 0
            if player.rect.bottom > screen_height:
                player.rect.bottom = screen_height

            for enemy in enemy_list:
                # reverse the movement direction if enemy goes out of bounds
                if enemy.rect.left < 0:
                    enemy.rect.left = 0
                    enemy.speed[0] = 0
                    enemy.speed[1] = -6
                if enemy.rect.right > screen_width:
                    enemy.rect.right = screen_width
                    enemy.speed[0] = -enemy.speed[0]
                if enemy.rect.top < 0:
                    enemy.rect.top = 0
                    enemy.speed[1] = -enemy.speed[1]
                if enemy.rect.bottom > screen_height:
                    enemy.rect.bottom = screen_height
                    enemy.speed[1] = 0
                    enemy.speed[0] = 6

                # Collision detection for aisles.
                for aisle in aisles:
                    aisle.detectCollision(enemy)

                enemy.move()

            # detect all collisions between the player and enemy
            # but don't remove enemy after collisions
            # increment score if there was a collision
            if pygame.sprite.spritecollide(player, enemy_list, False):
                score += 1

            
            # draw the player and enemy sprites to the screen
            sprite_list.draw(screen)
            enemy_list.draw(screen)
            
            # set up the score text
            text = basicFont.render('Score: %d' % score, True, (255, 255, 255))
            textRect = text.get_rect()
            textRect.x = screen_rect.x
            textRect.y = screen_rect.y
            # draw the text onto the surface
            screen.blit(text, textRect)
            
            # --- Timer Draw ---
            # Calculate total seconds
            total_seconds = frame_count // frame_rate
            
            # Divide by 60 to get total minutes
            minutes = total_seconds // 60
            
            # Use modulus (remainder) to get seconds
            seconds = total_seconds % 60
            
            # Use python string formatting to format in leading zeros
            output_string = "Time: {0:02}:{1:02}".format(minutes, seconds)
            
            # Blit to the screen
            text = basicFont.render(output_string, True, (255,255,255))
            screen.blit(text, [0, 16])
            # --- Timer End ---

            # update the screen
            pygame.display.flip()

            # limit to 60 FPS
            frame_count+=1
            clock.tick(frame_rate)
            
        elif game_state==1: #Days over Results Screen
            # handle input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                    
                    
            # black background
            screen.fill((0, 0, 0))
            
            white = (255,255,255)
            screen.blit(basicFont.render('DAY %d RESULTS:' % game_day, True, white),[280,70])
            screen.blit(basicFont.render('Score: %d' % score, True, white), [0,0])
            
            #list of stolen items
            screen.blit(basicFont.render("Inventory:",True, white), [120,100])
            i=1
            for item in inventory:
                screen.blit(basicFont.render(item[0]+" x%d" % item[1], True, white), [120,100+16*i])
                i+=1
            
            #family status
            i=0
            for fami in families:
                stats=""
                
                if fami.hunger < fami.mhunger/2:
                    stats+="Hungry "
                if fami.thirst < fami.mthirst/2:
                    stats+="Thirsty "
                if fami.heat < fami.mheat/2:
                    stats+="Cold "
                if fami.clean < fami.mclean/2:
                    stats+="Dirty "
                if fami.sick > 0:
                    stats+="Sick "
                if stats == "":
                    stats = "Fine"
                    
                if fami.health<1:
                    fami.status = "Dead"
                if fami.status == "Dead":
                    fami.stats = "Dead"
                screen.blit(basicFont.render(fami.name+"'s Status: %s" % stats, True, white), [340,100+16*i])
                i+=1
                
            # update the screen
            pygame.display.flip()


def main():
    # initialize pygame
    pygame.init()

    # create the window
    size = width, height = 640, 480
    screen = pygame.display.set_mode(size)

    # set the window title
    pygame.display.set_caption("Do You Even Lift?")

    # create the menu
    menu = cMenu(50, 50, 20, 5, 'vertical', 100, screen,
                 [('Start Game',   1, None),
                  ('Other Option', 2, None),
                  ('Exit',         3, None)])
    # center the menu
    menu.set_center(True, True)
    menu.set_alignment('center', 'center')

    # state variables for the finite state machine menu
    state = 0
    prev_state = 1

    # ignore mouse and only update certain rects for efficiency
    pygame.event.set_blocked(pygame.MOUSEMOTION)
    rect_list = []

    while 1:
        # check if the state has changed, if it has, then post a user event to
        # the queue to force the menu to be shown at least once
        if prev_state != state:
            pygame.event.post(pygame.event.Event(EVENT_CHANGE_STATE, key = 0))
            prev_state = state

        # get the next event
        e = pygame.event.wait()

        # update the menu
        if e.type == pygame.KEYDOWN or e.type == EVENT_CHANGE_STATE:
            if state == 0:
                # "default" state
                rect_list, state = menu.update(e, state)
            elif state == 1:
                # start the game
                event_loop()
            elif state == 2:
                # just to demonstrate how to make other options
                pygame.display.set_caption("y u touch this")
                state = 0
            else:
                # exit the game and program
                pygame.quit()
                sys.exit()

            # quit if the user closes the window
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # update the screen
            pygame.display.update(rect_list)

if __name__ == '__main__':
    main()