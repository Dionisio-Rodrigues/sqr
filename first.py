import pygame
from pygame.locals import *
from sys import exit
import random
import os
import time

board_base = [
    {
        'board': 'Área Escolar',
        'board_img': 'area-escolar.png'
    },
    {
        'board': 'Curva Acentuada À Esquerda',
        'board_img': 'curva-acentuada-esquerda.png'
    },
    {
        'board': 'Dê A Preferência',
        'board_img': 'de-preferencia.png'
    },
    {
        'board': 'Velocidade Máxima:  60 Km/h',
        'board_img': 'max-60km.png'
    },
    {
        'board': 'Parada Obrigatória',
        'board_img': 'parada-obrigatoria.png'
    },
    {
        'board': 'Passagem Sinalizadora De Pedestres',
        'board_img': 'passagem-de-pedestre.png'
    },
    {
        'board': 'Pista Irregular',
        'board_img': 'pista-irregular.png'
    },
    {
        'board': 'Proibido Estacionar',
        'board_img': 'proibido-estacionar.png'
    },
    {
        'board': 'Proibido Ultrapassar',
        'board_img': 'proibido-ultrapassagem.png'
    },
    {
        'board': 'Circulação de Idosos',
        'board_img': 'circulacao-de-idosos-removebg-preview.png'
    },
    {
        'board': 'Cuidado com Cascalhos',
        'board_img': 'cuidado-com-cascalhos-removebg-preview.png'
    },
    {
        'board': 'Junções Sucessivas',
        'board_img': 'juncoessucessivas-removebg-preview.png'
    },
    {
        'board': 'Saliência ou Lombada',
        'board_img': 'lombada-removebg-preview.png'
    },
    {
        'board': 'Passagem De Nível Com Barreira',
        'board_img': 'niveis-de-barreiras-removebg-preview.png'
    },
    {
        'board': 'Passagem De Nível Sem Barreira',
        'board_img': 'passagem-sem-niveis-de-barreiras-removebg-preview.png'
    },
    {
        'board': 'Ponte Móvel',
        'board_img': 'ponte-movel-removebg-preview.png'
    },
    {
        'board': 'Proíbido Seguir',
        'board_img': 'proibido-seguir.png'
    },
    {
        'board': 'Proibido Virar À Direita',
        'board_img': 'proibido-virar-direita-removebg-preview.png'
    },
    {
        'board': 'Proibido Virar À Esquerda',
        'board_img': 'proibido-virar-esquerda-removebg-preview.png'
    },
    {
        'board': 'Proibido Retornar À Direita',
        'board_img': 'retorno-proibido-removebg-preview.png'
    },
    {
        'board': 'Alfândega',
        'board_img': 'sinalizacao-de-alfandega-removebg-preview.png'
    },
    {
        'board': 'Trânsito Compartilhado Por Ciclistas E Pedestres',
        'board_img': 'transito-compartilhado-removebg-preview.png'
    },
    {
        'board': 'Uso Obrigatório De Corrente',
        'board_img': 'uso-obrigatorio-de-correntes-removebg-preview.png'
    },
    {
        'board': 'Vento lateral',
        'board_img': 'ventos-fortes-laterais-removebg-preview.png'
    }
]

main_directory = os.path.dirname(__file__)
images_directory  = os.path.join(main_directory, 'assets/images')
songs_directory = os.path.join(main_directory, 'assets/songs')


# inicializa todas as funções da biblioteca pygame
pygame.init()

# variaveis com as dimensões da tela
width = 640*2
heigth = 480*2

# instancia uma janela(objeto surface), recebendo uma tupla indicando largura e altura 
window = pygame.display.set_mode((width, heigth))

font = pygame.font.SysFont('arial', 20, bold = True, italic = True)
pontos = 0

pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.load(os.path.join(songs_directory, 'music-bg.mp3'))
pygame.mixer.music.play(-1)

soundGet = pygame.mixer.Sound(os.path.join(songs_directory, 'sound-get.wav'))

clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
board_group = pygame.sprite.Group()

# player settings
player_size = [20, 20]
vel = 10
player_x = (width/2) - player_size[0]/2 
player_y = (heigth/2) - player_size[1]/2

