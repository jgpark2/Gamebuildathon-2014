import pygame
import sys
import os
from menu import *

background = pygame.image.load(os.path.join('images', 'floor.png'))

"""
Sprites from: http://untamed.wild-refuge.net/rmxpresources.php?characters
"""

class Player(pygame.sprite.Sprite):
    # constructor for this class
    def __init__(self):
        # call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        # create 50px by 50px surface
        self.image = pygame.Surface((16, 16))
        # color the surface cyan
        #self.image.fill((0, 205, 205))
        self.images = []
        self.images.append(pygame.image.load(os.path.join('images', 'p_west.png')))
        self.images.append(pygame.image.load(os.path.join('images', 'p_north.png')))
        self.images.append(pygame.image.load(os.path.join('images', 'p_east.png')))
        self.images.append(pygame.image.load(os.path.join('images', 'p_south.png')))

        self.image = self.images[1]
        self.rect = self.image.get_rect()
        self.speed = [0, 0]
        self.dir=1

        self.hasStolen = False
        '''
         1
        0 2
         3
        '''
        #initialize inventory, this is reset at the beginning of each level
        self.inventory = { 'clothing' : 0 ,'drink' : 0, 'food' : 0, 'game':0, 'medicine':0, 'soap':0 }

    def left(self):
        self.speed[1]=0
        self.speed[0] = -4
        self.image = self.images[0]
        self.dir=0

    def right(self):
        self.speed[1]=0
        self.speed[0] = 4
        self.image = self.images[2]
        self.dir=2

    def up(self):
        self.speed[0]=0
        self.speed[1] = -4
        self.image = self.images[1]
        self.dir=1

    def down(self):
        self.speed[0]=0
        self.speed[1] = 4
        self.image = self.images[3]
        self.dir=3

    def move(self):
        # move the rect by the displacement ("speed")
        self.rect = self.rect.move(self.speed)
        
    def steal(self, type):
        self.inventory[type]+=1
        return

class Aisle(pygame.sprite.Sprite):
    def __init__(self, spr, type):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((250, 40))
        self.image = pygame.image.load(os.path.join('images', spr))
        self.rect = self.image.get_rect()
        self.speed = [0, 0]
        self.type = type

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


