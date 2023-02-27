import pygame, random
from webcam import Webcam
import mediapipe as mp
import math
import cv2

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Ancho y alto de la pantalla
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# Valores por defectos en el juego
GAME_DURATION = 30 # Duracion del juego, en segundos
TOP_SCORE = 10 # Score maximo con el que el jugador gana
GRAVITY = 2 # Gravedad. Que permitira saltos

THING_SPEED_Y_MIN = 2
THING_SPEED_Y_MAX = 4

PLAYER_NUMBER_MIN = 2
PLAYER_NUMBER_MAX = 2

# Archivos de imagenes
BACKGROUND_IMG = "img/fondo-01.jpg" # Imagen de fondo
PLAYER_IMG = "img/jugador.png" # Jugador normal
PLAYER_IMG_SAD = "img/jugador-sad.png" # Jugador feliz
PLAYER_IMG_HAPPY = "img/jugador-happy.png" # Jugador triste
THINGS_IMG_LIST = ["img/moneda-01.png", "img/moneda-02.png", "img/moneda-03.png"] # Lista de things (se elegiran aleatoriamente)

# Archivos de musica (deben estar en formato WAV)
GAME_MUSIC = "music/music.wav" # Musica de fondo del juego
GAME_MUSIC_WINNER = "music/winner.wav" # Musica para cuando el jugador gane
GAME_MUSIC_GAMEOVER = "music/gameover.wav" # Musica para cuando el jugador pierda

# Archivos de sonido (deben estar en formato OGG)
MOTION_SOUND = "sound/motion.ogg" # Sonido de movimiento
PUNCH_SOUND = "sound/coin.ogg" # Sonido de golpe
ERROR_SOUND = "sound/error.ogg" # Sonido de error

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() # Esto llama al constructor de la clase padre (Sprite)
        self.image = pygame.image.load(PLAYER_IMG).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH/2 - self.rect.width/2
        self.rect.y = SCREEN_HEIGHT - self.rect.height
        self.speed_x = 0
        self.speed_y = 0
    
    def update(self):
        # Cambio de velicidad en el eje Y producto de la gravedad (para que caiga cuando salta)
        if self.rect.x <  SCREEN_WIDTH - self.rect.width:
            self.speed_y = self.speed_y + GRAVITY
        
        # Ver que no se salga de los limites de la pantalla en el eje X
        if self.rect.x + self.speed_x < 0 or SCREEN_WIDTH - self.rect.width < self.rect.x + self.speed_x:
            self.speed_x = -self.speed_x
        
        # Ver que no se salga de los limites de la pantalla en el eje Y
        if SCREEN_HEIGHT - self.rect.height < self.rect.y + self.speed_y:
            self.speed_y = 0
        
        # Realizacion del movimiento
        self.rect.x = self.rect.x + self.speed_x
        self.rect.y = self.rect.y + self.speed_y
    
    def be_sad(self):
        self.image = pygame.image.load(PLAYER_IMG_SAD).convert_alpha()

    def be_happy(self):
        self.image = pygame.image.load(PLAYER_IMG_HAPPY).convert_alpha()

    def assign_number(self):
        self.number = random.randint(PLAYER_NUMBER_MIN, PLAYER_NUMBER_MAX)
        font = pygame.font.SysFont("Arial", 60, bold=True)

        number_text = font.render(str(self.number), 1, WHITE)
        W = number_text.get_width()
        H = number_text.get_height()
        self.image.blit(number_text, [self.rect.width/2 - W/2, self.rect.height/2 - H/3])

        symbol_text = font.render("°", 1, WHITE)
        W = symbol_text.get_width()
        H = symbol_text.get_height()
        self.image.blit(symbol_text, [self.rect.width/2 - W/2, self.rect.height/2 - 2*H/3])

