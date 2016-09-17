"""

"""
import sys, os, math, decimal, logging
import pygame
from pygame.locals import *
from ast import literal_eval

#game constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
TRACK_WIDTH = 4000
TRACK_HEIGHT = 4000
SHIP_ACCEL = 400 #accelerate 200 pixels per second
MAX_VEL = 450 #1.5 seconds to reach max velocity
TWOPLACES = decimal.Decimal(10) ** -2

#global logging
LOGEvent = logging.getLogger('SystemEvents')
LOGEvent.setLevel(logging.DEBUG)
LOGCrash = logging.getLogger('CrashReports')
LOGCrash.setLevel(logging.INFO)
LOGError = logging.getLogger('SystemErrors')
LOGError.setLevel(logging.WARNING)

FHEvent = logging.FileHandler('Logs/SystemEvents.log')
FHCrash = logging.FileHandler('Logs/CrashReports.log')
FHError = logging.FileHandler('Logs/SystemErrors.log')
FHEvent.setLevel(logging.DEBUG)
FHCrash.setLevel(logging.CRITICAL)
FHError.setLevel(logging.WARNING)

FMT = logging.Formatter('At %(asctime)s \n%(levelname)s: %(message)s')
FHEvent.setFormatter(FMT)
FHCrash.setFormatter(FMT)
FHError.setFormatter(FMT)

LOGEvent.addHandler(FHEvent)
LOGCrash.addHandler(FHCrash)
LOGError.addHandler(FHError)

#makes loading images easier
def load_image(name, colorkey=False):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', name
        raise SystemExit, message
    image = image.convert()
    if colorkey:
        if colorkey is -1: #colorkey = -1 will take the top left pixel
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image 

#makes loading sounds easier
def load_sound(name):
	fullname = os.path.join('data', name)
	try:
		sound = pygame.mixer.Sound(fullname)
	except pygame.error, message:
		print 'Cannot load sound:', name
		raise SystemExit, message
	return sound

#makes loading music easier
def load_music(name):
	fullname = os.path.join('data', name)
	try:
		pygame.mixer.music.load(fullname)
	except pygame.error, message:
		print 'Cannot load music:', name
		raise SystemExit, message

#makes drawing text to surface easier
def write(msg, size, color = (0,0,0), font="trebuchetms"):
	myfont = pygame.font.SysFont(font, size) 
	mytext = myfont.render(msg, True, color) #msg, antialias, color 
	mytext = mytext.convert_alpha()
	return mytext

class Ship(pygame.sprite.Sprite):
	def __init__(self, startpos):
		pygame.sprite.Sprite.__init__(self)
		self.image = load_image('ship.png', -1)
		self.baseimage = load_image('ship.png', -1)
		self.rect = self.image.get_rect()
		self.width = self.image.get_width()
		self.height = self.image.get_height()
		self.rect.center = startpos
		self.pos = startpos
		self.velocity_x = 0
		self.velocity_y = 0
		self.maxvelocity = MAX_VEL
		self.absolutepos = startpos
		self.angle = 0
		self.sound = load_sound("accel.wav")
		
	def update(self):
		if self.velocity_y != 0:
			if self.velocity_x > 0:
				self.angle = math.degrees(math.atan(self.velocity_y/self.velocity_x))
				self.image = pygame.transform.rotate(self.baseimage, -self.angle)
				self.rect = self.image.get_rect()
			if self.velocity_x < 0:
				self.angle = math.degrees(math.atan(self.velocity_y/self.velocity_x))
				self.image = pygame.transform.rotate(self.baseimage, -self.angle + 180)
				self.rect = self.image.get_rect()

	def input(self, pressed, seconds):
		if pressed[pygame.K_w]:
			self.velocity_y -= SHIP_ACCEL * seconds 
		if pressed[pygame.K_s]:
			self.velocity_y += SHIP_ACCEL * seconds
		if pressed[pygame.K_a]:
			self.velocity_x -= SHIP_ACCEL * seconds
		if pressed[pygame.K_d]:
			self.velocity_x += SHIP_ACCEL * seconds
		
		if self.velocity_x>self.maxvelocity:
			self.velocity_x = self.maxvelocity
		if self.velocity_y>self.maxvelocity:
			self.velocity_y = self.maxvelocity
		if self.velocity_x<(-self.maxvelocity):
			self.velocity_x = (-self.maxvelocity)
		if self.velocity_y<(-self.maxvelocity):
			self.velocity_y = (-self.maxvelocity)	

