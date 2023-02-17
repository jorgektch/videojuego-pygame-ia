# Importacion e inicializacion de la libreria
from threading import Thread
import cv2
import pygame
import mediapipe as mp

# Variables globales
pantalla_ancho = 1280
pantalla_alto = 720

class Webcam:
    def __init__(self):
        self.stopped = False
        self.stream = None
        self.lastFrame = None

    def start(self):
        t = Thread(target=self.update, args=())
        t.daemon = True
        t.start()
        return self

    def update(self):
        if self.stream is None:
            self.stream = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        while True:
            if self.stopped:
                return
            (result, image) = self.stream.read()
            if not result:
                self.stop()
                return
            self.lastFrame = image
                
    def read(self):
        return self.lastFrame

    def stop(self):
        self.stopped = True

    def width(self):
        return self.stream.get(cv2.CAP_PROP_FRAME_WIDTH )

    def height(self):
        return self.stream.get(cv2.CAP_PROP_FRAME_HEIGHT )
    
    def ready(self):
        return self.lastFrame is not None

class Bloque:
    def __init__(self, posx, posy, ancho, alto):
        self._posx = posx
        self._posy = posy
        self._ancho = ancho
        self._alto = alto

class Jugador:
    def __init__(self, posx, posy, ancho, alto, color, desplazamiento):
        self._posx = posx
        self._posy = posy
        self._ancho = ancho
        self._alto = alto
        self._color = color
        self._direccion = 0
        self._desplazamiento = desplazamiento
        self._elemento = None

class Juego:
    def __init__(self):
        #Facemesh
        self.mp_face_mesh = mp.solutions.face_mesh
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles

        pygame.init()
        pygame.display.set_caption("Misiles")

        #self.background = Background()
        #self.initialize()
        self.pantalla = pygame.display.set_mode([pantalla_ancho, pantalla_alto])

        self.inicializar()

    def iniciar(self):
        jugador = Jugador(20, 40, 100, 200, (255,0,0), 1)
        
        finalizado = False

        while not finalizado:

            # Did the user click the window close button?
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    finalizado = True
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_LEFT:
                        jugador._direccion = -1
                    if evento.key == pygame.K_RIGHT:
                        jugador._direccion = 1
            
            # Realizar movimiento
            if jugador._posx + jugador._desplazamiento*jugador._direccion < 0:
                jugador._direccion = -1*jugador._direccion
            if jugador._posx + jugador._ancho + jugador._desplazamiento*jugador._direccion > pantalla_ancho:
                jugador._direccion = -1*jugador._direccion

            jugador._posx = jugador._posx + jugador._desplazamiento*jugador._direccion


            # Fill the background with white
            self.pantalla.fill((10, 255, 255))


            jugador._elemento = pygame.Rect(jugador._posx, jugador._posy, jugador._ancho, jugador._alto)
            

            # Drawing Rectangle
            pygame.draw.rect(self.pantalla, jugador._color, jugador._elemento)

            # Flip the display
            pygame.display.flip()

        # Done! Time to quit.
        pygame.quit()

    def procesar_camara(self):
        image = self.webcam.read()
        if image is not None:
            image.flags.writeable = False
            image = cv2.flip(image, 1)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            results = self.face_mesh.process(image)
            self.webcam_image = image
            if results.multi_face_landmarks is not None:
                for face_landmarks in results.multi_face_landmarks:
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

                    #Deteccion de angulo
                    self.detect_head_movement(top, bottom)
            k = cv2.waitKey(1) & 0xFF

    def inicializar(self):
        self.webcam = Webcam().start()
        
        self.max_face_surf_height=0
        self.face_left_x = 0
        self.face_right_x = 0
        self.face_top_y = 0
        self.face_bottom_y = 0

j = Juego()
j.iniciar()