class Thing(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() # Esto llama al constructor de la clase padre (Sprite)
        self.image = pygame.image.load(random.choice(THINGS_IMG_LIST)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = 0
        self.speed_x = 3*random.randint(-1, 1)
        self.speed_y = random.randint(THING_SPEED_Y_MIN, THING_SPEED_Y_MIN)
    
    def update(self):
        # Ver que no se salga de los limites de la pantalla en el eje X
        if self.rect.x + self.speed_x < 0 or SCREEN_WIDTH - self.rect.width < self.rect.x + self.speed_x:
            self.speed_x = -self.speed_x
        
        # Ver que no se salga de los limites de la pantalla en el eje Y
        if SCREEN_HEIGHT - self.rect.width < self.rect.y + self.speed_y:
            self.rect.y = SCREEN_HEIGHT - self.rect.width
            self.speed_y = 0
        # Realizacion del movimiento
        self.rect.x = self.rect.x + self.speed_x
        self.rect.y = self.rect.y + self.speed_y
    
    def hit_the_ground(self):
        if self.rect.y == SCREEN_HEIGHT - self.rect.width:
            return True
        else:
            return False
    
    def assign_number(self):
        self.number = random.randint(1,144)
        font = pygame.font.SysFont("Arial", 40, bold=True)

        number_text = font.render(str(self.number), 1, WHITE)
        W = number_text.get_width()
        H = number_text.get_height()
        self.image.blit(number_text, [self.rect.width/2 - W/2, self.rect.height/2 - H/2])

class Game:
    def __init__(self):
        pygame.init() # Se inicializa pygame
        pygame.display.set_caption("Juego de ejemplo") # Cambiar el nombre del juego

        self.screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        self.backgroung = pygame.image.load(BACKGROUND_IMG)
        self.clock = pygame.time.Clock() # Reloj que permitira manipular los fps

        self.correct_thing_list = pygame.sprite.Group() # Lista que contiene los things correctos. Se usara para detectar colisiones
        self.incorrect_thing_list = pygame.sprite.Group() # Lista que contiene los things incorrectos. Se usara para detectar colisiones
        self.sprite_list = pygame.sprite.Group() # Lista que contiene todos los sprites (things y el player). Se usara para dibujarlas

        self.player = Player()
        self.player.assign_number() # Se le asigna el numero
        self.sprite_list.add(self.player) # Se agrega el player a la lista de sprites del juego

        self.time = GAME_DURATION+1 # Tiempo de duracion del juego
        self.score = 0 # Puntaje del jugador

        self.started = True # Indica si el juego ha iniciado o terminado
        self.game_over = None # Indica si perdio. None significa que no tiene valor asignado

        self.collision_sound = pygame.mixer.Sound(PUNCH_SOUND)
        self.motion_sound = pygame.mixer.Sound(MOTION_SOUND)
        self.error_sound = pygame.mixer.Sound(ERROR_SOUND)

        pygame.mixer.music.load(GAME_MUSIC)
        pygame.mixer.music.play(-1)

        # Facemesh de mediapipe
        self.mp_face_mesh = mp.solutions.face_mesh
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles

        # Uso de webcam
        self.webcam = Webcam().start() # Inicializacion de la camara
        self.max_face_surf_height = 0
        self.face_left_x = 0
        self.face_right_x = 0
        self.face_top_y = 0
        self.face_bottom_y = 0
    
    def create_things(self):
        if self.game_over == None: # Verifica si el jugador aun no ha perdido ni ganado
            if random.randint(1, 50) == 50: # Genero un aleatorio entre 1 y 100; y si sale 50 creo un thing que caera
                thing = Thing()
                thing.assign_number()
                self.sprite_list.add(thing) # Se agrega el thing a la lista de sprites del juego (que contiene thing y al jugador)
                
                # Se verifica a cual lista de thing se agregara (correct o incorrect)
                if self.is_correct(thing) == True:
                    self.correct_thing_list.add(thing)
                else:
                    self.incorrect_thing_list.add(thing)

    def process_events(self):
        for event in pygame.event.get(): # Captura los eventos para analizarlos
            if event.type == pygame.QUIT: # Verifica si el usuario cierra la pantalla
                self.started = False
            if event.type == pygame.KEYDOWN: # Verifica si presiona una tecla
                # Se analiza primero, el caso en que el jugador no ha ganado ni perdido (game_over = None)
                if self.game_over == None: 
                    if event.key == pygame.K_LEFT:
                        self.player.speed_x = -10
                        self.motion_sound.play() # Se reproduce el sonido de movimiento
                    if event.key == pygame.K_RIGHT:
                        self.player.speed_x = 10
                        self.motion_sound.play() # Se reproduce el sonido de movimiento
                    if event.key == pygame.K_SPACE:
                        self.player.speed_y = -20
                        self.motion_sound.play() # Se reproduce el sonido de movimiento
                else: # Aqui se analiza el caso contrario, es decir cuando gano o perdio. Solo debe esperar el ENTER del usuario
                    if event.key == pygame.K_RETURN: # Verifica si presiona ENTER
                        if self.game_over != None: # Verifica si el jugador ha perdido o ha ganado (diferente de None)
                            self.__init__()
    
    def is_correct(self, thing):
        if thing.number%self.player.number == 0:
            return True
        else:
            return False

    def detect_collisions(self):
        # Detectar colisiones correctas
            thing_hit_list = pygame.sprite.spritecollide(self.player, self.correct_thing_list, True)

            for thing in thing_hit_list:
                self.correct_thing_list.remove(thing) # Se elimina de la lista de things
                self.sprite_list.remove(thing) # Se elimina de la lista de sprites (things y player)

                self.score = self.score + 1 # Aumenta el puntaje
                self.collision_sound.play() # Reproduce el sonido de la colision

            # Detectar colisiones incorrectas
            thing_hit_list = pygame.sprite.spritecollide(self.player, self.incorrect_thing_list, True)

            for thing in thing_hit_list:
                self.incorrect_thing_list.remove(thing) # Se elimina de la lista de things
                self.sprite_list.remove(thing) # Se elimina de la lista de sprites (things y player)

                self.score = self.score - 1 # Aumenta el puntaje
                self.error_sound.play() # Reproduce el sonido de la colision

    def detect_fallen(self):
        # Eliminar los things correctos que cayeron al suelo
        for thing in self.correct_thing_list:
            if thing.hit_the_ground() == True:
                self.sprite_list.remove(thing) # Se elimina de la lista de sprites (things y player)
                self.correct_thing_list.remove(thing) # Se elimina de la lista de things

        # Eliminar los things incorrectos que cayeron al suelo
        for thing in self.incorrect_thing_list:
            if thing.hit_the_ground() == True:
                self.sprite_list.remove(thing) # Se elimina de la lista de sprites (things y player)
                self.incorrect_thing_list.remove(thing) # Se elimina de la lista de things

    def run_logic(self):
        if self.started == True: # Se verifica que el juego este iniciado

            # Actualizamos la posicion de todos los sprites
            self.sprite_list.update()

            self.detect_collisions() # Se detectan colisiones
            self.detect_fallen() # Se detectan things que cayeron al suelo

            # Se asegura que el puntaje no baje de cero (no hay puntaje negativo)
            if self.score < 0:
                self.score = 0

            # Si el jugador aun no ha ganado o perdido, verificamos que le pasa
            if self.game_over == None:
                self.time = self.time - 0.02 # Actualizamos el tiempo

                # Detecto si gana o pierde
                if int(self.time) > 0: # Si el tiempo es mayor a cero (tiene tiempo)
                    if self.score >= TOP_SCORE: # Verifica si el score es 3 o mas, en ese caso gana
                        self.game_over = False # No ha perdido, es decir ha ganado
                        # Se reproduce sonido de game over
                        pygame.mixer.music.load(GAME_MUSIC_WINNER)
                        pygame.mixer.music.play(-1)
                        # Se cambia la imagen del jugador ALEGRE
                        self.player.be_happy()
                else:
                    self.game_over = True # Ha perdido
                    # Se reproduce sonido de game over
                    pygame.mixer.music.load(GAME_MUSIC_GAMEOVER)
                    pygame.mixer.music.play(-1)
                    # Se cambia la imagen del jugador TRISTE
                    self.player.be_sad()
    
    def display_info(self):
        font = pygame.font.SysFont('Showcard Gothic', 30, bold=False)
        score_text = font.render("Puntos: "+str(self.score)+" / "+str(TOP_SCORE), True, BLACK)
        time_text = font.render("Tiempo: "+str(int(self.time)), True, BLACK)

        self.screen.blit(score_text, (20, 20))
        self.screen.blit(time_text, (SCREEN_WIDTH - time_text.get_width() - 20, 20))

    def pause_motion(self):
        for sprite in self.sprite_list:
            sprite.speed_x = 0
            sprite.speed_y = 0
        
        for thing in self.correct_thing_list:
            sprite.speed_x = 0
            sprite.speed_y = 0

        for thing in self.incorrect_thing_list:
            sprite.speed_x = 0
            sprite.speed_y = 0
    
    def display_frame(self):
        self.screen.blit(self.backgroung, [0, 0]) # Se dibuja el fondo
        self.sprite_list.draw(self.screen) # Se dibujan todos los srpites
        # Se dibuja la camara
        if self.webcam.lastFrame is not None:
            self.render_camera()
        self.display_info() # Se dibujan los textos (puntos y tiempo)
        
        if self.game_over == False:
            font = pygame.font.SysFont('Showcard Gothic', 30, bold=True)
            text = font.render("Ganaste. Presiona ENTER para continuar", True, BLACK)
            # Posicion del texto
            text_x = SCREEN_WIDTH/2 - text.get_width()/2
            text_y = SCREEN_HEIGHT/2 - text.get_height()/2
            self.screen.blit(text, [text_x, text_y])

            # Se pausa el movimiento para todos los elementos del juego
            self.pause_motion()
        elif self.game_over == True:
            font = pygame.font.SysFont('Showcard Gothic', 30, bold=True)
            text = font.render("Perdiste. Presiona ENTER para continuar", True, BLACK)
            # Posicion del texto
            text_x = SCREEN_WIDTH/2 - text.get_width()/2
            text_y = SCREEN_HEIGHT/2 - text.get_height()/2
            self.screen.blit(text, [text_x, text_y])

            # Se pausa el movimiento para todos los elementos del juego
            self.pause_motion()

        pygame.display.flip() # Actualizar el display

    def process_camera(self, face_mesh):
        image = self.webcam.read()
        if image is not None:
            image.flags.writeable = False
            image = cv2.flip(image, 1)
            height, width, _ = image.shape
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            results = face_mesh.process(image)
            self.webcam_image = image
            if results.multi_face_landmarks is not None:
                for face_landmarks in results.multi_face_landmarks:
                    """
                    #Coordenadas de la cara (arriba y abajo)
                    top = (face_landmarks.landmark[10].x, face_landmarks.landmark[10].y)
                    bottom = (face_landmarks.landmark[152].x, face_landmarks.landmark[152].y)

                    #Obtener coordenadas del 'cuadrado' de la cara para poder mostrarlo en la pantalla despues
                    self.face_left_x = face_landmarks.landmark[234].x
                    self.face_right_x = face_landmarks.landmark[454].x
                    self.face_top_y = face_landmarks.landmark[10].y
                    self.face_bottom_y = face_landmarks.landmark[152].y

                    #Dejar algo de espacio alrededor
                    self.face_left_x = self.face_left_x - .1
                    self.face_right_x = self.face_right_x + .1
                    self.face_top_y = self.face_top_y - .1
                    self.face_bottom_y = self.face_bottom_y + .1

                    cv2.line(
                        self.webcam_image, 
                        (int(top[0] * self.webcam.width()), int(top[1] * self.webcam.height())),
                        (int(bottom[0] * self.webcam.width()), int(bottom[1] * self.webcam.height())),
                        (0, 255, 0), 3
                    )

                    cv2.circle(self.webcam_image, (int(top[0] * self.webcam.width()), int(top[1] * self.webcam.height())), 8, (0,0,255), -1)
                    cv2.circle(self.webcam_image, (int(bottom[0] * self.webcam.width()), int(bottom[1] * self.webcam.height())), 8, (0,0,255), -1)
                    """
                    x_sup = int(face_landmarks.landmark[10].x * width)
                    y_sup = int(face_landmarks.landmark[10].y * height)
                    
                    x_inf = int(face_landmarks.landmark[152].x * width)
                    y_inf = int(face_landmarks.landmark[152].y * height)

                    x_mean_vertical = int((x_sup + x_inf)/2)
                    y_mean_vertical = int((y_sup + y_inf)/2)

                    x_left = int(face_landmarks.landmark[234].x * width)
                    y_left = int(face_landmarks.landmark[234].y * height)

                    x_right = int(face_landmarks.landmark[454].x * width)
                    y_right = int(face_landmarks.landmark[454].y * height)

                    y_mean_horizontal = (y_right + y_left)/2

                    cv2.line(image, (x_sup, y_sup), (x_inf, y_inf), (255,0,0), 5)

                    cv2.circle(image, (x_sup, y_sup), 10, (255,0,255), -1)
                    cv2.circle(image, (x_inf, y_inf), 10, (255,0,255), -1)
                    cv2.circle(image, (x_mean_vertical, y_mean_vertical), 10, (255,0,255), -1)
                    cv2.circle(image, (x_left, y_left), 10, (255,0,255), -1)
                    cv2.circle(image, (x_right, y_right), 10, (255,0,255), -1)

                    cv2.line(image, (x_left, y_left), (x_right, y_right), (255,0,0), 5)

                    #Deteccion de angulo
                    radians = -math.atan2(y_sup-y_inf,x_sup-x_inf)
                    degrees = math.degrees(radians)
                    degrees = round(degrees)

                    self.detect_head_movement(degrees, y_mean_vertical, y_mean_horizontal)

            k = cv2.waitKey(1) & 0xFF

    def detect_head_movement(self, degrees, y_mean_vertical, y_mean_horizontal):
        """
        radians = math.atan2(bottom[1] - top[1], bottom[0] - top[0])
        degrees = math.degrees(radians)

        #Angulo de deteccion de 70 a 110 (-1 a 1)
        min_degrees = 70
        max_degrees = 110
        degree_range = max_degrees - min_degrees
        
        if degrees < min_degrees: degrees = min_degrees
        if degrees > max_degrees: degrees = max_degrees

        self.movement = ( ((degrees-min_degrees) / degree_range) * 2) - 1
        """

        if degrees < 85:
            self.player.speed_x = 20
        elif degrees > 95:
            self.player.speed_x = -20
        else:
            self.player.speed_x = 0


        if y_mean_vertical < y_mean_horizontal:
            self.player.speed_y = -20
        #else:
        #    dy = 0

    def render_camera(self):
        # Limpiar coordenadas del cuadro de la cara
        if self.face_left_x < 0: self.face_left_x = 0
        if self.face_right_x > 1: self.face_right_x = 1
        if self.face_top_y < 0: self.face_top_y = 0
        if self.face_bottom_y > 1: self.face_bottom_y = 1

        face_surf = pygame.image.frombuffer(self.webcam_image, (int(self.webcam.width()), int(self.webcam.height())), "BGR")
        """
        face_rect = pygame.Rect(
            int(self.face_left_x*self.webcam.width()),
            int(self.face_top_y*self.webcam.height()),
            int(self.face_right_x*self.webcam.width()) - int(self.face_left_x*self.webcam.width()),
            int(self.face_bottom_y*self.webcam.height()) - int(self.face_top_y*self.webcam.height())
        )
        
        only_face_surf = pygame.Surface((
            int(self.face_right_x*self.webcam.width()) - int(self.face_left_x*self.webcam.width()),
            int(self.face_bottom_y*self.webcam.height()) - int(self.face_top_y*self.webcam.height())
        ))
        only_face_surf.blit(face_surf, (0,0), face_rect)

        height = only_face_surf.get_rect().height
        width = only_face_surf.get_rect().width
        if width == 0:
            width = 1
        face_ratio = height / width
        face_area_width = 200
        face_area_height = face_area_width * face_ratio
        if (face_area_height > self.max_face_surf_height):
            self.max_face_surf_height = face_area_height
        only_face_surf = pygame.transform.scale(only_face_surf, (int(face_area_width),int(self.max_face_surf_height)))
        """
        height = face_surf.get_rect().height
        width = face_surf.get_rect().width
        face_ratio = height / width

        face_area_width = 200

        face_area_height = face_area_width * face_ratio

        face_surf = pygame.transform.scale(face_surf, (int(face_area_width),int(face_area_height)))
        self.screen.blit(face_surf, [SCREEN_WIDTH/2-face_area_height/2, 0])

    def run(self):
        """
        while self.started == True:
            self.create_things()
            self.process_events()
            self.run_logic()
            self.display_frame()
            self.display_info()
            self.clock.tick(60) # 60 fps
        pygame.quit()
        """
        with self.mp_face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            min_detection_confidence=0.5,
            refine_landmarks=True
        ) as face_mesh:
            while self.started == True:

                if self.game_over == None:
                    if not self.webcam.ready():
                        continue
                    self.process_camera(face_mesh)

                self.create_things()
                self.process_events()
                self.run_logic()
                self.display_frame()
                self.display_info()
                self.clock.tick(60) # 60 fps
            pygame.quit()

if __name__== "__main__" :
    g = Game()
    g.run()