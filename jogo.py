import os
import random
import pygame
from pygame.locals import *

pygame.init()

SCREEN_WIDTH = 500 #LARGURA DA TELA
SCREEN_HEIGHT = 800 #ALTURA DA TELA
SPEED = 10 
GRAVITY = 1
GAME_SPEED = 10
GROUND_WIDTH = 2 * SCREEN_WIDTH
GROUND_HEIGHT = 100

PIPE_WIDTH = 80
PIPE_HEIGHT = 500

PIPE_GAPE = 200

class Bird(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) # imagem / dimensão do passaro
        self.SPRITE0 = pygame.image.load(os.path.join('imagens_game','sprite0.png')).convert_alpha()
        self.SPRITE1 = pygame.image.load(os.path.join('imagens_game','sprite1.png')).convert_alpha()
        self.SPRITE2 = pygame.image.load(os.path.join('imagens_game','sprite2.png')).convert_alpha()

        self.images = [
            self.SPRITE0, 
            self.SPRITE1, 
            self.SPRITE2
        ]

        self.speed = SPEED
        self.current_image = 0
        self.image = pygame.image.load(os.path.join('imagens_game','sprite0.png')).convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect[0] = SCREEN_WIDTH - 230            # Ponto de spaw do passaro? SIM
        self.rect[1] = SCREEN_HEIGHT - 460
        print(self.rect)

    def update(self): #pra atualizar as infortmações do jogo
        self.current_image = (self.current_image + 1) % 3 #Quando chegar a 3, o valor sera 0.
        self.image = self.images[self.current_image]

        self.speed += GRAVITY

        #Update Height
        self.rect[1] += self.speed #Velocidade de Queda

    def bump(self):
        self.speed =- SPEED


class Pipe(pygame.sprite.Sprite): #Classe do Cano

    def __init__(self, inverted, xpos, ysize): 
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(os.path.join('imagens_game', 'cano.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image, (PIPE_WIDTH, PIPE_HEIGHT))

        self.rect = self.image.get_rect()
        self.rect[0] = xpos

        if inverted: # Se Cano for Invertido...
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect[1] =- (self.rect[3] - ysize) # zero ou 1 ?
        else:
            self.rect[1] = SCREEN_HEIGHT - ysize

        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        pipe_speed = 15
        self.rect[0] -= pipe_speed

def is_off_screen(sprite): #Indica se o Sprite ta fora da Tela
    return sprite.rect[0] < -(sprite.rect[2])


def get_random_pipes(xpos):
    size = random.randint(100, 300) #Canos tamanho aleatório
    pipe = Pipe(False, xpos, size)
    pipe_inverted = Pipe(True, xpos, SCREEN_HEIGHT - size - PIPE_GAPE)
    return (pipe, pipe_inverted)



class Ground(pygame.sprite.Sprite): #Classe pro chao. Ele vai se movimentar

    def __init__(self, xpos): #WIDTH = LARGURA 
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(os.path.join('imagens_game', 'solo.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image, (GROUND_WIDTH, GROUND_HEIGHT))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        self.rect[1] = SCREEN_HEIGHT - GROUND_HEIGHT
        
    def update(self):
        self.rect[0] -= GAME_SPEED



pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

BACKGROUND = pygame.image.load(os.path.join('imagens_game', 'background.png'))
BACKGROUND = pygame.transform.scale(BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT))

bird_group = pygame.sprite.Group()
bird = Bird() # E esse ERRO chapa?
bird_group.add(bird)

ground_group = pygame.sprite.Group() # Confgs do chao

for i in range(2):
    ground = Ground(GROUND_WIDTH * i)
    ground_group.add(ground)


pipe_group = pygame.sprite.Group()
for i in range(2):
    pipes = get_random_pipes(SCREEN_WIDTH * i + 700)
    pipe_group.add(pipes[0])
    pipe_group.add(pipes[1])
    

clock = pygame.time.Clock()

game_on = True

while game_on:

    clock.tick(20) 
    # Colisões do jogo
    if pygame.sprite.groupcollide(bird_group, ground_group, False, False, pygame.sprite.collide_mask) or pygame.sprite.groupcollide(bird_group, pipe_group, False, False, pygame.sprite.collide_mask):
        #Game Over
        pygame.display.update() 
        game_on = False
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                bird.bump()

    screen.blit(BACKGROUND, (0, 0)) #posição do canto superior esquerdo 

    if is_off_screen(ground_group.sprites()[0]): #Se o Sprite ta fora da tela...
        ground_group.remove(ground_group.sprites()[0])

        new_ground = Ground(GROUND_WIDTH - 20)
        ground_group.add(new_ground) 

    if is_off_screen(pipe_group.sprites()[0]):
        pipe_group.remove(pipe_group.sprites()[0])
        pipe_group.remove(pipe_group.sprites()[0])

        pipes = get_random_pipes(SCREEN_WIDTH * 2)
        pipe_group.add(pipes[0])
        pipe_group.add(pipes[1])

    bird_group.update()
    ground_group.update()
    pipe_group.update()

    bird_group.draw(screen) #desenha geral do grupo
    pipe_group.draw(screen)
    ground_group.draw(screen)

    pygame.display.update()   

    