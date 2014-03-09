

def game():
        
    import pygame
    import os
    import random
    import math


    numb = 0
    pygame.init()
    screen=pygame.display.set_mode((800,800))
    FRICTION =25
    GRAD = math.pi / 180
    chance = 1   
    
    #define sprite groups
    birdgroup = pygame.sprite.LayeredUpdates()   
    bargroup = pygame.sprite.Group()
    stuffgroup = pygame.sprite.Group()
    holegroup = pygame.sprite.Group()
    # LayeredUpdates instead of group to draw in correct order
    allgroup = pygame.sprite.LayeredUpdates() # more sophisticated than simple group

    def draw():
        a=screen.get_width()/2
        b=screen.get_height()/2
        Hole((0,0))
        Hole((a*2-60,0))
        Hole((0,b*2-60))
        Hole((a*2-60,b*2-60))
        if numb == 0:      
            Goti()
        elif numb == 1:
            Bird((a,b))
        elif numb == 2:
            Bird((a - 55,b))
        elif numb == 3:
            Bird((a + 55,b))
        elif numb == 4:
            Bird((a + 30,b + 45))
        elif numb == 5:
            Bird((a - 30,b + 45))
        elif numb == 6:
            Bird((a + 30,b - 45))
        elif numb == 7:
            Bird((a - 30,b - 45))
        elif numb == 8:
            Bird((a - 110,b ))
        elif numb == 9:
            Bird((a - 80,b + 45 ))
        elif numb == 10:
            Bird((a + 110,b ))
        elif numb == 11:
            Bird((a + 80,b + 45 ))
        elif numb == 12:
            Bird((a - 80,b - 45 ))
        elif numb == 13:
            Bird((a + 80,b - 45 ))
        elif numb == 14:
            Bird((a ,b - 100 ))
        elif numb == 15:
            Bird((a - 55,b - 100 ))
        elif numb == 16:
            Bird((a + 55,b - 100))
        elif numb == 17:
            Bird((a ,b + 100 ))
        elif numb == 18:
            Bird((a + 55,b + 100 ))
        elif numb == 19:
            Bird((a - 55,b + 100))


    def elastic_collision(sprite1, sprite2):
        """elasitc collision between 2 sprites (calculated as disc's).
           The function alters the dx and dy movement vectors of both sprites.
           The sprites need the property .mass, .radius, .pos[0], .pos[1], .dx, dy
           pos[0] is the x postion, pos[1] the y position"""
        # here we do some physics: the elastic
        # collision
        #
        # first we get the direction of the push.
        # Let's assume that the sprites are disk
        # shaped, so the direction of the force is
        # the direction of the distance.
        dirx = sprite1.pos[0] - sprite2.pos[0]
        diry = sprite1.pos[1] - sprite2.pos[1]
        #
        # the velocity of the centre of mass
        sumofmasses = sprite1.mass + sprite2.mass
        sx = (sprite1.dx * sprite1.mass + sprite2.dx * sprite2.mass) / sumofmasses
        sy = (sprite1.dy * sprite1.mass + sprite2.dy * sprite2.mass) / sumofmasses
        # if we sutract the velocity of the centre
        # of mass from the velocity of the sprite,
        # we get it's velocity relative to the
        # centre of mass. And relative to the
        # centre of mass, it looks just like the
        # sprite is hitting a mirror.
        #
        bdxs = sprite2.dx - sx
        bdys = sprite2.dy - sy
        cbdxs = sprite1.dx - sx
        cbdys = sprite1.dy - sy
        # (dirx,diry) is perpendicular to the mirror
        # surface. We use the dot product to
        # project to that direction.
        distancesquare = dirx * dirx + diry * diry
        if distancesquare == 0:
            # no distance? this should not happen,
            # but just in case, we choose a random
            # direction
            dirx = random.randint(0,11) - 5.5
            diry = random.randint(0,11) - 5.5
            distancesquare = dirx * dirx + diry * diry
        dp = (bdxs * dirx + bdys * diry) # scalar product
        dp /= distancesquare # divide by distance * distance.
        cdp = (cbdxs * dirx + cbdys * diry)
        cdp /= distancesquare
        # We are done. (dirx * dp, diry * dp) is
        # the projection of the velocity
        # perpendicular to the virtual mirror
        # surface. Subtract it twice to get the
        # new direction.
        #
        # Only collide if the sprites are moving
        # towards each other: dp > 0
        if dp > 0:
            sprite2.dx -= 2 * dirx * dp 
            sprite2.dy -= 2 * diry * dp
            sprite1.dx -= 2 * dirx * cdp 
            sprite1.dy -= 2 * diry * cdp


    class BirdCatcher(pygame.sprite.Sprite):
        """circle around the mouse pointer. Left button create new sprite, right button kill sprite"""
        def __init__(self):
            pygame.sprite.Sprite.__init__(self, self.groups)
            self.image = pygame.Surface((100,100)) # created on the fly
            self.image.set_colorkey((0,0,0)) # black transparent
            pygame.draw.circle(self.image, (255,0,0), (50,50), 50, 2) # red circle
            self.image = self.image.convert_alpha()
            self.rect = self.image.get_rect()
            self.radius = 50 # for collide check

        def update(self, seconds):
            # no need for seconds but the other sprites need it
            self.rect.center = pygame.mouse.get_pos()


            
    class Hole(pygame.sprite.Sprite):
        """shows a bar as long as how much milliseconds are passed between two frames"""
        def __init__(self, pos=screen.get_rect().center):
            pygame.sprite.Sprite.__init__(self, self.groups)
            self.pos=pos
            self.holesurface=pygame.Surface((60, 60))
	    self.holesurface.set_colorkey((0,0,0))
            pygame.draw.circle(self.holesurface, (250,100,81), (30,30),30) # paint blue circle
            self.holesurface = self.holesurface.convert_alpha()       # if you use tranparent colors you need convert_alpha()
            self.image = self.holesurface
            self.rect = self.image.get_rect()            
        
        def update(self, time):
            screen.blit(self.holesurface, self.pos)   

            

    class Bird(pygame.sprite.Sprite):
        """a nice little sprite that bounce off walls and other sprites"""
        #image=[]
        # not necessary:
        birds = {} # a dictionary of all Birds, each Bird has its own number
        number = 0  
        def __init__(self, startpos=screen.get_rect().center):
            pygame.sprite.Sprite.__init__(self,  self.groups ) #call parent class. NEVER FORGET !
            
            self.ballsurface=pygame.Surface((50, 50))
	    self.ballsurface.set_colorkey((0,0,0))
            if(Bird.number == 1):
                pygame.draw.circle(self.ballsurface, (255,0,0), (25,25),25)
            elif(Bird.number % 2 ==0):
                pygame.draw.circle(self.ballsurface, (100,175,81), (25,25),25)
            else:
                pygame.draw.circle(self.ballsurface, (200,75,181), (25,25),25)                
            self.ballsurface = self.ballsurface.convert_alpha()       # if you use tranparent colors you need convert_alpha()
            self.pos = [0,0] # dummy values to create a list
            self.pos[0] = float(startpos[0]) # float for more precise calculation
            self.pos[1] = float(startpos[1])
            self.area = screen.get_rect()
            self.image = self.ballsurface
            #self.hitpointsfull = float(HITPOINTS) # maximal hitpoints , float makes decimal
            #self.hitpoints = float(HITPOINTS) # actual hitpoints
            self.rect = self.image.get_rect()
            self.radius = 25 # this to we can set according to size of our goti
            self.dx=0
            self.dy=0            
            self.catched = False
            self.mass = 40
            self.number = Bird.number # get my personal Birdnumber
            Bird.number+= 1           # increase the number for next Bird
            Bird.birds[self.number] = self # store myself into the Bird dictionary

            

        def update(self, seconds):
            # friction make birds slower
            k=self.dx
            self.dx=self.dx-FRICTION*seconds*self.dx*0.01
            kk=self.dx
            if(kk*k<=0):
                self.dx=0
            if(self.dx>100):
                self.dx=100
            l=self.dy
            self.dy=self.dy-FRICTION*seconds*self.dy*0.01
            ll=self.dy
            if(ll*l<=0):
                self.dy=0
            if(self.dy>100):
                self.dy=100
            
            self.pos[0] += self.dx * seconds
            self.pos[1] += self.dy * seconds
            if(self.pos[0]<50 and self.pos[1]<50):
                self.kill()
            elif(self.pos[0]<50 and self.pos[1]>(screen.get_height()-50)):
                self.kill()
            elif(self.pos[0]>(screen.get_width()-50) and self.pos[1]<50):
                self.kill()
            elif(self.pos[0]>(screen.get_height()-50) and self.pos[1]>(screen.get_height()-50)):
                self.kill()
            # -- check if Bird out of screen
            self.areacheck()
            #--- calculate new position on screen -----
            self.rect.centerx = round(self.pos[0],0)
            self.rect.centery = round(self.pos[1],0)


        def areacheck(self):
            if not self.area.contains(self.rect):
                # --- compare self.rect and area.rect
                if self.pos[0] + self.rect.width/2 > self.area.right:
                    self.pos[0] = self.area.right - self.rect.width/2
                    self.dx=self.dx*-1
                if self.pos[0] - self.rect.width/2 < self.area.left:
                    self.pos[0] = self.area.left + self.rect.width/2
                    self.dx=self.dx*-1
                if self.pos[1] + self.rect.height/2 > self.area.bottom:
                    self.pos[1] = self.area.bottom - self.rect.height/2
                    self.dy=self.dy*-1
                if self.pos[1] - self.rect.height/2 < self.area.top:
                    self.pos[1] = self.area.top + self.rect.height/2
                    self.dy=self.dy*-1


    class Goti(Bird):
        def __init__(self, startpos=screen.get_rect().center):
            Bird.__init__(self)
            self.image = pygame.Surface((80,80)) # created on the fly
            self.image.set_colorkey((0,0,0)) # black transparent
            pygame.draw.circle(self.image, (105,105,0), (40,40), 40) # red circle
            pygame.draw.circle(self.image, (10,105,50), (35,0), 5)
            self.image = self.image.convert_alpha()
            self.pos = [0,0] # dummy values to create a list
            self.pos[0] = float(startpos[0]) # float for more precise calculation
            self.pos[1] = float(startpos[1]-200)
            self.rect = self.image.get_rect()
            self.radius = 40 # for collide check
            self.angle = 0.0
            self.speed = 20.0
            self.rotatespeed = 1.0
            self.nimage = self.image # 0 for not crashing, 2 for big
            self.sp = 40
            self.mass=60

        def update(self, time):

                k=self.dx
                self.dx=self.dx-FRICTION*seconds*self.dx*0.01
                kk=self.dx
                if(kk*k<=0):
                    self.dx=0
                if(self.dx>100):
                    self.dx=100
                l=self.dy
                self.dy=self.dy-FRICTION*seconds*self.dy*0.01
                ll=self.dy
                if(ll*l<=0):
                    self.dy=0
                if(self.dy>100):
                    self.dy=100

                if self.dx==0 and self.dy==0 :
                    self.pos[0]=400
                    self.pos[1]=600


                pygame.display.set_caption("SPEED : %i" % (self.sp))      #sp is used for setting the initial speed of stricker
                pressedkeys = pygame.key.get_pressed()


                self.ddx = 0.0
                self.ddy = 0.0
                if pressedkeys[pygame.K_w]: # forward
                         self.dx = self.sp
                         self.ddx = -math.sin(self.angle*GRAD) 
                         self.ddy = -math.cos(self.angle*GRAD) 
                if pressedkeys[pygame.K_s]: # backward
                         self.ddx = +math.sin(self.angle*GRAD) 
                         self.ddy = +math.cos(self.angle*GRAD) 
                if pressedkeys[pygame.K_e]: # right side
                         self.ddx = +math.cos(self.angle*GRAD)
                         self.ddy = -math.sin(self.angle*GRAD)
                if pressedkeys[pygame.K_q]: # left side
                         self.ddx = -math.cos(self.angle*GRAD) 
                         self.ddy = +math.sin(self.angle*GRAD) 

                if pressedkeys[pygame.K_KP_PLUS]:
                    self.sp += 1
                if pressedkeys[pygame.K_KP_MINUS]:
                    self.sp -= 1

                self.dx += self.ddx * self.speed
                self.dy += self.ddy * self.speed             
                self.pos[0] += self.dx * seconds
                self.pos[1] += self.dy * seconds
                # -- check if Bird out of screen
                self.areacheck()
                # ------------- rotate ------------------
                if pressedkeys[pygame.K_a]: # left turn , counterclockwise
                    self.angle += self.rotatespeed
                if pressedkeys[pygame.K_d]: # right turn, clockwise
                    self.angle -= self.rotatespeed
                self.oldcenter = self.rect.center
                self.image = pygame.transform.rotate(self.nimage, self.angle)
                self.rect = self.image.get_rect()
                self.rect.center = self.oldcenter
                #--- calculate new position on screen -----
                self.rect.centerx = round(self.pos[0],0)
                self.rect.centery = round(self.pos[1],0)


            

        
    background = pygame.Surface((screen.get_width(), screen.get_height()))
    background.fill((255,255,255))     # fill white

    screen.blit(background, (0,0))     # blit background on screen (overwriting all)


    #assign default groups to each sprite class
    # (only allgroup is useful at the moment)
    Hole.groups = holegroup, allgroup
    Bird.groups =  birdgroup, allgroup
    BirdCatcher.groups = stuffgroup, allgroup



    draw()  # one single Bird

    hunter = BirdCatcher() # display the BirdCatcher and name it "hunter"

    # set 
    millimax = 0
    othergroup =  [] # important for good collision detection
    badcoding = False
    clevercoding = False
    clock = pygame.time.Clock()        # create pygame clock object 
    mainloop = True
    FPS = 60                           # desired max. framerate in frames per second. 


    while mainloop:
        

        milliseconds = clock.tick(FPS)  # milliseconds passed since last frame
        if milliseconds > millimax:
            millimax = milliseconds
        seconds = milliseconds / 1000.0 # seconds passed since last frame

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mainloop = False # pygame window closed by user
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    numb += 1
                    draw()
                if event.key == pygame.K_ESCAPE:
                    mainloop = False # user pressed ESC
                elif event.key == pygame.K_z:
                    for bird in birdgroup:
                        if bird.number == 0:
                            if chance % 2 == 0:
                                bird.pos[0] = 400
                                bird.pos[1] = 700
                            else:
                                bird.pos[0] = 400
                                bird.pos[1] = 100
                            chance += 1
                    

        # create new Bird on mouseclick
        if pygame.mouse.get_pressed()[0]:
            #if not pygame.sprite.spritecollideany(hunter, birdgroup): 
                Bird(pygame.mouse.get_pos()) # create a new Bird at mousepos

        '''pygame.display.set_caption("ms: %i max(ms): %i fps: %.2f birds: %i gravity: %s bad:%s clever:%s"% (milliseconds, 
                                    millimax, clock.get_fps(), len(birdgroup), Fragment.gravity, badcoding, clevercoding))'''
        
        # ------ collision detecttion
        
        # test if a bird collides with another bird
        for bird in birdgroup:

                othergroup[:] = birdgroup.sprites()  #group of all birds
                othergroup.remove(bird) # remove the actual bird, only all other birds remain
                if pygame.sprite.spritecollideany(bird, othergroup):                     
                    crashgroup = pygame.sprite.spritecollide(bird, othergroup, False, pygame.sprite.collide_mask )
                    for crashbird in crashgroup:
                        bird.crashing = True
                        elastic_collision(crashbird, bird)                        

                    
        # ----------- clear, draw , update, flip -----------------  
        allgroup.clear(screen, background)
        allgroup.update(seconds)
        allgroup.draw(screen)           
        pygame.display.flip()         

if __name__ == "__main__":
    game()
