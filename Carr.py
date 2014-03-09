

def game():
        
    import pygame
    import os
    import random
    import time
    import math


    #pygame.mixer.pre_init(44100, -16, 2, 2048) # setup mixer to avoid sound lag
    pygame.init()
    screen=pygame.display.set_mode((800,800)) # try out larger values and see what happens !
    #winstyle = 0  # |FULLSCREEN # Set the display mode
    BIRDSPEEDMAX = 200
    BIRDSPEEDMIN = 0
    FRICTION =50
    GRAD = math.pi / 180 # 2 * pi / 360   # math module needs Radiant instead of Grad
    #HITPOINTS = 100.0 
    #FORCE_OF_GRAVITY = 9.81 # in pixel per second .#See http://en.wikipedia.org/wiki/Gravitational_acceleration
    #print pygame.ver 
    '''def write(msg="pygame is cool"):
        """write text into pygame surfaces"""
        myfont = pygame.font.SysFont("None", 32)
        mytext = myfont.render(msg, True, (0,0,0))
        mytext = mytext.convert_alpha()
        return mytext'''
    
    #define sprite groups
    birdgroup = pygame.sprite.LayeredUpdates()   
    bargroup = pygame.sprite.Group()
    stuffgroup = pygame.sprite.Group()
    holegroup = pygame.sprite.Group()
    strikegroup = pygame.sprite.Group()
    # LayeredUpdates instead of group to draw in correct order
    allgroup = pygame.sprite.LayeredUpdates() # more sophisticated than simple group

    def make():
        Bird((screen.get_width()/2, screen.get_height()/2))
        #time.sleep(5)
        Bird((100, 300))
        #Bird((700, 200))
        #Bird((700, 300))
        #Bird((700, 500))

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


    '''class Striker(Bird):
        """circle around the mouse pointer. Left button create new sprite, right button kill sprite"""
        def __init__(self, startpos=screen.get_rect().center):
            Bird.__init__(self)
            self.image = pygame.Surface((60,60)) # created on the fly
            self.image.set_colorkey((0,0,0)) # black transparent
            pygame.draw.circle(self.image, (0,255,255), (30,30), 30)
            pygame.draw.circle(self.image, (200, 100, 150), (10, 10), 5 ) 
            self.image = self.image.convert_alpha()
            self.angle=0
            self.radius = 30 # for collide check
            self.pos=[0.0, 0.0]
            self.pos[0] = float(startpos[0]) # float for more precise calculation
            self.pos[1] = float(startpos[1])
            self.dx=0
            self.dy=0
            self.rotatespeed = 1.0 # rotating speed
            self.rect = self.image.get_rect()

        def update(self, time):
                screen.blit(self.image, self.pos)
                pressedkeys = pygame.key.get_pressed()
                self.ddx = 0.0
                self.ddy = 0.0
                if pressedkeys[pygame.K_w]: # forward
                         self.ddx = -math.sin(self.angle*GRAD) 
                         self.ddy = -math.cos(self.angle*GRAD) 
                         #Smoke(self.rect.center, -self.ddx , -self.ddy )
                if pressedkeys[pygame.K_s]: # backward
                         self.ddx = +math.sin(self.angle*GRAD) 
                         self.ddy = +math.cos(self.angle*GRAD) 
                         #Smoke(self.rect.center, -self.ddx, -self.ddy )
                if pressedkeys[pygame.K_e]: # right side
                         self.ddx = +math.cos(self.angle*GRAD)
                         self.ddy = -math.sin(self.angle*GRAD)
                         #Smoke(self.rect.center, -self.ddx , -self.ddy )
                if pressedkeys[pygame.K_q]: # left side
                         self.ddx = -math.cos(self.angle*GRAD) 
                         self.ddy = +math.sin(self.angle*GRAD) 
                         #Smoke(self.rect.center, -self.ddx , -self.ddy )
                # ------------shoot-----------------
                if self.cooldown > 0:
                    self.cooldown -= time 
                else:
                    if pressedkeys[pygame.K_SPACE]: # shoot forward
                        self.ddx = +math.sin(self.angle*GRAD)#recoil
                        self.ddy = +math.cos(self.angle*GRAD)
                        lasersound.play() # play sound
                        self.shots += 1
                        Bullet(self, -math.sin(self.angle*GRAD) ,
                               -math.cos(self.angle*GRAD) )
                    self.cooldown = self.cooldowntime
                # ------------move------------------
                if not self.waiting:
                    self.dx += self.ddx * self.speed
                    self.dy += self.ddy * self.speed
                #self.speedcheck()   # friction, maxspeed             
                self.pos[0] += self.dx * seconds
                self.pos[1] += self.dy * seconds
                # -- check if Bird out of screen
                self.areacheck()
                ------------- rotate ------------------
                if pressedkeys[pygame.K_a]: # left turn , counterclockwise
                    self.angle += self.rotatespeed
                if pressedkeys[pygame.K_d]: # right turn, clockwise
                    self.angle -= self.rotatespeed
                self.oldcenter = self.rect.center
                self.image = pygame.transform.rotate(self.image, self.angle)
                self.rect = self.image.get_rect()
                self.rect.center = self.oldcenter
                #--- calculate new position on screen -----
                self.rect.centerx = round(self.pos[0],0)
                self.rect.centery = round(self.pos[1],0)
                #if self.hitpoints <= 0: # ----- alive---- 
                #    self.kill()

    class Fragment(pygame.sprite.Sprite):
        """a fragment of an exploding Bird"""
        gravity = True # fragments fall down ?
        def __init__(self, pos):
            pygame.sprite.Sprite.__init__(self, self.groups)
            self.pos = [0.0,0.0]
            self.pos[0] = pos[0]
            self.pos[1] = pos[1]
            self.image = pygame.Surface((10,10))
            self.image.set_colorkey((0,0,0)) # black transparent
            pygame.draw.circle(self.image, (random.randint(1,64),0,0), (5,5), 
                                            random.randint(2,5))
            self.image = self.image.convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.center = self.pos #if you forget this line the sprite sit in the topleft corner
            self.lifetime = 1 + random.random()*5 # max 6 seconds
            self.time = 0.0
            self.fragmentmaxspeed = BIRDSPEEDMAX * 2 # try out other factors !
            self.dx = random.randint(-self.fragmentmaxspeed,self.fragmentmaxspeed)
            self.dy = random.randint(-self.fragmentmaxspeed,self.fragmentmaxspeed)
            
        def update(self, seconds):
            self.time += seconds
            if self.time > self.lifetime:
                self.kill() 
            self.pos[0] += self.dx * seconds
            self.pos[1] += self.dy * seconds
            if Fragment.gravity:
                self.dy += FORCE_OF_GRAVITY # gravity suck fragments down
            self.rect.centerx = round(self.pos[0],0)
            self.rect.centery = round(self.pos[1],0)'''
            
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
    '''class Hole(pygame.sprite.Sprite):
        def __init__(self, number=3):
            pygame.sprite.Sprite.__init__(self,self.groups)
            self.pos=(0.0,0.0)
            self.holesurface=pygame.Surface((60, 60))
	    self.holesurface.set_colorkey((0,0,0))
            pygame.draw.circle(self.holesurface, (250,100,81), (30,30),30) # paint blue circle
            self.holesurface = self.holesurface.convert_alpha()       # if you use tranparent colors you need convert_alpha()
            self.image = self.holesurface
            self.rect = self.image.get_rect()
            #self.number = number # the unique number (name) of hole
        def update(self, time):
            screen.blit(self.holesurface, self.pos)'''
            

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
            if(Bird.number == 0):
                pygame.draw.circle(self.ballsurface, (255,0,0), (25,25),25)
            elif(Bird.number % 2 ==0):
                pygame.draw.circle(self.ballsurface, (50,255,100), (25,25),25)
            else:
                pygame.draw.circle(self.ballsurface, (200,75,181), (25,25),25)                
            self.ballsurface = self.ballsurface.convert_alpha()       # if you use tranparent colors you need convert_alpha()
            #self.ballrect = self.ballsurface.get_rect() # the rectangle of the ball surface, for collision detection
            #self.ballx, self.bally = 550, 240             



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
            #self.newspeed()
            #self.cleanstatus()
            self.catched = False
            #self.crashing = False
            #--- not necessary:
            self.number = Bird.number # get my personal Birdnumber
            Bird.number+= 1           # increase the number for next Bird
            Bird.birds[self.number] = self # store myself into the Bird dictionary
            #print "my number %i Bird number %i " % (self.number, Bird.number)
            #Livebar(self) #create a Livebar for this Bird. 
            
        '''def newspeed(self):
            # new birdspeed, but not 0
            speedrandom = random.choice([-1,1]) # flip a coin
	    #self.dx = 100
            self.dx = random.random() * BIRDSPEEDMAX * speedrandom + speedrandom 
	    #self.dy = 80
            self.dy = random.random() * BIRDSPEEDMAX * speedrandom + speedrandom '''
            
        '''def kill(self):
            """because i want to do some special effects (sound, dictionary etc.)
            before killing the Bird sprite i have to write my own kill(self)
            function and finally call pygame.sprite.Sprite.kill(self) 
            to do the 'real' killing"""
            cry.play()
            #print Bird.birds, "..."
            for _ in range(random.randint(3,15)):
                Fragment(self.pos)
            Bird.birds[self.number] = None # kill Bird in sprite dictionary
            pygame.sprite.Sprite.kill(self) # kill the actual Bird '''

        '''def cleanstatus(self):
            self.catched = False   # set all Bird sprites to not catched
            self.crashing = False'''

        def update(self, seconds):
            # friction make birds slower
            k=self.dx
            self.dx=self.dx-FRICTION*seconds
            kk=self.dx
            if(kk*k<=0):
                self.dx=0
            elif(self.dx>100):
                self.dx=100
            l=self.dy
            self.dy=self.dy-FRICTION*seconds
            ll=self.dy
            if(ll*l<=0):
                self.dy=0
            elif(self.dy>100):
                self.dy=100
            '''if abs(self.dx) > BIRDSPEEDMIN and abs(self.dy) > BIRDSPEEDMIN:
                self.dx *= FRICTION
                self.dy *= FRICTION
            # spped limit
            if abs(self.dx) > BIRDSPEEDMAX:
                self.dx = BIRDSPEEDMAX * self.dx / self.dx
            if abs(self.dy) > BIRDSPEEDMAX:
                self.dy = BIRDSPEEDMAX * self.dy / self.dy'''
            # new position
            
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
            if not self.area.contains(self.rect):
                #self.crashing = True # change colour later
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
            '''else:
                if self.catched:
                    self.kill() # blue rectangle'''

                #self.newspeed() # calculate a new direction
            #--- calculate actual image: crasing, catched, both, nothing ?
            #self.image = Bird.image[self.crashing + self.catched*2]
            #--- calculate new position on screen -----
            self.rect.centerx = round(self.pos[0],0)
            self.rect.centery = round(self.pos[1],0)
            #--- loose hitpoins
            '''if self.crashing:
                self.hitpoints -=1'''
            #--- check if still alive
            '''if self.hitpoints <= 0:
                self.kill()'''

        
    background = pygame.Surface((screen.get_width(), screen.get_height()))
    background.fill((255,255,255))     # fill white
    #Hole((screen.get_width()-30,30),2)
    #Hole((30,screen.get_height()-30),3)
    #Hole((screen.get_width()-30,screen.get_height()-30),4)
    #pygame.draw.circle(background, (243,50,81), (screen.get_width()-30,30),30)
    #pygame.draw.circle(background, (243,50,81), (30,screen.get_height()-30),30)
    #pygame.draw.circle(background, (243,50,81), (screen.get_width()-30,screen.get_height()-30),30)    
    '''background.blit(write("press left mouse button for more sprites."),(150,10))
    background.blit(write("press right mouse button to kill sprites."),(150,40))
    background.blit(write("press g to toggle gravity"),(150,70))
    background.blit(write("press b to toggle bad coding"),(150,100))
    background.blit(write("press c to toggle clever coding"), (150,130))
    background.blit(write("Press ESC to quit"), (150,160))'''

    # paint vertical lines to measure passed time (Timebar)
    #for x in range(0,screen.get_width()+1,20):
    '''for x in range(0,140,20):
        pygame.draw.line(background, (255,0,255), (x,0) ,(x,screen.get_height()), 1)
    background = background.convert()  # jpg can not have transparency'''
    screen.blit(background, (0,0))     # blit background on screen (overwriting all)


    #assign default groups to each sprite class
    # (only allgroup is useful at the moment)
    #Livebar.groups =  bargroup, allgroup 
    Hole.groups = holegroup, allgroup
    Bird.groups =  birdgroup, allgroup
    #Fragment.groups = fragmentgroup, allgroup
    BirdCatcher.groups = stuffgroup, allgroup
    Striker.groups = strikegroup, allgroup
    #assign default layer for each sprite (lower numer is background)
    BirdCatcher._layer = 5 # top foreground
    #Fragment._layer = 4
    #Timebar._layer = 3
    #Bird._layer = 2
    #Livebar._layer = 1




    # load images into classes (class variable !)
    '''try:
        Bird.image.append(pygame.image.load(os.path.join("data","Goti.png")))
        Bird.image.append(pygame.image.load(os.path.join("data","Goti.png")))
    except:
        raise UserWarning, "no image files 'babytux.png' and 'babytux_neg.png' in subfolder 'data'" '''
    #Bird.image.append(Bird.image[0].copy()) # copy of first image
    #pygame.draw.rect(Bird.image[2], (0,0,255), (0,0,32,36), 1) # blue border
    #Bird.image.append(Bird.image[1].copy()) # copy second image
    #pygame.draw.rect(Bird.image[3], (0,0,255), (0,0,32,36), 1) # blue border
    #Bird.image[0] = Bird.image[0].convert_alpha()
    #Bird.image[1] = Bird.image[1].convert_alpha()
    #Bird.image[2] = Bird.image[2].convert_alpha()
    #Bird.image[3] = Bird.image[3].convert_alpha()

    '''try:
        cry = pygame.mixer.Sound(os.path.join('data','claws.ogg'))  #load sound
    except:
        raise UserWarning, "could not load sound claws.ogg from 'data'"'''


   

    # at game start create a Bird and one BirdCatcher
    make()  # one single Bird
    Hole((0,0))
    Hole((screen.get_width()-60,0))
    Hole((0,screen.get_height()-60))
    Hole((screen.get_width()-60,screen.get_height()-60))
    hunter = BirdCatcher() # display the BirdCatcher and name it "hunter"
    Striker()

    # set 
    millimax = 0
    othergroup =  [] # important for good collision detection
    badcoding = False
    clevercoding = False
    clock = pygame.time.Clock()        # create pygame clock object 
    mainloop = True
    FPS = 60                           # desired max. framerate in frames per second. 
    


    '''for hole in holegroup:
        background.blit(hole.holesurface, hole.pos)
    for bird in birdgroup:
        screen.blit(bird.ballsurface, bird.pos)'''
    while mainloop:
        
        milliseconds = clock.tick(FPS)  # milliseconds passed since last frame
        #Timebar(milliseconds)
        if milliseconds > millimax:
            millimax = milliseconds
        seconds = milliseconds / 1000.0 # seconds passed since last frame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mainloop = False # pygame window closed by user
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    mainloop = False # user pressed ESC
                    '''elif event.key == pygame.K_g:
                    Fragment.gravity = not Fragment.gravity # toggle gravity class variable'''
                elif event.key == pygame.K_b:
                    if badcoding:
                        othergroup =  []  
                    badcoding = not badcoding
                    if badcoding: 
                        clevercoding = False
                elif event.key == pygame.K_c:
                    clevercoding = not clevercoding
                    if clevercoding:
                        badcoding = False
                elif event.key == pygame.K_p:
                    print "----------"
                    print "toplayer:", allgroup.get_top_layer()
                    print "bottomlayer:", allgroup.get_bottom_layer()
                    print "layers;", allgroup.layers()
                    

        # create new Bird on mouseclick
        if pygame.mouse.get_pressed()[0]:
            #if not pygame.sprite.spritecollideany(hunter, birdgroup): 
                Bird(pygame.mouse.get_pos()) # create a new Bird at mousepos
        if pygame.mouse.get_pressed()[2]:
            # kill sprites
            crashgroup = pygame.sprite.spritecollide(hunter, birdgroup, True, pygame.sprite.collide_mask)
        '''pygame.display.set_caption("ms: %i max(ms): %i fps: %.2f birds: %i gravity: %s bad:%s clever:%s"% (milliseconds, 
                                    millimax, clock.get_fps(), len(birdgroup), Fragment.gravity, badcoding, clevercoding))'''
        
        # ------ collision detecttion
        '''for bird in birdgroup:
            bird.cleanstatus()'''
        
        '''for hhole in holegroup:    
            #pygame.sprite.spritecollide(sprite, group, dokill, collided = None): return Sprite_list
            crashgroup = pygame.sprite.spritecollide(hhole, birdgroup, False, pygame.sprite.collide_circle)
            # pygame.sprite.collide_circle works only if one sprite has self.radius
            # you can do without that argument collided and only the self.rects will be checked
            for crashbird in crashgroup:
                crashbird.catched = True # will get a blue border from Bird.update()'''
                #crashbird.kill()   # this would remove him from all his groups
        
        # test if a bird collides with another bird
        for bird in birdgroup:
            if not clevercoding:
                if badcoding:
                    othergroup = birdgroup.copy() # WRONG ! THIS CODE MAKES UGLY TIME-CONSUMING GARBAGE COLLECTION !
                else:
                    othergroup[:] = birdgroup.sprites() # correct. no garbage collection
                othergroup.remove(bird) # remove the actual bird, only all other birds remain
                if pygame.sprite.spritecollideany(bird, othergroup): 
                    
                    crashgroup = pygame.sprite.spritecollide(bird, othergroup, False, pygame.sprite.collide_mask )
                    for crashbird in crashgroup:
                        bird.crashing = True
                        bird.dx -= crashbird.pos[0] - bird.pos[0]
                        bird.dy -= crashbird.pos[1] - bird.pos[1]
            else:
                # very clever coding
                crashgroup = pygame.sprite.spritecollide(bird, birdgroup, False)
                for crashbird in crashgroup:
                    if crashbird.number != bird.number: #avoid collision with itself
                        bird.crashing = True # make bird blue
                        bird.dx -= crashbird.pos[0] - bird.pos[0] # move bird away from other bird
                        bird.dy -= crashbird.pos[1] - bird.pos[1]
                    
        # ----------- clear, draw , update, flip ----------------- 
 
        allgroup.clear(screen, background)
        allgroup.update(seconds)
        #screen.blit(background,(0,0))
        '''for bird in birdgroup:
            screen.blit(bird.ballsurface, bird.pos)'''
        
        allgroup.draw(screen)   
        pygame.display.flip()         

if __name__ == "__main__":
    game()