# altera titula da janela
pygame.display.set_caption('Jogo')

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(images_directory, 'car/car.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image, (64,64))
        self.rect = self.image.get_rect()
        self.rect.center = (width/2, heigth/2)

    # def update(self, x = 0, y = 0):
    #     self.rect.y += y
    #     self.rect.x += x

class Board(pygame.sprite.Sprite):
    def __init__(self, board):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(images_directory, board['board_img']))
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.board = board['board']
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(100, width-100), random.randint(100, heigth-100))
    
    def update(self, posXY):
        self.rect.center = posXY

correct_board:Board

def get_boards():
    boards = []
    for x in range(3):
        board = random.choice(board_base)

        while board in boards:
            board = random.choice(board_base)
            
        boards.append(board)
    
    return boards

def board_generator():
    boards = get_boards()
    for board in boards:
        board_group.add(Board(board))

board_generator()
correct_board = random.choice(board_group.sprites())
player = Player()
all_sprites.add(player)
print('placa correta: '+correct_board.board)
flag_flip = [False, False]
flag_rotate = False
rotate = 0

start_time = time.time()
time_left = 30

times_up = False
while not times_up:
    # controla a quantidade de frames
    clock.tick(30)

    # preenche a surface com a cor preta
    window.fill((255,255,255))

    msg = f'Pontos: {pontos}'
    
    msg_time = f'Tempo Restante: {round(time_left - (time.time() - start_time), 1)}'

    msg_question = f'{correct_board.board}'

    text_format = font.render(msg, True, (0, 0, 0))
    question = font.render(msg_question, True, (255, 0, 0))
    time_format = font.render(msg_time, True, (0, 0, 255))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

    if pygame.key.get_pressed()[K_UP]:
        player.rect.y -= vel

        # if flag_rotate:
        #     player.image = pygame.transform.rotate(player.image, -90)
        #     flag_rotate = False

        # if flag_flip[0]:
        #     player.image = pygame.transform.flip(player.image, False, True)
        #     flag_flip[0] = False
            
    if pygame.key.get_pressed()[K_DOWN]:
        player.rect.y += vel

        # if flag_rotate:
        #     player.image = pygame.transform.rotate(player.image, -90)
        #     flag_rotate = False
        #     flag_flip[False]

        # if not flag_flip[0]:
        #     player.image = pygame.transform.flip(player.image, False, True)
        #     flag_flip[0] = True

    if pygame.key.get_pressed()[K_LEFT]:
        player.rect.x -= vel

        # if not flag_rotate:
        #     player.image = pygame.transform.rotate(player.image, 90)
        #     flag_rotate = True

        # if flag_flip[1]:
        #     player.image = pygame.transform.flip(player.image, True, False)
        #     flag_flip[1] = False

    if pygame.key.get_pressed()[K_RIGHT]:
        player.rect.x += vel

        # if not flag_rotate:
        #     player.image = pygame.transform.rotate(player.image, 90)
        #     flag_rotate = True
        #     flag_flip[1] = False
        
        # if not flag_flip[1]:
        #     player.image = pygame.transform.flip(player.image, True, False)
        #     flag_flip[1] = True

    # Desenha os ajentes na surface

    collide = pygame.sprite.spritecollide(player, board_group, False)

    if collide:
        print('Voce pegou uma placa')
        soundGet.play()
        if collide[0].board == correct_board.board:
            pontos += 10
            time_left += 1
            for board in board_group:
                board.kill()
            board_generator()
            correct_board = random.choice(board_group.sprites())
            print('Placa correta: '+correct_board.board)
        else:
            pontos -= 10
            print('Placa incorreta: '+collide[0].board)
            for board in board_group:
                board.update((random.randint(100, width-100), random.randint(100, heigth-100)))
            

    window.blit(time_format, (30, 20))
    window.blit(question, (width*0.45, 20))
    window.blit(text_format, (width*0.9, 20))

    # bordas continuas mapa
    if player.rect.centery < -100: 
        player.rect.centery = heigth+100

    if player.rect.centery > heigth+100: 
        player.rect.centery = -100

    if player.rect.centerx < -100: 
        player.rect.centerx = width+100

    if player.rect.centerx > width+100:
        player.rect.centerx = -100

    if time_left - (time.time() - start_time) < 0:
        times_up = True

    # Faz com que o objeto surface desanhado apareça na tela
    board_group.draw(window)
    all_sprites.draw(window)
    pygame.display.update()
