import pygame, random

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class Player(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height):
        super().__init__() # Esto llama al constructor de la clase padre (Sprite)
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.image = pygame.image.load("img/caja.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = self.screen_width/2 - self.rect.width/2
        self.rect.y = self.screen_height - self.rect.height
        self.speed_x = 0
        self.speed_y = 0
    
    def update(self):
        # Ver que no se salga de los limites de la pantalla (rebote)
        if self.rect.x + self.speed_x < 0 or self.screen_width - self.rect.width < self.rect.x + self.speed_x:
            self.speed_x = -self.speed_x
        # Realizacion del movimiento
        self.rect.x = self.rect.x + self.speed_x

class Coin(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height):
        super().__init__() # Esto llama al constructor de la clase padre (Sprite)
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.image = pygame.image.load("img/moneda-01.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, self.screen_width - self.rect.width)
        self.rect.y = 0
        self.speed_x = 2*random.randint(-1, 1)
        self.speed_y = 2
    
    def update(self):
        # Ver que no se salga de los limites de la pantalla (rebote)
        if self.rect.x + self.speed_x < 0 or self.screen_width - self.rect.width < self.rect.x + self.speed_x:
            self.speed_x = -self.speed_x
        # Realizacion del movimiento
        self.rect.x = self.rect.x + self.speed_x
        self.rect.y = self.rect.y + self.speed_y

class Game:
    def __init__(self):
        pygame.init()

        self.screen_width = 1280
        self.screen_height = 720
        self.screen = pygame.display.set_mode([self.screen_width, self.screen_height])

        self.backgroung = pygame.image.load("img/fondo-01.jpg")
        self.clock = pygame.time.Clock() # Reloj que permitira manipular los fps
        
        
        self.coin_sound = pygame.mixer.Sound("sound/coin.ogg")
        self.sound = pygame.mixer.Sound("sound/coin.ogg")
        self.sound = pygame.mixer.Sound("sound/coin.ogg")
        

        self.coin_list = pygame.sprite.Group() # Lista que contiene los coins que caeran. Se usara para detectar colisiones
        self.sprite_list = pygame.sprite.Group() # Lista que contiene todos los sprites (coins y el player). Se usara para dibujarlas

        self.player = Player(self.screen_width, self.screen_height) # Jugador
        self.sprite_list.add(self.player) # Se agrega el player a la lista de sprites del juego

        self.time = 10
        self.score = 0

        self.started = True # None
        self.game_over = None

    def pause_motion(self):
        for element in self.sprite_list:
            element.speed_x = 0
            element.speed_y = 0

    def create_coins(self):
        if random.randint(1,100) == 50: # Genero un alewtorio entre 1 y 100, y si sale 50, genero un nuevo coin
            coin = Coin(self.screen_width, self.screen_height)
            self.coin_list.add(coin) # Se agrega el coin a la lista de coins del juego
            self.sprite_list.add(coin) # Se agrega el coin a la lista de sprites del juego
    
    def process_events(self):
        # Capturar los eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Terminar cuando cierre la pantalla
                self.started = False
            if event.type == pygame.KEYDOWN: # Verifica si se presiono una tecla
                if event.key == pygame.K_LEFT:
                    self.player.speed_x = - 10
                if event.key == pygame.K_RIGHT:
                    self.player.speed_x = 10
                if event.key == pygame.K_RETURN: # Si el juego ha terminado permite presionar ENTER para continuar
                    if self.game_over != None:
                        self.__init__()
    
    def run_logic(self):
        if self.started == True:
            # Actualizar la posicion de todos los sprites
            self.sprite_list.update()

            # Detectar colisiones
            coins_hit_list = pygame.sprite.spritecollide(self.player, self.coin_list, True)

            for coin in coins_hit_list:
                self.sprite_list.remove(coin)
                self.score = self.score + 1
                self.coin_sound.play()
            
            # Actualizamos el tiempo
            self.time = self.time-0.01

            # Detectar si gana o pierde
            if int(self.time) > 0: # Si el tiempo es mayor a cero
                if self.score >= 2: # Verificar si el score es 30 o mas, en ese caso gana
                    self.game_over = False
            else: # Si el tiempo llega a cero, habra perdido
                self.game_over = True

    def display_frame(self):
        if self.game_over == None:
            self.screen.blit(self.backgroung, [0, 0])
            self.sprite_list.draw(self.screen)
            self.display_info()

            
        else:
            # Limpiar pantalla
            #self.screen.fill(WHITE)
            self.pause_motion()

            if self.game_over == False:
                font = pygame.font.SysFont("Arial", 50) # Fuente con que se va a dibujar
                text = font.render("Felicitaciones, ganaste :)", True, BLACK) # Texto que se va a dibujar
                # Posicion del texto centrada en x e y
                text_x = self.screen_width/2 - text.get_width()/2
                text_y = self.screen_height/2 - text.get_height()/2
                self.screen.blit(text, [text_x, text_y])
                
            if self.game_over == True:
                font = pygame.font.SysFont("Arial", 50) # Fuente con que se va a dibujar
                text = font.render("Perdiste, vuelve a intentarlo", True, BLACK) # Texto que se va a dibujar
                # Posicion del texto centrada en x e y
                text_x = self.screen_width/2 - text.get_width()/2
                text_y = self.screen_height/2 - text.get_height()/2
                self.screen.blit(text, [text_x, text_y])
        
        pygame.display.flip()  
        
    
    def display_info(self):
        self.font = pygame.font.SysFont('Showcard Gothic', 30, bold=False)
        score_text = self.font.render("Puntos: "+str(self.score), True, BLACK)
        time_text = self.font.render("Tiempo: "+str(int(self.time)), True, BLACK)

        self.screen.blit(score_text, (10, 10))
        self.screen.blit(time_text, (self.screen_width - time_text.get_width(), 10))
    
    def run(self):
        
        
        while self.started == True:
            self.create_coins()
            self.process_events()
            self.run_logic()
            self.display_frame()
            self.display_info()
            self.clock.tick(60) # 60 fps
        pygame.quit()

g = Game()
g.run()