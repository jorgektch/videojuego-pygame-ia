import pygame, random

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() # Esto llama al constructor de la clase padre (Sprite)
        self.image = pygame.image.load("caja.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.speed_x = 0
        self.speed_y = 0
    
    def update(self, screen_width):
        # Ver que no se salga de los limites de la pantalla (rebote)
        if self.rect.x + self.speed_x < 0 or screen_width - self.rect.width < self.rect.x + self.speed_x:
            self.speed_x = -self.speed_x
        # Realizacion del movimiento
        self.rect.x = self.rect.x + self.speed_x

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() # Esto llama al constructor de la clase padre (Sprite)
        self.image = pygame.image.load("moneda-01.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.speed_x = 0
        self.speed_y = 0
    
    def update(self, screen_width, screen_height):
        # Ver que no se salga de los limites de la pantalla (rebote)
        if self.rect.x + self.speed_x < 0 or SCREEN_WIDTH - self.rect.width < self.rect.x + self.speed_x:
            self.speed_x = -self.speed_x
        # Realizacion del movimiento
        self.rect.x = self.rect.x + self.speed_x
        self.rect.y = self.rect.y + self.speed_y

class Game:
    def __init__(self):
        self.screen_width = 1280
        self.screen_height = 720
        self.screen = pygame.display.set_mode([screen_width, screen_height])

        self.backgroung = pygame.image.load("fondo-01.png")
        self.clock = pygame.time.Clock() # Reloj que permitira manipular los fps

        self.coin_list = pygame.sprite.Group() # Lista que contiene los coins que caeran. Se usara para detectar colisiones
        self.sprite_list = pygame.sprite.Group() # Lista que contiene todos los sprites (coins y el player). Se usara para dibujarlas

        self.player = Player() # Jugador
        self.sprite_list.add(self.player) # Se agrega el player a la lista de sprites del juego

        self.score = 0

        self.started = True # None
        self.game_over = None

    def create_coins(self):
        if random.randint(1,100) == 50: # Genero un alewtorio entre 1 y 100, y si sale 50, genero un nuevo coin
            coin = Coin()
            self.coin_list.add(coin) # Se agrega el coin a la lista de coins del juego
            self.sprite_list.add(coin) # Se agrega el coin a la lista de sprites del juego
    
    def display_frame(self):
        if self.started == True:
            self.screen.blit(self.backgroung, [0, 0])
            self.all_sprites_list.draw(self.screen)
        else:
            # Limpiar pantalla
            self.screen.fill(WHITE)
            if self.win == True:
                font = pygame.font.SysFont("Arial", 50) # Fuente con que se va a dibujar
                text = font.render("Felicitaciones, ganaste :)", True, BLACK) # Texto que se va a dibujar
                # Posicion del texto centrada en x e y
                text_x = SCREEN_WIDTH/2 - text.get_width()/2
                text_y = SCREEN_HEIGHT/2 - text.get_height()/2
                self.screen.blit(text, [text_x, text_y])
                time.sleep(3)
            if self.game_over == True:
                font = pygame.font.SysFont("Arial", 50) # Fuente con que se va a dibujar
                text = font.render("Perdiste, vuelve a intentarlo", True, BLACK) # Texto que se va a dibujar
                # Posicion del texto centrada en x e y
                text_x = SCREEN_WIDTH/2 - text.get_width()/2
                text_y = SCREEN_HEIGHT/2 - text.get_height()/2
                self.screen.blit(text, [text_x, text_y])
                time.sleep(3)