class Button():
	"""
	Creates a Surface object and a Rect object 
	The Surface object gets blitted to the screen
	The Rect object detects clicks
	"""
	def __init__(self, text, pos, fsize = 25, wh=(300,50), color1 = (230,230,230), color2 = (0,122,174)): 
		self.strmsg = text
		self.msg = write(text, fsize)
		self.pos = pos
		self.wh = wh
		self.highlight = False
		self.basecolor = color1
		self.highcolor = color2
		self.msgwidth = self.msg.get_width()
		self.msgheight = self.msg.get_height()
		self.surf = pygame.Surface(wh)
		self.surf.fill(color1) #this apparently sets coordinates back to (0,0)
		self.rect = pygame.Rect(pos,wh)
		self.surf.blit(self.msg, ((wh[0]-self.msgwidth)/2,(wh[1]-self.msgheight)/2))
		self.sound = load_sound("buttonclick.wav")

	def clicked(self, mousepos):
		if self.rect.collidepoint(mousepos):
			self.sound.play()
		return self.rect.collidepoint(mousepos)

	def update(self, mousepos):
		if self.rect.collidepoint(mousepos) and self.highlight == False:
			self.rect = self.surf.fill(self.highcolor)
			self.rect = pygame.Rect(self.pos,self.wh)
			self.surf.blit(self.msg, ((self.wh[0]-self.msgwidth)/2,(self.wh[1]-self.msgheight)/2))
			self.highlight = True
			return True
		elif not self.rect.collidepoint(mousepos) and self.highlight == True:
			self.rect = self.surf.fill(self.basecolor)
			self.rect = pygame.Rect(self.pos,self.wh)
			self.surf.blit(self.msg, ((self.wh[0]-self.msgwidth)/2,(self.wh[1]-self.msgheight)/2))
			self.highlight = False
			return True
		else:
			return False	

class Star(pygame.sprite.Sprite):
	total = 0

	def __init__(self, xy_wh):
		pygame.sprite.Sprite.__init__(self)
		self.starinfo = xy_wh
		self.startpos = (xy_wh[0],xy_wh[1])
		self.width = xy_wh[2]
		self.height = xy_wh[3]
		self.baseimage = load_image('star.png', -1)
		self.image = pygame.transform.scale(self.baseimage, (self.width,self.height))
		self.rect = self.image.get_rect()
		self.rect.x = self.startpos[0]
		self.rect.y = self.startpos[1]
		Star.total += 1

class Nebula(pygame.sprite.Sprite):

	def __init__(self, pos):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface([150,150])
		self.image = load_image('nebula.png', -1)
		self.rect = self.image.get_rect()
		self.pos = pos
		self.rect.x = pos[0]
		self.rect.y = pos[1]
		self.totaltime = 0

	def rotate(self, seconds):
		self.totaltime += seconds
		if self.totaltime > 0.1:
			self.totaltime = 0
			self.image = pygame.transform.rotate(self.image, 90)

class Timer():
	def __init__(self):
		self.clock = pygame.time.Clock()
		self.FPS = 60
		self.playtime = 0
		self.milliseconds = 0
		self.seconds = 0
		self.minutes = 0

	def update(self):
		self.milliseconds = self.clock.tick(self.FPS)
		self.seconds = self.milliseconds / 1000.0
		self.playtime += self.seconds

	def formattime(self):
		milliplaytime = self.playtime - math.floor(self.playtime)

		if self.playtime >= 60:
			self.minutes = self.playtime / 60.0
			self.playtime = self.playtime % 60.0

		#minutes:seconds:milliseconds (without leading/trailing zeroes)
		timerstring = ('%02d'% self.minutes)+"."+ ('%02d'% self.playtime) + str(decimal.Decimal(milliplaytime).quantize(TWOPLACES)).strip("0") 
		return timerstring

