import pygame                   # Stellt Objekte und Konstanten zur Spielprogrammierung zur Verfügung
import os
import random

class Settings(object):
    width = 700
    height = 400
    fps = 60
    title = "Sipher"
    file_path = os.path.dirname(os.path.abspath(__file__))
    images_path = os.path.join(file_path, "images")
    bordersize = 1

    @staticmethod
    def get_dim():
        return (Settings.width, Settings.height)

class Fighter(pygame.sprite.Sprite):
    def __init__(self, pygame):
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.images_path, "Fighter1.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (70, 64))
        self.rect = self.image.get_rect()
        self.rect.left = (Settings.width - self.rect.width) // 2
        self.rect.top = Settings.height - self.rect.height - 10
        self.direction = 0
        self.speed = 2
        self.space = False

    def update(self):
        # Steuerung mit Pfeiltasten in richtung oben,unten,links,rechts
        if pygame.key.get_pressed()[pygame.K_LEFT] == True:
           self.rect.left -= self.speed

        if pygame.key.get_pressed()[pygame.K_RIGHT] == True:
            self.rect.left += self.speed

        if pygame.key.get_pressed()[pygame.K_UP] == True:
           self.rect.top -= self.speed

        if pygame.key.get_pressed()[pygame.K_DOWN] == True:
            self.rect.top += self.speed

        # Die Spieler Figur wird an einen zufälligen ort teleportiert im bereich des Fensters
        if pygame.key.get_pressed()[pygame.K_SPACE] == True:
            self.space = True
        if pygame.key.get_pressed()[pygame.K_SPACE] == False and self.space == True:
            self.rect.top = random.randrange(0, Settings.height - self.rect.height)
            self.rect.left = random.randrange(0, Settings.width - self.rect.width)
            self.space = False    

        # Spielebegrenzung 
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= Settings.width:
            self.rect.right = Settings.width
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= Settings.height:
            self.rect.bottom = Settings.height


class Game(object):
    def __init__(self):
        self.screen = pygame.display.set_mode(Settings.get_dim())
        pygame.display.set_caption(Settings.title)
        self.background = pygame.image.load(os.path.join(Settings.images_path, "background.png")).convert()
        self.background = pygame.transform.scale(self.background, (Settings.width, Settings.height))
        self.background_rect = self.background.get_rect()

        self.all_Fighters = pygame.sprite.Group()
        self.Fighter = Fighter(pygame)
        self.all_Fighters.add(self.Fighter)

        self.clock = pygame.time.Clock()
        self.done = False

    def run(self):
        while not self.done:             # Hauptprogrammschleife mit Abbruchkriterium   
            self.clock.tick(Settings.fps)          # Setzt die Taktrate auf max 60fps    
            for event in pygame.event.get():    # Durchwandere alle aufgetretenen  Ereignisse
                if event.type == pygame.QUIT:   # Wenn das rechts obere X im Fenster geklickt
                    self.done = True                 # Flag wird auf Ende gesetzt            
                    
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.Fighter.direction = 0
                    elif event.key == pygame.K_RIGHT:
                        self.Fighter.direction = 0
                      

            self.all_Fighters.update()


            self.screen.blit(self.background, self.background_rect)
            self.all_Fighters.draw(self.screen)
            
            pygame.display.flip()   # Aktualisiert das Fenster




if __name__ == '__main__':      #                      
    pygame.init()               # Bereitet die Module zur Verwendung vor  
    game = Game()
    game.run()
    pygame.quit()               # beendet pygame