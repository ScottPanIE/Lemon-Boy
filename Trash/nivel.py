
import pygame
import colisiones



from sprites import Player
from sprites import Elementos



ANCHO,ALTO = 1000,520

"""	Nota:
	Crear menú de objetos obtenidos
	Mejorar la decteción de colisión con respecto al salto	
"""
	
		
class Nivel(pygame.sprite.Sprite):

	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.group_general = pygame.sprite.Group()
		self.group_inmovil = pygame.sprite.Group()
		self.group_trampolin = pygame.sprite.Group()
		self.group_dead = pygame.sprite.Group()
		self.group_lemones = pygame.sprite.Group()
		self.group_enemy = pygame.sprite.Group()

		self.prox_nivel = None
		self.prox_escena = None

		self.colision = colisiones.Colisiones()
		self.colision_enemy = colisiones.Colisiones()
		self.map = None
		
	def update(self):
		self.group_general.update()
		self.player.update()		

		self.colision.estaticos(self.player,self.group_inmovil)
		self.colision.salto(self.player,self.group_trampolin)
		self.colision.muerto(self.player,self.group_dead,self.llave)
		self.colision.lemon(self.player,self.group_lemones)		

		for enemy in self.group_enemy:
			self.colision_enemy.estaticos(enemy,self.group_inmovil)
			self.colision_enemy.salto(enemy,self.group_trampolin)
			self.colision_enemy.muerto(enemy,self.group_dead,self.llave)
			self.colision_enemy.lemon(enemy,self.group_lemones)	
			

		if self.player.rect.colliderect(self.llave.rect):
			self.player.llave = True
			self.llave.kill()
		if self.player.rect.colliderect(self.puerta.rect):
			if self.player.llave == True:
				self.puerta.activar_animacion = True
				self.prox_escena = self.prox_nivel
						

	def draw(self,VENTANA):
		
		self.group_general.draw(VENTANA)
		VENTANA.blit(self.player.image,self.player.rect)

	def generate(self):


		x = 0
		y = 0

		for i in range(len(self.map)):
			self.map[i] = list(self.map[i])
			

		for i in range(len(self.map)):
			for j in range(len(self.map[0])):	
				if self.map[i][j] == "E":

					try:
						self.player.rect.x = x
						self.player.rect.y = y
					except:
						j = Player.Player(x,y)
						self.player = j

				elif self.map[i][j] == "#":
					j = Elementos.Block(x,y,(20*2,20*2),(0,0))
					j.scale2x()
					self.group_general.add(j)
					self.group_inmovil.add(j)

				elif self.map[i][j] == "X":
					j = Elementos.Puas(x,y)
					self.group_general.add(j)
					self.group_dead.add(j)

				elif self.map[i][j] == "S":
					j = Elementos.Puerta(x,y)
					self.puerta = j
					self.group_general.add(j)
					  
				elif self.map[i][j] == "P":
					j = Elementos.Lemon(x,y)
					self.group_general.add(j)
					self.group_lemones.add(j)

				elif self.map[i][j] == "L":
					j = Elementos.Llave(x,y)
					self.group_general.add(j)
					self.llave = j

				elif self.map[i][j] == "T":
					j = Elementos.Trampolin(x,y)
					self.group_general.add(j)
					self.group_trampolin.add(j)

				elif self.map[i][j] == "B":	
					
					try:
						j = Player.Enemy(x,y,self.player)
						self.group_general.add(j)
						self.group_enemy.add(j)

					except:
						pass


				#elif self.map[i][j] == "-":
					#pass


				x +=40


			x = 0
			y +=40				

		x,y = 0,0

		if len(self.group_enemy) == 0:
			for i in range(len(self.map)):
				for j in range(len(self.map[0])):
					if self.map[i][j] == "B":	
						j = Player.Enemy(x,y,self.player)
						self.group_general.add(j)
						self.group_enemy.add(j)					
						print("Enemigo encontrado.")
						break

					x +=40

				x = 0
				y +=40

		

class Nivel1(Nivel):
	def __init__(self):
		Nivel.__init__(self)
		self.prox_nivel = Nivel2()
		self.prox_escena = None
		self.map =[ "#------------------------",
					"#------------------------",
					"#------------------------",
					"##-----------------------",
					"#E-------P-------B-----S-",
					"####---###-----####---###",
					"#-----XX#-----#######--##",
					"#-----###-----########--#",
					"##------#-----####-----##",
					"#X----###-----####----###",
					"##------------L------####",
					"####------XX--###########",
					"#########################"] 

class Nivel2(Nivel):
	def __init__(self):
		Nivel.__init__(self)
		self.prox_nivel = Nivel3()
		self.prox_escena = None
		self.map =[ "#########################",
					"#-----------------------#",
					"#-----------------------#",
					"#-----XX----------------#",
					"#L-x--##-T-P------------#",
					"#####---###########---###",
					"#-------------------#--##",
					"#-------------####-###--#",
					"##----------B#---------##",
					"#X--------#####------x###",
					"###----X#########----####",
					"#-E---#############X---S-",
					"#########################"] 

class Nivel3(Nivel):
	def __init__(self):
		Nivel.__init__(self)
		self.prox_nivel = Nivel4()
		self.prox_escena = None
		self.map =[ "#########################",
					"###----------------------",
					"##-----------------------",
					"#-----------------B----S-",
					"#-----------T---X########",
					"###---#-#####---#-------#",
					"#-P-#-----#-------------#",
					"#######X----#--##-----L-#",
					"#------##----------x-##-#",
					"#--------##--------#----#",
					"#------------##---------#",
					"#E---------------##-----#",
					"#########################"] 

class Nivel4(Nivel):
	def __init__(self):
		Nivel.__init__(self)
		self.prox_nivel  = Nivel5()
		self.prox_escena = None
		self.map =[ "#########################",
					"#-----------------------#",
					"#------------L----------#",
					"#-----------##----------#",
					"#-------P-B---T-X##--####",
					"#-------####--#-##-----##",
					"#---------------##-------",
					"#-----------T---##-X-X---",
					"#E----------#---##-#-#---",
					"##------------T-##-----S-",
					"#--P##--##----#-##--#--##",
					"#XX###XXX#X##XXXX#XXX#---",
					"#########################"] 




class Nivel5(Nivel):
	def __init__(self):
		Nivel.__init__(self)
		self.prox_nivel  = None
		self.prox_escena = None
		self.map =[ "#########################",
					"#-----------------------#",
					"#-----------------------#",
					"#-----------------------#",
					"#-----------------------#",
					"#-----------------------#",
					"#-----------------------#",
					"#-----------------------#",
					"#-----------------------#",
					"#-----------------------#",
					"#------------------------",
					"#E-L-------------------S-",
					"#########################"] 