class Track():
	trackdict = {1 : ("track.png","track1.txt","track1scores.txt"),
					 2 : ("track.png","track2.txt","track2scores.txt"),
					 3 : ("track.png","track3.txt","track3scores.txt"),
					 4 : ("track.png","track4.txt","track4scores.txt"),
					 5 : ("track.png","track5.txt","track5scores.txt")}
						 #background , coordinates, highscores
	def __init__(self, num):
		self.trackinfo = Track.trackdict[num]
		self.track = load_image(self.trackinfo[0])
		self.trackwh = self.track.get_size()
		self.coordinatelist = []
		self.starlist = []
		self.rectstarlist = []
		self.shipstartpos = 0,0
		self.nebulapos = 0,0

	def loadtrack(self):
		trackname = os.path.join('levels', self.trackinfo[1])
		trackfile = open(trackname, 'r')
		for line in trackfile:
			self.coordinatelist.extend(literal_eval(line.strip()))

		self.shipstartpos = self.coordinatelist.pop(0)
		self.nebulapos = self.coordinatelist.pop(len(self.coordinatelist)-1)
			
		for t in self.coordinatelist:
			s = Star(t)
			self.starlist.append(s)
		return self.shipstartpos, self.nebulapos, self.starlist

	def getrectstarlist(self):
		for s in self.starlist:
			self.rectstarlist.append(s.rect)
		return self.rectstarlist

	def getstartpos(self):
		return self.shipstartpos

	def gettrack(self):
		return self.track
	
	def gettrackscores(self):
		return self.trackinfo[2]

