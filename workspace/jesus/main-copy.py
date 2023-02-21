import pygame
import random
import sys
from pyo import *
import time
COLOR_NEGRO = (0,0,0)
COLOR_BLANCO = (255,255,255)

PANTALLA_ANCHO = 1280
PANTALLA_ALTO = 720

JUGADOR_POSX = 600
JUGADOR_POSY = 550
JUGADOR_ANCHO = 150
JUGADOR_ALTO = 150
JUGADOR_COLOR = (210,255,255)
JUGADOR_DESPLAZAMIENTO = 1

INTERVALO_NUEVO_BLOQUE = random.randint(500,1500)

JUGADOR_IMG_URL = "workspace/jesus/img/caja.png"
BLOQUES_IMGS = ["img/moneda-01.png", "img/moneda-02.png", "img/moneda-03.png"]
FONDO_IMG_URL = "workspace/jesus/img/fondo.jpg"

LOGOTIPO_URL = "img/logotipo.png"


class Bloque(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        BLOQUE_IMG_URL = BLOQUES_IMGS[random.randint(0,2)]
        self.image = pygame.image.load(BLOQUE_IMG_URL).convert()
        self.image.set_colorkey(COLOR_NEGRO)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, PANTALLA_ANCHO - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.veloc_x = random.randrange(-1,1)
        self.veloc_y = 1

        self.numero = random.randint(1,144)
        self.texto = str(self.numero)
        self.font = pygame.font.SysFont("Arial", 40, bold=True)
        self.textSurf = self.font.render(self.texto, 1, COLOR_BLANCO)
        W = self.textSurf.get_width()
        H = self.textSurf.get_height()
        self.image.blit(self.textSurf, [self.rect.width/2 - W/2, self.rect.height/2 - H/2])

    """
	def update(self):
		self.rect.y += self.speedy
		self.rect.x += self.speedx
		if self.rect.top > HEIGHT + 10 or self.rect.left < -40 or self.rect.right > WIDTH + 40:
			self.rect.x = random.randrange(PANTALLA_ANCHO - self.rect.width)
			self.rect.y = random.randrange(-140, - 100)
			self.speedy = random.randrange(1, 10)
    """
    def update(self):
        self.rect.x = self.rect.x + self.veloc_x
        self.rect.y = self.rect.y + self.veloc_y
        #if self.rect.top > PANTALLA_ALTO:

        # Validacion previa
        if self.rect.x + self.veloc_x < 0:
            self.veloc_x = -self.veloc_x
        if self.rect.x + JUGADOR_ANCHO + self.veloc_x > PANTALLA_ANCHO:
            self.veloc_x = -self.veloc_x
            

class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(JUGADOR_IMG_URL).convert()
        self.image.set_colorkey(COLOR_NEGRO)
        self.rect = self.image.get_rect()
        self.rect.centerx = PANTALLA_ANCHO/2
        self.rect.bottom = PANTALLA_ALTO
        self.veloc_x = random.randrange(-5,5)
        self.direccion = 0
        self.desplazamiento = 4

    def asignar(self):
        self.numero = random.randint(2,2)
        self.texto = str(self.numero)
        self.font = pygame.font.SysFont("Arial", 60, bold=True)
        self.textSurf = self.font.render(self.texto, 1, COLOR_BLANCO)
        W = self.textSurf.get_width()
        H = self.textSurf.get_height()
        self.image.blit(self.textSurf, [self.rect.width/2 - W/2, self.rect.height/2 - H/3])

        self.textSurf = self.font.render("°", 1, COLOR_BLANCO)
        W = self.textSurf.get_width()
        H = self.textSurf.get_height()
        self.image.blit(self.textSurf, [self.rect.width/2 - W/2, self.rect.height/2 - 2*H/3])

    def girar(self):
        """
        last_rect_centerx = self.rect.centerx
        last_rect_bottom = self.rect.bottom
        if self.direccion == -1:
            self.image = pygame.image.load(JUGADOR_IZQ_IMG_URL).convert()
            self.image.set_colorkey(COLOR_NEGRO)
            self.rect = self.image.get_rect()
            self.rect.centerx = last_rect_centerx
            self.rect.bottom = last_rect_bottom

        elif self.direccion == 1:
            self.image = pygame.image.load(JUGADOR_DER_IMG_URL).convert()
            self.image.set_colorkey(COLOR_NEGRO)
            self.rect = self.image.get_rect()
            self.rect.centerx = last_rect_centerx
            self.rect.bottom = last_rect_bottom
        """
        pass

    def update(self):
        self.girar()

        # Validacion previa
        if self.rect.x + self.direccion*self.desplazamiento < 0:
            self.rect.x = 0
            self.direccion = 1
        if self.rect.x + JUGADOR_ANCHO + self.direccion*self.desplazamiento > PANTALLA_ANCHO:
            self.rect.x = PANTALLA_ANCHO - JUGADOR_ANCHO
            self.direccion = -1
       
        

        # Movimiento
        self.rect.x = self.rect.x + self.direccion*self.desplazamiento

        
        

class Juego:
    def __init__(self, ancho, alto):
        self.ancho = ancho
        self.alto = alto
        self.pantalla = pygame.display.set_mode([ancho, alto])
        self.finalizado = False

        self.sprites_lista = pygame.sprite.Group()
        self.bloques_correctos = pygame.sprite.Group()
        self.bloques_incorrectos = pygame.sprite.Group()

        self.jugador = Jugador()
        self.sprites_lista.add(self.jugador)

        self.vidas = 3
        self.tiempo = 30 # segundos
        self.puntos = 0
        self.aciertos = 0
        self.errores = 0
        
        self.clock = pygame.time.Clock()

        pygame.init()

        self.jugador.asignar()
        self.fondo = pygame.image.load(FONDO_IMG_URL)

        


        self.logotipo = pygame.image.load(LOGOTIPO_URL)




    def iniciar(self):
        pygame.display.set_caption("MateGame")
        self.ultimo_bloque = pygame.time.get_ticks()

        # /// AUDIO /// 

        # encendemos el servidor de audio
        s = Server(sr=48000, buffersize=256, duplex=0, winhost="wasapi").boot().start()

        # declaracion del efecto de sonido
        fx_env = Adsr(attack=0.01, decay=0.1, sustain=0.0, release=0.0, dur=0.5, mul=1)
        fx_osc = LFO(type = 4)

        # notas de la escala C# mayor (Hz)
        scale = [i*0.5 for i in [277.18, 311.13, 349.23, 369.99, 415.30, 466.16, 523.25, 554.37, 622.25, 698.46, 739.99, 830.61, 932.33, 1046.5]]

        # rellenar un array llamado "indices" con los indices de "scale"
        indices = []
        for i in range(0, len(scale)):
            indices.append(i)

        # seleccion aleatoria de la frecuencia de eleccion de nota
        arp_freq = Choice(choice = [2, 2, 4, 4, 4, 6], freq = 2)

        # seleccion aleatoria de indices de "scale"
        arp_nota = Choice(choice=indices, freq=arp_freq)

        tecera = Choice(choice=[0, 0, 0, 0, 0, 0, 0, 2], freq=arp_freq)

        # síntesis de pluck
        pluck_env = Tanh(-Log(LFO(freq=arp_freq, type=0).range(0,1)/arp_freq)/4)
        pluck_dry = LFO(freq = [100, 200], mul=pluck_env*0.1)
        pluck_wet = Biquad(pluck_dry, freq=pluck_env*2000, q=-(10 + pluck_env), type=0)
        pluck_out = pluck_wet.mix(1).mix(2).out()

        # //////////////

        while self.finalizado == False:
            # Texto en la pantalla
            #self.pantalla.fill(COLOR_BLANCO)

            # /// AUDIO /// 

            # actualizamos la frecuencia de la nota

            if int(arp_nota.get()) > len(scale) - 2:
                tecera.setChoice([0, 0, 0, 0, 0, 0, 0, 2 - len(scale)])

            pluck_dry.setFreq([scale[int(arp_nota.get())], scale[int(arp_nota.get() + tecera.get())]])
            

            # //////////////
            
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.finalizado = True
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_LEFT:
                        self.jugador.direccion = -1
                        
                    if evento.key == pygame.K_RIGHT:
                        self.jugador.direccion = 1

    
            #self.pantalla.fill(COLOR_BLANCO)

            # Realizar movimiento
            self.sprites_lista.update()
            
            self.ahora = pygame.time.get_ticks()
            if self.ahora - self.ultimo_bloque > INTERVALO_NUEVO_BLOQUE:
                bloque = Bloque()
                if bloque.numero % self.jugador.numero == 0:
                    self.bloques_correctos.add(bloque)
                else:
                    self.bloques_incorrectos.add(bloque)
                self.sprites_lista.add(bloque)
                

                self.ultimo_bloque = pygame.time.get_ticks()
            """
            aleatorio = random.randint(1,100)
            if aleatorio == 100:
                bloque = Bloque()
                self.sprites_lista.add(bloque)
            """

            hits = pygame.sprite.spritecollide(self.jugador, self.bloques_correctos, True)
            for hit in hits:
                self.aciertos = self.aciertos + 1

                # reproducir efecto de acierto
                fx_osc.setMul(0.25*fx_env)
                fx_osc.setFreq(440 - 700*fx_env)
                fx_hit_out = fx_osc.mix(2).out()
                fx_env.play()


            hits = pygame.sprite.spritecollide(self.jugador, self.bloques_incorrectos, True)
            for hit in hits:
                self.errores = self.errores + 1

                # reproducir efecto de fallo
                fx_osc.setMul(0.08*fx_env)
                fx_osc.setFreq(700 + 300*fx_env)
                fx_hit_out = fx_osc.mix(2).out()
                fx_env.play()
                

            self.pantalla.blit(self.fondo, [0, 0])

            self.sprites_lista.draw(self.pantalla)

            # Dibujar informacion

            # self.pantalla.blit(self.logotipo, (PANTALLA_ANCHO/2-self.logotipo.get_rect().width/2,40))

            self.fuente_informacion = pygame.font.SysFont("OCR-A Extended", 25)
            self.fuente_grande = pygame.font.SysFont("OCR-A Extended", 100)
            texto_aciertos = self.fuente_informacion.render("Aciertos: "+str(self.aciertos), 1, COLOR_BLANCO)
            texto_aciertos_rect = texto_aciertos.get_rect()
            self.pantalla.blit(texto_aciertos, (40,40))

            texto_reto = self.fuente_informacion.render("Captura los múltiplos de", 1, COLOR_BLANCO)
            texto_reto_2 = self.fuente_grande.render(str(self.jugador.numero), 1, COLOR_BLANCO)
            texto_reto_rect = texto_reto.get_rect()
            self.pantalla.blit(texto_reto, (PANTALLA_ANCHO/2-texto_reto_rect.width/2,150))
            self.pantalla.blit(texto_reto_2, (PANTALLA_ANCHO/2-texto_reto_2.get_rect().width/2,180))
            
            texto_errores = self.fuente_informacion.render("Errores: "+str(self.errores), 1, COLOR_BLANCO)
            texto_errores_rect = texto_errores.get_rect()
            self.pantalla.blit(texto_errores, (PANTALLA_ANCHO-40-texto_errores_rect.width,40))


            #self.clock.tick(600)

            pygame.display.flip()

            #pygame.time.wait(50)
        pygame.quit()

if __name__== "__main__" :
    j = Juego(PANTALLA_ANCHO, PANTALLA_ALTO)
    j.iniciar()

s.stop()



"""
python -m venv env
.\env\Scripts\activate
pip install mediapipe
pip install opencv_python
pip install pygame
pip freeze > requirements.txt
pip install -r requirements.txt
"""