class Door(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((80, 30))
        self.image = pygame.image.load(os.path.join('images', 'entrance.png'))
        self.rect = self.image.get_rect()

class Employee(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # load the PNG
        self.images = []
        self.images.append(pygame.image.load(os.path.join('images', 'e_west.png')))
        self.images.append(pygame.image.load(os.path.join('images', 'e_north.png')))
        self.images.append(pygame.image.load(os.path.join('images', 'e_east.png')))
        self.images.append(pygame.image.load(os.path.join('images', 'e_south.png')))
        self.image = self.images[2]
        self.rect = self.image.get_rect()

    def move(self):
        self.rect = self.rect.move(self.speed)

    def dir_x(self):
        return 1 if self.speed[0] > 0 else -1

    def dir_y(self):
        return 1 if self.speed[1] > 0 else -1

    def detectCaught(self, thief):
        dx = self.speed[0]
        dy = self.speed[1]

        if thief.hasStolen:
            if thief.rect.centerx == self.rect.centerx:
                if thief.rect.centery > self.rect.centery and dy > 0 and thief.rect.centery-self.rect.centery<=200:
                    return True
                elif thief.rect.centery < self.rect.centery and dy < 0 and self.rect.centery-thief.rect.centery<=200:
                    return True
            elif thief.rect.centery == self.rect.centery:
                if thief.rect.centerx > self.rect.centerx and dx > 0 and thief.rect.centerx-self.rect.centerx<=200:
                    return True
                elif thief.rect.centerx < self.rect.centerx and dx < 0 and self.rect.centerx-thief.rect.centerx <=200:
                    return True

        return False

    def left(self):
        self.speed[1]=0
        self.speed[0] = -4
        self.image = self.images[0]

    def right(self):
        self.speed[1]=0
        self.speed[0] = 4
        self.image = self.images[2]

    def up(self):
        self.speed[0]=0
        self.speed[1] = -4
        self.image = self.images[1]

    def down(self):
        self.speed[0]=0
        self.speed[1] = 4
        self.image = self.images[3]

def event_loop():
    pygame.display.set_caption("Do You Even Lift?")
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
    player.rect.topleft = 340-80/2, 480-30

    #name, hunger, thirst, heat, clean, sick, health
    families = []
    mother = Family("Mother-in-Law", 6, 2, 5, 3, 0, 5)
    wife = Family("Wife", 8, 2, 5, 5, 0, 5)
    son = Family("Son", 7, 2, 5, 4, 0, 3)
    dog = Family("Fido", 5, 2, 7, 4, 0, 4)

    #Employees (enemies)
    enemy_list=pygame.sprite.Group()
    emp1 = Employee()
    emp1.rect.bottomleft = 0, screen_height
    emp1.speed = [4, 0]
    enemy_list.add(emp1)

    aisles = []
    spr = ['aisle_cloth.png','aisle_drink.png','aisle_food.png','aisle_game.png','aisle_med.png','aisle_soap.png']
    type = ['clothing','drink','food','game','medicine','soap']
    for i in range(0, 3):
        aisle1 = Aisle(spr[i], type[i])
        aisle2 = Aisle(spr[3+i], type[3+i])
        offset = i*screen_height/4
        aisle1.rect.topleft = 40, (20+offset+40)
        aisle2.rect.topright = (screen_width-40), (20+offset+40)
        aisles.append(aisle1)
        aisles.append(aisle2)

    entrance = Door()
    entrance.rect.topleft = 340-80/2, 480-30
    
    # create a sprite group for the player and enemy
    # so we can draw to the screen
    sprite_list = pygame.sprite.Group()
    sprite_list.add(player)
    # sprite_list.add(enemy)
    for aisle in aisles:
        sprite_list.add(aisle)

    # create a sprite group for enemies only to detect collisions
    
    door_list = pygame.sprite.Group()
    door_list.add(entrance)

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
                    
                    if event.key == pygame.K_SPACE and player.dir==1:
                        player.hasStolen = True

                        # Find which aisle you are stealing from
                        for aisle in aisles:
                            if aisle.rect.collidepoint(player.rect.centerx, player.rect.centery-16-2):
                                print "stealing..." +aisle.type
                                player.steal(aisle.type)
                    elif event.key == pygame.K_SPACE and pygame.sprite.spritecollide(player, door_list, False):
                        game_state=1
                        
                
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
                    enemy.up()
                if enemy.rect.right > screen_width:
                    enemy.rect.right = screen_width
                    enemy.left()
                if enemy.rect.top < 0:
                    enemy.rect.top = 0
                    enemy.down()
                if enemy.rect.bottom > screen_height:
                    enemy.rect.bottom = screen_height
                    enemy.right()

                # Collision detection for aisles.
                for aisle in aisles:
                    aisle.detectCollision(enemy)

                enemy.move()

                if enemy.detectCaught(player):
                    game_state = 3
            
            # draw the player and enemy sprites to the screen
            door_list.draw(screen)
            sprite_list.draw(screen)
            enemy_list.draw(screen)
            
            # set up the score text
            text = basicFont.render('Day: %d' % game_day, True, (255, 255, 255))
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
            if frame_count>60*10: #7200:
                game_state=1
            clock.tick(frame_rate)
            
        elif game_state==1: #Days over Results Screen
            # handle input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        print "next day"
                        game_state=0
                        #reset inventory
                        player.inventory = { 'clothing' : 0 ,'drink' : 0, 'food' : 0, 'game':0, 'medicine':0, 'soap':0 }
                        frame_count=0
                        game_day+=1
                        player.speed=[0,0]
                        player.rect.topleft = 340-80/2, 480-30
                    
            # black background
            screen.fill((0, 0, 0))
            
            white = (255,255,255)
            screen.blit(basicFont.render('DAY %d RESULTS:' % game_day, True, white),[280,70])
            screen.blit(basicFont.render('Score: %d' % score, True, white), [0,0])
            screen.blit(basicFont.render('Press SPACE to continue', True, white),[280,400])
            
            #list of stolen items
            screen.blit(basicFont.render("Inventory:",True, white), [120,100])
            i=1
            for item, count in player.inventory.iteritems():
                screen.blit(basicFont.render(item+" x%d" % count, True, white), [120,100+16*i])
                i+=1
            
            famsize = len(families)
            for thing in families:
                thing.hunger = max(min(thing.mhunger, thing.hunger + (player.inventory["food"]/famsize)) - 1, 0)
                thing.thirst = max(min(thing.mthirst, thing.thirst + (player.inventory["drink"]/famsize)) - 1, 0)
                thing.heat = max(min(thing.mheat, thing.heat + (player.inventory["clothing"]/famsize)) - 1, 0)
                thing.clean = max(min(thing.mclean, thing.clean + (player.inventory["soap"]/famsize)) - 1, 0)
                
                if thing.sick == 1:
                    if player.inventory["medicine"] > 0:
                        thing.sick = 0
                        player.inventory["medicine"] -= 1

                if thing.hunger == 0 or thing.thirst == 0 or thing.heat == 0 or thing.clean == 0:
                    thing.sick = 1

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

        # Game over
        elif game_state == 3:
            pygame.time.wait(1000)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            screen.fill((0, 0, 0))

            white = (255,255,255)

            gameovertext = pygame.font.SysFont(None, 50).render("Game Over", True, white)
            screen.blit(gameovertext, [screen_width/2- gameovertext.get_rect().width/2,100])

            dayssurvivedtext = pygame.font.SysFont(None, 30).render('Days survived: %d' % game_day, True, white)
            screen.blit(dayssurvivedtext, [screen_width/2- dayssurvivedtext.get_rect().width/2,140])

            pygame.display.flip()

def instructions_page():
    pygame.display.set_caption("Instructions")
    while 1:
        pygame.display.get_surface().fill((0,0,0))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    event_loop()
                elif event.key == pygame.K_BACKSPACE:
                    main_menu()

        instructions_text1 = "Steal items to help your hapless family."
        instructions_text2 = "Press SPACE in front of an aisle to steal from it."
        instructions_text3 = "Avoid the gaze of the guards."
        instructions_text4 = "The game is over if they see you."
        instructions_text5 = "The game is over if your family dies."
        instructions_text6 = "#YOLO"

        instructions1 = pygame.font.SysFont(None, 30).render(instructions_text1, True, (255,255,255))
        instructions2 = pygame.font.SysFont(None, 30).render(instructions_text2, True, (255,255,255))
        instructions3 = pygame.font.SysFont(None, 30).render(instructions_text3, True, (255,255,255))
        instructions4 = pygame.font.SysFont(None, 30).render(instructions_text4, True, (255,255,255))
        instructions5 = pygame.font.SysFont(None, 30).render(instructions_text5, True, (255,255,255))
        instructions6 = pygame.font.SysFont(None, 30).render(instructions_text6, True, (255,255,255))

        screen2 = pygame.display.get_surface()
        screen2.blit(instructions1, [10, 10])
        screen2.blit(instructions2, [10, 40])
        screen2.blit(instructions3, [10, 70])
        screen2.blit(instructions4, [10, 100])
        screen2.blit(instructions5, [10, 130])
        screen2.blit(instructions6, [10, 170])

        act1 = pygame.font.SysFont(None, 20).render("Press SPACE to start game.", True, (255,255,255))
        act2 = pygame.font.SysFont(None, 20).render("Press BACKSPACE to go back to the menu.", True, (255,255,255))

        screen2.blit(act1, [10, 230])
        screen2.blit(act2, [10, 250])
        pygame.display.flip()

def main_menu():
    # set the window title
    pygame.display.set_caption("Do You Even Lift?")
    pygame.display.get_surface().fill((0,0,0))
    titletext = pygame.font.SysFont(None, 32).render("Do You Even Lift?", True, (255,255,255))
    screen = pygame.display.get_surface()
    screen.blit(titletext, [640/2 - titletext.get_rect().width/2,100])
    
    # create the menu
    menu = cMenu(50, 50, 20, 5, 'vertical', 100, screen,
                 [('Start Game',   1, None),
                  ('Instructions', 2, None),
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
                #pygame.display.set_caption("y u touch this")
                instructions_page()

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

def main():
    # initialize pygame
    pygame.init()

    # create the window
    size = width, height = 640, 480
    screen = pygame.display.set_mode(size)
    main_menu()

if __name__ == '__main__':
    main()