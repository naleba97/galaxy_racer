"""
LevelCreator for GalaxyRacer

Move camera with [WASD] and [Left Click] to create stars
Press [E] to switch the size of the stars
Press [R] to place the ship start position
Press [T] to place the nebula position
Only the most recently placed ship/nebula will be saved
When finished press [ESC]

Saves star coordinates to GalaxyRacer/levels/track?.txt

desired functions - right click checks collision with star object in starlist
						if collides - delete object
"""
import sys, os
import pygame
from pygame.locals import *

#game constants
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768

#make loading images easier
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

#makes drawing text to surface easier
def write(msg, size, color = (255,255,255), font="comicsansms"):
	myfont = pygame.font.SysFont(font, size) 
	mytext = myfont.render(msg, True, color) #msg, antialias, color pink
	mytext = mytext.convert_alpha()
	return mytext

class Star(pygame.sprite.Sprite):
	total = 0

	def __init__(self, xy_wh):
		pygame.sprite.Sprite.__init__(self, self.groups)
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

def main():
	pygame.init()
	screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
	track = load_image('track.png', False)
	track_wh = track.get_size()
	background = pygame.Surface(screen.get_size())
	starimage1 = load_image('star.png', -1)
	starimage2 = pygame.transform.scale2x(starimage1)
	starimage3 = pygame.transform.scale2x(starimage2)
	ship = load_image('ship.png', -1)
	shippos = 0,0
	nebula = load_image('nebula.png', -1)
	nebulapos = 0,0
	clock = pygame.time.Clock()
	FPS = 60
	camerapos = 0,0
	camera_vel_x = 0
	camera_vel_y = 0
	starsize = 1
	starlist = []
	stargroup = pygame.sprite.Group()
	Star.groups = stargroup

	gameloop = True
	while gameloop:	
		mousepos = pygame.mouse.get_pos()
		if starsize == 1:
			mystarimage = starimage1
		elif starsize == 2:
			mystarimage = starimage2
		elif starsize == 3:
			mystarimage = starimage3

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				gameloop = False
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					gameloop = False
				elif event.key == pygame.K_e:
					starsize += 1
					if starsize == 4:
						starsize = 1
				elif event.key == pygame.K_r:
					shippos = (mousepos[0] + camerapos[0], mousepos[1] + camerapos[1])
					track.blit(ship, shippos)
				elif event.key == pygame.K_t:
					nebulapos = (mousepos[0] + camerapos[0], mousepos[1] + camerapos[1])
					track.blit(nebula, nebulapos)
			elif event.type == pygame.MOUSEBUTTONDOWN:
				if pygame.mouse.get_pressed()[0]:
					starpos = (mousepos[0] + camerapos[0], mousepos[1] + camerapos[1])
					starwh = mystarimage.get_size()
					track.blit(mystarimage, starpos)
					xy_wh = starpos+starwh
					s = Star(xy_wh)
					starlist.append(s)

		pressed = pygame.key.get_pressed()
		if pressed[pygame.K_a]:
			camera_vel_x = -10
		elif pressed[pygame.K_d]:
			camera_vel_x = 10
		else:
			camera_vel_x = 0
			
		if pressed[pygame.K_w]:
			camera_vel_y = -10	
		elif pressed[pygame.K_s]:
			camera_vel_y = 10	
		else:
			camera_vel_y = 0

		#only create subsurface if it's within bounds
		if  camerapos[0]>=0 and camerapos[1]>=0 and \
			camerapos[0]<=(track_wh[0]-WINDOW_WIDTH) and \
			camerapos[1]<=(track_wh[1]-WINDOW_HEIGHT):
				background = track.subsurface((camerapos[0], camerapos[1],
								   WINDOW_WIDTH, WINDOW_HEIGHT))
				camerapos = (camerapos[0] + camera_vel_x, camerapos[1] + camera_vel_y)

				#HARD CODING TO AVOID NEGATIVE NUMBERS IN camerapos
				if camerapos[0]<0:	
					camerapos = (0,camerapos[1])
				if camerapos[1]<0:
					camerapos = (camerapos[0],0)
				if camerapos[0]>(track_wh[0]-WINDOW_WIDTH):
					camerapos = (track_wh[0]-WINDOW_WIDTH,camerapos[1])
				if camerapos[1]>(track_wh[1]-WINDOW_HEIGHT):
					camerapos = (camerapos[0],track_wh[1]-WINDOW_HEIGHT)

		screen.blit(background, (0,0))
		screen.blit(mystarimage, mousepos)
		screen.blit(write('Move camera with [WASD] and [Left Click] to create stars', 15), (0,0))
		screen.blit(write('Press [E] to switch the size of the stars', 15), (0,20))
		screen.blit(write('Press [R] to place the ship start position', 15), (0,40))
		screen.blit(write('Press [T] to place the nebula position', 15), (0,60))
		screen.blit(write('Only the most recently placed ship/nebula will be saved', 15), (0,80))
		screen.blit(write('When finished press [ESC]', 15), (0,100))
		screen.blit(write(str((mousepos[0] + camerapos[0], mousepos[1] + camerapos[1])), 20), (0,120))
		clock.tick(FPS)		
		pygame.display.update()

	#iterates the file name
	for i in range(1,100):
		name = "levels/newtrack"+str(i)+".txt"
		if not os.path.isfile(name):
			fullname = os.path.join(name)
			break

	f = open(fullname, 'w')

	f.write(str(shippos)+",\n") #first line is always ship pos

	for s in starlist:
		temp = str(s.starinfo) 
		f.write(temp+",\n")

	f.write(str(nebulapos)+",\n") #last line is always nebula pos

if __name__ == '__main__': main()
