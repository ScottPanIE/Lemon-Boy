import pygame
import os
import math
import random
from script import Sprite 

ruta_base =  os.path.abspath("")
ruta_base += "/image/"


class Enemy(Sprite.Sprite):
	def __init__(self):
		Sprite.Sprite.__init__(self)
		self.limite_x = 50
		self.vl = 3
	def patroling(self):
		if self.vl > 0:
			if self.rect.x < self.pos_patrullandox + self.limite_x:
				self.vlx = self.vl
			else:
				self.vl *=-1 
		elif self.vl < 0:
			if self.rect.x > self.pos_patrullandox -self.limite_x:
				self.vlx = self.vl
			else:
				self.vl *=-1

	def follow(self):
		self.distancia = math.sqrt(	(	(self.rect.x - self.player.rect.x )**2 + (self.rect.y - self.player.rect.y)**2	)	)
		if self.distancia < 200:
			if self.player.rect.left < self.rect.left:
				self.vlx = -self.vl
			elif self.player.rect.right > self.rect.right:
				self.vlx = self.vl
			
			if self.player.rect.left == self.rect.right or self.player.rect.right == self.rect.left:
				self.vlx = 0

		else:
			self.vlx = 0



class Enemy_Rect(Enemy):
	def __init__(self,x,y,group):
		Enemy.__init__(self)
		self.image = pygame.Surface((20,20))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.vlx = -3
		self.vly = 0
		self.group = group
		self.pos_patrullandox = self.rect.x
		
	def update(self):
		self.gravity()
		self.patroling()
		self.collided()



class Skull(Enemy):
	def __init__(self,x,y,group,Object,sentido = True):
		Enemy.__init__(self)
		self.position = 1 
		self.position_state = 1
		self.sentido = sentido
		
		if self.sentido == False:
			self.image = pygame.image.load(ruta_base + "skulls{}.png".format(self.position)) 
		
		else:
			self.image = pygame.transform.flip(pygame.image.load(ruta_base + "skulls{}.png".format(self.position)),True,False)	 


		self.image = self.image.subsurface((5,13),(27,27))
		self.image = pygame.transform.scale(self.image,(40,40))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		#self.pos_patrullandox = 0
		#self.player = player
		self.distancia = None
		self.delay = 20
		self.cont = 0
		self.group = group
		self.element = "skull"
		
		self.Object = Object
		self.cont_bullet = 0
		
		
	def update(self):
		#self.seguimiento()
		self.gravity()
		self.rect.x += self.vlx
		self.rect.y += self.vly
		self.seguimiento()
		self.collided()
			
	def seguimiento(self):
		self.distancia = math.sqrt(	(	(self.Object.x - self.rect.x )**2 + (self.Object.y - self.rect.y)**2	)	)
		self.cont += 5
		if self.distancia < 250:			
			if self.cont >= self.delay:		
				if self.position <= 4:
					
					if self.sentido == False:
						self.image = pygame.image.load(ruta_base + "skulls{}.png".format(self.position)) 
					elif self.sentido == True:
						self.image = pygame.transform.flip(pygame.image.load(ruta_base + "skulls{}.png".format(self.position)),True,False) 

					self.image = self.image.subsurface((5,13),(27,27))
					self.image = pygame.transform.scale(self.image,(40,40))

					self.position +=1
					self.cont = 0
					self.cont_bullet = 0
				else:
					self.cont_bullet += 0.45
					if self.cont_bullet > 10:	
						#self.bullet.add(Bullet.Bullet(self.rect.x,self.rect.y-2))
						self.cont_bullet = 0
		else:	
			if self.cont >= self.delay:
				if self.position > 1:				
					self.position -=1
					if self.sentido == False:
						self.image = pygame.image.load(ruta_base + "skulls{}.png".format(self.position)) 
					elif self.sentido == True:
						self.image = pygame.transform.flip(pygame.image.load(ruta_base + "skulls{}.png".format(self.position)),True,False) 
					
					self.image = self.image.subsurface((5,13),(27,27))
					self.image = pygame.transform.scale(self.image,(40,40))

					self.cont = 0
				else:
					self.fijo()			
	def fijo(self):
			if self.position_state < 5:		
				
				if self.sentido == False:
					self.image = pygame.image.load(ruta_base + "skulls{}.png".format(self.position)) 
				elif self.sentido == True:
					self.image = pygame.transform.flip(pygame.image.load(ruta_base + "skulls{}.png".format(self.position)),True,False)  
				
				self.image = self.image.subsurface((5,13),(27,27))
				self.image = pygame.transform.scale(self.image,(40,40))

				self.position_state +=1
				self.cont = 0
			elif self.position_state >= 4:
				self.position_state =1 

	def cannon(self):
		#print(len(self.group_bullet))
		for bullet in self.bullet:
			if bullet.rect.x <= 0:
				bullet.kill()


class Lord_of_the_flies(Enemy):
	def __init__(self,x,y,group):
		Enemy.__init__(self)
		self.position = 1 
		self.image = pygame.image.load(ruta_base + "/sprites/belcebu/belcebu{}.png".format(self.position))
		self.image = pygame.transform.scale(self.image,(40,80))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.vlx = 0
		self.vly = 0
		self.group = group
		self.delay = 20
		self.cont = 0

	def update(self):
		self.cont +=10
		if self.cont >= self.delay:
			if self.position < 5:		
				self.image = pygame.image.load(ruta_base + "/sprites/belcebu/belcebu{}.png".format(self.position)) 
				self.image = pygame.transform.scale(self.image,(40,80))
				self.position +=1
			elif self.position >= 4:
				self.position =1 
			
			self.cont = 0
		
		self.gravity()
		self.collided()

class Dog(Enemy):
	def __init__(self,x,y,group,sentido):#player):
		Enemy.__init__(self)
		frames = [pygame.image.load(ruta_base + "sprites/dog1.png"),
				  pygame.image.load(ruta_base + "sprites/dog2.png"),
				  pygame.image.load(ruta_base + "sprites/dog3.png")]
				
		self.scale_x = 30
		self.scale_y = 25
		self.image = pygame.transform.scale(frames[0],(self.scale_x,self.scale_y))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.animacion = Sprite.animation(frames,self.scale_x,self.scale_y)
		self.animacion.limite = 3
		self.group = group
		#self.player = player
		self.pos_patrullandox = self.rect.x

		self.vl = 3 if sentido == "left" else -3
		
		#print(self.vl)
	def update(self):

		if self.vlx < 0:
			self.image = self.animacion.update(True)

		if self.vlx > 0:
			self.image = self.animacion.update(False)
		
		self.patroling()
		#self.follow()
		self.gravity()
		self.collided()
		