class GalaxyRacer():
	"""The main class of the game"""

	def __init__(self):
		LOGEvent.info("Game successfully instantiated and sounds/art assets loaded.")
		pygame.mixer.pre_init(44100, -16, 2, 2048)
		pygame.init()
		self.screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
		pygame.display.set_caption("GalaxyRacer - A fast paced Space Race")
		self.background=pygame.Surface((self.screen.get_rect().width, self.screen.get_rect().height))
		self.gamestate = "STARTUP"		

	def startup(self):
		logo1 = load_image("CognitiveThought.png")
		logo2 = load_image("CelestialSoft.png")
		logolist = [logo1, logo2]
		for l in logolist:
			for i in range (225): #fade in
		   		self.background.fill((0,0,0))
		   		l.set_alpha(i)
		   		self.screen.blit(l,(0,0))
		   		pygame.display.flip()

			pygame.time.delay(1000)
			for i in range (225): #fade out
				self.background.fill((0,0,0))
				l.set_alpha(225-i)
				self.screen.blit(l,(0,0))
				pygame.display.flip()
			pygame.time.delay(1000)
		load_music('menu_music.ogg')
		pygame.mixer.music.play(-1)
		self.gamestate = "MENU"

	def menu(self):
		self.background = load_image("menu_background.png")

		playbutton = Button("Play", (250,250), fsize = 30)
		tutorialbutton = Button("Tutorial", (250,350), fsize = 30)
		exitbutton = Button("Exit", (250,450), fsize = 30)
		buttonlist = [playbutton, tutorialbutton, exitbutton]

		#draw the menu
		self.screen.blit(self.background,(0,0))
		self.screen.blit(playbutton.surf,playbutton.pos)
		self.screen.blit(tutorialbutton.surf,tutorialbutton.pos)
		self.screen.blit(exitbutton.surf,exitbutton.pos)
		pygame.display.update()

		menuloop = True
		while menuloop:
			mousepos = pygame.mouse.get_pos()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					menuloop = False
					self.gamestate = "EXIT"
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						menuloop = False
						self.gamestate = "EXIT"
				elif event.type == pygame.MOUSEBUTTONDOWN:
					if pygame.mouse.get_pressed()[0]: #left mouse button down
						if playbutton.clicked(mousepos): 
							self.gamestate = "STAGE_SELECT"
							menuloop = False
						elif tutorialbutton.clicked(mousepos):
							self.gamestate = "TUTORIAL"
							menuloop = False
						elif exitbutton.clicked(mousepos):
							self.gamestate = "EXIT"
							menuloop = False
			#checks if buttons should highlight						
			for b in buttonlist:				
				if b.update(mousepos):
					self.screen.blit(b.surf,b.pos)
			pygame.display.update()			

	def tutorial(self):
		currentpage = 1
		self.background = load_image("tutorial"+str(currentpage)+".png")
		backbutton = Button("Back", (50,500), wh = (100,50), color1 = (145,0,0), color2 = (185,0,0))
		nextbutton = Button("Next", (650,500), wh = (100,50), color1 = (0,0,145), color2 = (0,0,185))
		buttonlist = [backbutton, nextbutton]

		self.screen.blit(self.background,(0,0))
		self.screen.blit(backbutton.surf, backbutton.pos)
		self.screen.blit(nextbutton.surf, nextbutton.pos)
		pygame.display.update()

		tutorialloop = True
		while tutorialloop:
			mousepos = pygame.mouse.get_pos()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					tutorialloop = False
					self.gamestate = "EXIT"
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						tutorialloop = False
						self.gamestate = "MENU"
				elif event.type == pygame.MOUSEBUTTONDOWN:
					if pygame.mouse.get_pressed()[0]:
						if backbutton.clicked(mousepos):
							if currentpage == 1:
								tutorialloop = False
								self.gamestate = "MENU"
							else:
								currentpage -= 1
						if nextbutton.clicked(mousepos):
							if currentpage == 9:
								tutorialloop = False
								self.gamestate = "MENU"
							else:
								currentpage += 1
			self.background = load_image("tutorial"+str(currentpage)+".png")
			self.screen.blit(self.background, (0,0))
			self.screen.blit(backbutton.surf, backbutton.pos)
			self.screen.blit(nextbutton.surf, nextbutton.pos)

			for b in buttonlist:				
				if b.update(mousepos):
					self.screen.blit(b.surf,b.pos)
			pygame.display.update()

	def stageselect(self):
		#create background and buttons
		self.background = load_image("stage_select.png")
		trackimage1 = load_image("Cassiopeia.png")
		trackimage2 = load_image("Dipper.png")
		trackimage3 = load_image("Libra.png")
		trackimage4 = load_image("Pisces.png")
		trackimage5 = load_image("Scorpio.png")
		trackbutton1 = Button("Play Track 1", (30,225), fsize = 17, wh = (140,40))
		trackbutton2 = Button("Play Track 2", (180,225), fsize = 17, wh = (140,40))
		trackbutton3 = Button("Play Track 3", (330,225), fsize = 17, wh = (140,40))
		trackbutton4 = Button("Play Track 4", (480,225), fsize = 17, wh = (140,40))
		trackbutton5 = Button("Play Track 5", (630,225), fsize = 17, wh = (140,40))
		scorebutton1 = Button("Highscores", (30,270), fsize = 15, wh = (140,30))		
		scorebutton2 = Button("Highscores", (180,270), fsize = 15, wh = (140,30))
		scorebutton3 = Button("Highscores", (330,270), fsize = 15, wh = (140,30))
		scorebutton4 = Button("Highscores", (480,270), fsize = 15, wh = (140,30))
		scorebutton5 = Button("Highscores", (630,270), fsize = 15, wh = (140,30))
		backbutton = Button("Back", (50,500), wh = (100,50))
		buttonlist = [trackbutton1, trackbutton2, trackbutton3, 
				trackbutton4, trackbutton5, scorebutton1, scorebutton2, 
				scorebutton3, scorebutton4, scorebutton5, backbutton]
		trackimagelist = [trackimage1, trackimage2, trackimage3, trackimage4, trackimage5]

		#draw the menu
		self.screen.blit(self.background,(0,0))
		for b in buttonlist:
			self.screen.blit(b.surf,b.pos)
		for i in range(5):
			self.screen.blit(trackimagelist[i],(30 + 150*i, 75))
		pygame.display.update()

		stageloop = True
		while stageloop:
			mousepos = pygame.mouse.get_pos()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					stageloop = False
					self.gamestate = "EXIT"
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						stageloop = False
						self.gamestate = "MENU"
				elif event.type == pygame.MOUSEBUTTONDOWN:
					if pygame.mouse.get_pressed()[0]: #left mouse button 
						if trackbutton1.clicked(mousepos): 
							stageloop = False
							self.gamestate = "PLAYING"
							return 1
						elif trackbutton2.clicked(mousepos):
							stageloop = False
							self.gamestate = "PLAYING"
							return 2
						elif trackbutton3.clicked(mousepos):
							stageloop = False
							self.gamestate = "PLAYING"
							return 3
						elif trackbutton4.clicked(mousepos):
							stageloop = False
							self.gamestate = "PLAYING"
							return 4
						elif trackbutton5.clicked(mousepos):
							stageloop = False
							self.gamestate = "PLAYING"
							return 5
						elif scorebutton1.clicked(mousepos):
							stageloop = False
							self.gamestate = "HIGHSCORES"
							return 1
						elif scorebutton2.clicked(mousepos):
							stageloop = False
							self.gamestate = "HIGHSCORES"
							return 2
						elif scorebutton3.clicked(mousepos):
							stageloop = False
							self.gamestate = "HIGHSCORES"
							return 3
						elif scorebutton4.clicked(mousepos):
							stageloop = False
							self.gamestate = "HIGHSCORES"
							return 4
						elif scorebutton5.clicked(mousepos):
							stageloop = False
							self.gamestate = "HIGHSCORES"
							return 5
						elif backbutton.clicked(mousepos):
							stageloop = False
							self.gamestate = "MENU"		
			#checks if buttons should highlight				
			for b in buttonlist:				
				if b.update(mousepos):
					self.screen.blit(b.surf,b.pos)
			pygame.display.update()			

	def game(self, num):
		"""
		The main method for gameplay. 
		"""
		#initalize Track variables
		mytrack = Track(num)
		shipstartpos, nebulapos, starlist = mytrack.loadtrack()
		rectstarlist = mytrack.getrectstarlist() #list of collision rects
		track = mytrack.gettrack() 
		track_wh = track.get_size()
		self.background = pygame.Surface(self.screen.get_size())

		timer = Timer()
		myship = Ship(shipstartpos)
		nebula = Nebula(nebulapos)

		camerapos = (mytrack.getstartpos()[0] - WINDOW_WIDTH/2, mytrack.getstartpos()[1] - WINDOW_HEIGHT/2) 
		
		#initalize sound and music 
		load_music('game_music.ogg')
		pygame.mixer.music.play(-1)
		crashsound = load_sound("crash.wav")
		winsound = load_sound('victory.wav')
		
		pausebackground = pygame.Surface(self.screen.get_size())
		pausebackground.fill((0,0,0))
		pausebackground.set_alpha(150)
		#initialize pause, death, and win menu buttons
		resumebutton = Button("Resume", (250,300))
		exitbutton = Button("Back to Menu", (250,400))
		pausebuttonlist = [resumebutton, exitbutton]
		retrybutton = Button("Retry track?", (250,300))
		deathbuttonlist = [retrybutton, exitbutton]
		winbutton = Button("Highscores!", (300,400), wh = (200,75))

		timer.clock.tick() #call the tick before entering game loop to restart timer
		pauseloop = False
		gameloop = True
		while gameloop:

			timer.update()
			for event in pygame.event.get():
					if event.type == pygame.QUIT: #game exits completely if you close window
						gameloop = False
						self.gamestate = "EXIT"
					elif event.type == pygame.KEYDOWN:
						if event.key == pygame.K_ESCAPE: #game pauses if you press esc
							pauseloop = True
							#draw the pause manu
							self.screen.blit(pausebackground, (0,0))
							self.screen.blit(resumebutton.surf, (250,300))
							self.screen.blit(exitbutton.surf, (250,400))
							pygame.display.update()

			#pause menu
			while pauseloop:	
				"""
				Blits the faded layer onto screen and displays Resume and Exit button
				Game will only continue if a button is clicked
				"""
				mousepos = pygame.mouse.get_pos()
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						pauseloop = False
						gameloop = False
						self.gamestate = "EXIT"
					elif event.type == pygame.KEYDOWN:
						if event.key == pygame.K_ESCAPE:
							pauseloop = False
					elif event.type == pygame.MOUSEBUTTONDOWN:
						if pygame.mouse.get_pressed()[0]:#left mouse button down
							if resumebutton.clicked(mousepos): 
								pauseloop = False
								timer.clock.tick() #reset tick time
							elif exitbutton.clicked(mousepos):
								pauseloop = False
								gameloop = False
								self.gamestate = "MENU"
								load_music('menu_music.ogg')
								pygame.mixer.music.play(-1)			
				#button highlighting
				for b in pausebuttonlist:				
					if b.update(mousepos):
						self.screen.blit(b.surf,b.pos)
				pygame.display.update()	

			#handles game inputs
			pressed = pygame.key.get_pressed()
			myship.input(pressed, timer.seconds)
			myship.update()

			"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
			Code describing the Ship's movement while keeping it centered
			in the screen. Camera moves with same velocity as the ship. 
			When camerapos goes out of bounds near the edges of the track, it is 
			no longer updated (camera stops), and the ship leaves the center of the 
			screen. Camera resumes updates once the ship moves away from the edges of the track.
			"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
			#only create subsurface if it's within bounds
			if  camerapos[0]>=0 and camerapos[1]>=0 and \
				camerapos[0]<=(track_wh[0]-WINDOW_WIDTH) and \
				camerapos[1]<=(track_wh[1]-WINDOW_HEIGHT):
					
					#WE MUST UPDATE CAMERAPOS AFTER CREATING SUBSURFACE
					self.background = track.subsurface((camerapos[0], camerapos[1],
									   WINDOW_WIDTH, WINDOW_HEIGHT))
					camerapos = (myship.absolutepos[0] - (WINDOW_WIDTH/2) + myship.velocity_x * timer.seconds,
						myship.absolutepos[1] - (WINDOW_HEIGHT/2) + myship.velocity_y * timer.seconds)
					
					#HARD CODING TO AVOID NEGATIVE NUMBERS IN camerapos
					if camerapos[0]<0:	
						camerapos = (0,camerapos[1])
					if camerapos[1]<0:
						camerapos = (camerapos[0],0)
					if camerapos[0]>(track_wh[0]-WINDOW_WIDTH):
						camerapos = (track_wh[0]-WINDOW_WIDTH,camerapos[1])
					if camerapos[1]>(track_wh[1]-WINDOW_HEIGHT):
						camerapos = (camerapos[0],track_wh[1]-WINDOW_HEIGHT)

			#updating ship coordinates 
			myship.absolutepos = (myship.absolutepos[0] + myship.velocity_x * timer.seconds,
								 myship.absolutepos[1] + myship.velocity_y * timer.seconds)
			myship.pos = (myship.absolutepos[0] - camerapos[0], myship.absolutepos[1] - camerapos[1])
			updaterect = pygame.Rect(myship.absolutepos[0], myship.absolutepos[1], myship.width, myship.height)
			
			#draw camera, ship, nebula, and stars
			self.screen.blit(self.background, (0,0))		
			self.screen.blit(myship.image, (myship.pos[0],myship.pos[1]))
			self.screen.blit(write(timer.formattime(), 60, (255,255,255)), (450,10))
			for s in starlist:
				track.blit(s.image, (s.rect.x, s.rect.y))
			nebula.rotate(timer.seconds)
			track.blit(nebula.image, (nebula.pos[0],nebula.pos[1]))
			
			"""End Game"""

			#if the ship touches the nebula	
			if updaterect.colliderect(nebula.rect):
				"""Win situation"""
				winsound.play()
				win_background = load_image("win.png")
				for i in range (225): #fade in image
			   		self.background.fill((0,0,0))
			   		win_background.set_alpha(i)
			   		self.screen.blit(win_background,(0,0))
			   		#pygame.time.delay(10)
			   		pygame.display.update()
			   	self.screen.blit(write("Track "+str(num)+" cleared!", 50, (255,255,255)), (200,50))
			   	self.screen.blit(write("Your time: "+ timer.formattime(), 40, (255,255,255)), (200,200))
			   	self.screen.blit(winbutton.surf, (300,400))
			   	pygame.display.flip()
			   	load_music('menu_music.ogg')
				pygame.mixer.music.play(-1)

			   	winloop = True
			   	while winloop:
			   		mousepos = pygame.mouse.get_pos()
					for event in pygame.event.get():
						if event.type == pygame.MOUSEBUTTONDOWN:
							if pygame.mouse.get_pressed()[0]: 
								if winbutton.clicked(mousepos): 
									winloop = False
									gameloop = False
									newrecord = True
									self.gamestate = "HIGHSCORES"
									#check if player earned a highscore
									fullname = os.path.join('saves', mytrack.gettrackscores()) 
									f = open(fullname, 'r')
									i = 0
									while newrecord and i < 5:
										filescore = f.readline().translate(None, '.')
										if timer.formattime().translate(None, '.') < filescore[:filescore.index(',')]: #load in the i number line in track(num)highscores
											newrecord = False
											self.addhighscore(timer, i, fullname)
										i += 1			
									f.close()
					if winbutton.update(mousepos):							
						self.screen.blit(winbutton.surf,winbutton.pos)
					pygame.display.update()				

			#if the ship leaves the star road		
			if not updaterect.collidelistall(rectstarlist):
				"""Death/Lose Situation"""
				crashsound.play()
				self.screen.blit(pausebackground, (0,0))
				self.screen.blit(retrybutton.surf, (250,300))
				self.screen.blit(exitbutton.surf, (250,400))
				pygame.display.update()

				deathloop = True
				while deathloop:
					mousepos = pygame.mouse.get_pos()
					for event in pygame.event.get():
						if event.type == pygame.QUIT:
							deathloop = False
							gameloop = False
							self.gamestate = "EXIT"
						elif event.type == pygame.KEYDOWN:
							if event.key == pygame.K_ESCAPE:
								deathloop = False
								gameloop = False
								self.gamestate = "MENU"
								load_music('menu_music.ogg')
								pygame.mixer.music.play(-1)
						elif event.type == pygame.MOUSEBUTTONDOWN:
							if pygame.mouse.get_pressed()[0]: 
								if retrybutton.clicked(mousepos): 
									deathloop = False
									gameloop = False
								elif exitbutton.clicked(mousepos):
									deathloop = False
									gameloop = False
									self.gamestate = "MENU"	
									load_music('menu_music.ogg')
									pygame.mixer.music.play(-1)
					#button highlighting loop
					for b in deathbuttonlist:				
						if b.update(mousepos):
							self.screen.blit(b.surf,b.pos)
					pygame.display.update()	
			pygame.display.update()

	def addhighscore(self, timer, num, fullname):
		buttonlist =[]
		name = ['_','_','_']
		highscores = []
		self.background = load_image("newhighscore.png")
		tempbackground = self.background.subsurface((300,200,200,75))
		
		#initialize 26 character buttons + erasebutton
		for i in range(26):
			b = Button(chr(ord('A')+i), (100+65*(i%9),300+65*(i/9)), wh = (65,65))
			buttonlist.append(b)
		erasebutton = Button("Erase", (620,430), wh = (65,65), fsize = 20)
		donebutton = Button("Done", (225,530), fsize = 40)

		#draw the screen
		self.screen.blit(self.background, (0,0))
		for b in buttonlist:
			self.screen.blit(b.surf,b.pos)
		self.screen.blit(erasebutton.surf,erasebutton.pos)
		self.screen.blit(write("NEW HIGHSCORE", 50, color = (255,255,255)), (200,50))
		self.screen.blit(write("Enter your name! (3 characters)", 30, color = (255, 255, 255)), (180,150))
		pygame.display.update()

		count = 0
		done = False
		while not done:
			mousepos = pygame.mouse.get_pos()
			for event in pygame.event.get():
				if event.type == pygame.MOUSEBUTTONDOWN:
					if pygame.mouse.get_pressed()[0]: 
						for b in buttonlist:
							if b.clicked(mousepos):
								if count<3:
									name.insert(count,b.strmsg)
									name.pop()
									count += 1
						if erasebutton.clicked(mousepos):
							if count>0:
								count -= 1
								name.pop(count)
								name.append('_')
						if donebutton.clicked(mousepos):
							done = True

			self.screen.blit(tempbackground, (300,200))
			for i in range(len(name)):
				self.screen.blit(write(name[i], 50, color = (255, 255, 255)), (325+50*i,200))
			for b in buttonlist:				
				if b.update(mousepos):
					self.screen.blit(b.surf,b.pos)
			if erasebutton.update(mousepos):
				self.screen.blit(erasebutton.surf,erasebutton.pos)
			if count == 3:
				self.screen.blit(donebutton.surf,donebutton.pos)
			pygame.display.update()

		#save highscore + name[] at position num to track?scores.txt
		#delete 6th line/last line of track?scores.txt
		f = open(fullname, 'a')
		f.write("\n" + timer.formattime() + ",%s" % ''.join(name) + "\n")
		f.close()

		f = open(fullname, 'r+')
		for line in f:
			highscores.append(line)
		f.close()

		highscores.sort()
		highscores.remove('\n')
		highscores.pop()

		f = open(fullname, 'w')
		for h in highscores:
			f.write(h)
		f.close()

	def highscores(self, tracknum):
		self.background = load_image("highscores.png")
		backbutton = Button("Back", (50,500), wh = (100,50))
		highscore = []

		self.screen.blit(self.background, (0,0))
		self.screen.blit(backbutton.surf,backbutton.pos)
		self.screen.blit(write("Track "+str(tracknum), 60, (255,255,255)), (275,25))
		pygame.display.update()

		pathname = os.path.join('saves', "track%dscores.txt" % tracknum) 
		f = open(pathname, 'r')
		for line in f:
			line = line.replace(',',' - ') 
			highscore.append(line)

		for i in range(len(highscore)):
			self.screen.blit(write(str(i+1)+' - '+highscore[i][:-1], 50, (255,255,255)), (200,100+75*i))
		pygame.display.update()	

		scoresloop = True
		while scoresloop:
			mousepos = pygame.mouse.get_pos()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					scoresloop = False
					loop = False
					self.gamestate = "EXIT"
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						scoresloop = False
						self.gamestate = "STAGE_SELECT"
				elif event.type == pygame.MOUSEBUTTONDOWN:
					if pygame.mouse.get_pressed()[0]: 
						if backbutton.clicked(mousepos): 
							scoresloop = False
							self.gamestate = "STAGE_SELECT"

def main():
	LOGEvent.info("System Event Logger Initialized.")
	LOGEvent.info("Main Software Initialized.")
	gr = GalaxyRacer()
	tracknum = 0 
	mainloop = True
	while mainloop:
		if gr.gamestate == "STARTUP":
			gr.startup()
		elif gr.gamestate == "MENU":
			gr.menu()
		elif gr.gamestate == "TUTORIAL":
			gr.tutorial()	
		elif gr.gamestate == "STAGE_SELECT":
			tracknum = gr.stageselect()
		elif gr.gamestate == "PLAYING":
			gr.game(tracknum)
		elif gr.gamestate == "HIGHSCORES":
			gr.highscores(tracknum)	
		elif gr.gamestate == "EXIT":
			mainloop = False
			LOGEvent.info('Game Exited!\n************************************************************')
			pygame.quit()

if __name__ == '__main__': main()
