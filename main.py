#Importando as bibliotecas que foram utilizadas
import pygame
from pygame.locals import *
import random, time
#Inicia o programa
pygame.init()
# Variaveis do tamanho da tela
largura_tela = 600
comprimento_tela = 700
#Declarando o tamanho da tela usando a biblioteca pygame
tela = pygame.display.set_mode((largura_tela, comprimento_tela))
pygame.display.set_caption('Brick Breaker')

#Cor de fundo
cor_fundo = (234, 218, 184)

#funcao para gerar cores aleatorias entre (verde, vermelho e  azul)
def cor_aleatoria(x=0,y=0,z=0):
    lista_cores = [x, y, z]
    cor_aleatoria = random.randint(0,2)
    return lista_cores[cor_aleatoria]

#cor da plataforma
cor_plataforma = (142,135,123)
contorno = (100, 100, 100)

#cor do texto
verde = (86, 174, 87)
vermelho = (242, 85, 96)
azul = (69, 177, 232)
cor_texto = (78, 81, 139)

#definindo a fonte
fonte = pygame.font.SysFont('Constantia', 30)

#definindo as variaveis do jogo
colunas = 6
linhas = 6
relogio = pygame.time.Clock()
fps = 60
estado_bola = False
game_over = 0

#funcao para desenhar um texto na tela 
def desenhar_texto(font, text, text_color, x, y):
    imagem = font.render(text, True, text_color)
    tela.blit(imagem, (x,y))

#funcao para designar um inicio aleatorio para a bola
def inicio_bola():
    lista_valores = (1, -1)
    return random.choice(lista_valores)

#Definindo uma classe para a parede, ou seja, criando a parede como um objeto a ser exibido na tela 
class parede_blocos():
    def __init__ (self):
        self.largura = largura_tela // colunas
        self.comprimento = 50

    #Criando as colunas e linhas de blocos com as cores aleatorias, e coordenadas designadas
    def criar_parede(self):
        self.blocos = []
        #Uma lista para armazenar os dados de cada blocos individualmente
        blocos_individuais = []
        #percorre todas as linhas
        for linha in range(linhas):
            #lista com com as colunas de uma linha
            linha_blocos = []

            #percorre todas as colunas de uma linha
            for coluna in range(colunas):
                #criando uma posicao x e y para cada bloco
                bloco_x = coluna * self.largura
                bloco_y = linha * self.comprimento
                #criando um retangulo nas posicoes declaradas usando uma funcao dentro da biblioteca
                retangulo = pygame.Rect(bloco_x, bloco_y+50, self.largura , self.comprimento)
                #Determinando uma cor aleatoria
                cor_bloco = cor_aleatoria(verde, vermelho, azul)
                blocos_individuais = [retangulo, cor_bloco]
                #adiciona cada bloco de cada coluna nas linhas correspondente
                linha_blocos.append(blocos_individuais)
            #adiciona a linha inteira dentro da lista que vai conter todos os blocos
            self.blocos.append(linha_blocos)
        
        
        #Colocar uma cor aleatoria para cada bloco
        #sendo que nenhum bloco pode ter a mesma cor um do lado outro
        prox_bloc = 0
        cont_lin = 0
        bloco_anterior = []
        cont_bloco = -1
        for linha in self.blocos:
            
            for bloco in linha:
                cont_bloco += 1
                bloco_anterior.append(bloco[1])
                while bloco[1] == prox_bloc and bloco[1] == bloco_anterior[cont_bloco]:
                    bloco[1] = cor_aleatoria(vermelho, verde, azul)
                prox_bloc = bloco[1]
                bloco_anterior.append(bloco[1])
            cont_lin += 1
                
            
    #funcao que desenha a parede na tela usando a biblioteca
    def desenhar_parede(self):
        #percorre as linhas de blocos dentro da lista que contem todos os blocos
        for linha in self.blocos:
            for bloco in linha:
                pygame.draw.rect(tela, bloco[1], bloco[0])
                pygame.draw.rect(tela, cor_fundo, (bloco[0]), 5)

#Definindo uma classe para a plataforma, ou seja, criando a plataforma como um objeto a ser exibido na tela 
class plataforma():
    def __init__(self):
        #Definindo as variaveis da plataforma
        #Usando a funcao reset para resetar os dados da plataforma no restart
        self.reset()
    #movimento da plataforma
    def movimento_plat(self):
        #variavel do estado da direcao da plataforma
        self.direcao = 0
        #checando a tecla que foi pressionada utilizando a biblioteca pygame
        tecla = pygame.key.get_pressed()
        #Condicional da tecla da seta para esquerda move a plataforma para esquerda
        if tecla[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.velocidade
            self.direcao = -2
        #Condicional da tecla da seta para direita move a plataforma para direita
        if tecla[pygame.K_RIGHT] and self.rect.right < largura_tela:
            self.rect.x += self.velocidade
            self.direcao = +2
    #funcao que desenha a plataforma na tela utilizando a biblioteca pygame
    def desenhar_plataforma(self):
        pygame.draw.rect(tela, cor_plataforma, self.rect)
        pygame.draw.rect(tela, contorno, self.rect, 3)
    #funcao que reseta os dados das variveis para o formato inicial
    def reset(self):
        self.largura = int(largura_tela/colunas)
        self.comprimento = 20
        self.x = int(((largura_tela/2)-(self.largura/2)))
        self.y = comprimento_tela - (self.comprimento * 2)
        self.velocidade = 8
        self.rect = Rect(self.x, self.y, self.largura, self.comprimento)
        self.direcao = 0

#Definindo uma classe para a bola, ou seja, criando a bola como um objeto a ser exibido na tela 
class bola_jogo():
    def __init__(self, x, y):
        #funcao para resetar os dados das variaveis da bola do jogo
        self.reset(x, y)
    #funcao para desenhar a bola na tela
    def desenhar_bola(self):
        pygame.draw.circle(tela, cor_plataforma, (self.rect.x + self.raio_bola, self.rect.y + self.raio_bola), self.raio_bola)
        pygame.draw.circle(tela, contorno, (self.rect.x + self.raio_bola, self.rect.y + self.raio_bola), self.raio_bola)

    def movimento_bola(self):
        #Fronteira de colisao 
        colisao = 5

        estado_parede = 1
        contador_linha = 0
        for linha in parede_blocos.blocos:
            contador_coluna = 0
            for coluna in linha:
                #check collision
                if self.rect.colliderect(coluna[0]):
                    self.pontos += 10
                    #Ve se teve colisao de baixo da bola e por cima de algum bloco
                    if abs(self.rect.bottom - coluna[0].top) < colisao and self.velocidade_y > 0:
                        self.velocidade_y *= -1
                    #Ve se teve colisao por cima da bola e por baixo de algum bloco
                    elif abs(self.rect.top - coluna[0].bottom) < colisao and self.velocidade_y < 0:
                        self.velocidade_y *= -1
                    #Ve se teve colisao pelo lado direito da bola e lado esquerdo de algum bloco
                    elif abs(self.rect.right - coluna[0].left) < colisao and self.valocidade_x > 0:
                        self.valocidade_x *= -1
                    #Ve se teve colisao pelo lado esquerdo da bola e lado direito de algum bloco
                    elif abs(self.rect.left - coluna[0].right) < colisao and self.valocidade_x < 0:
                        self.valocidade_x *= -1
                    parede_blocos.blocos[contador_linha][contador_coluna][0] = (0, 0, 0, 0) 
                if parede_blocos.blocos[contador_linha][contador_coluna][0] != (0,0,0,0):
                    estado_parede = 0
                contador_coluna += 1
            contador_linha += 1
        #Depois de verificar todos os blocos checa para saber se todos os blocos foram destruidos
        if estado_parede == 1:
            self.game_over = 1
        #Verifica se a bola encostou nas paredes da janela 
        if self.rect.left < 0 or self.rect.right > largura_tela:
            self.valocidade_x *= -1
        #Verifica se a bola encostou no topo da janela 
        if self.rect.top < 0:
            self.velocidade_y *= -1
        #Verifica se a bola encostou na parte de baixo da janela, se sim, declara game_over como -1
        if self.rect.bottom > comprimento_tela:
            self.game_over = -1
        #Ve se teve colisao com a plataforma
        if self.rect.colliderect(plataforma_jogador):
            if abs(self.rect.bottom - plataforma_jogador.rect.top) < colisao:
                self.velocidade_y *= -1
                self.valocidade_x += plataforma_jogador.direcao
                if self.valocidade_x > self.velocidade_max:
                    self.valocidade_x = self.velocidade_max
                elif self.valocidade_x < 0 and self.valocidade_x < -self.velocidade_max:
                    self.valocidade_x = -self.velocidade_max
            else:
                self.valocidade_x *= -1
        #Velocidade base da bola 
        self.rect.x += self.valocidade_x
        self.rect.y += self.velocidade_y

        return self.game_over
    #funcao para resetar o estado atual da bola
    def reset(self, x, y):
        valor_aleatorio_x = inicio_bola()
        self.raio_bola = 10
        self.x = x - self.raio_bola
        self.y = y 
        self.rect = Rect(self.x, self.y, self.raio_bola * 2, self.raio_bola * 2)
        self.valocidade_x = 4 * valor_aleatorio_x
        self.velocidade_y = 4 
        self.game_over=0
        self.velocidade_max = 6
        self.pontos = 0
    #Desenha na tela a pontuacao em tempo real 
    def print_point(self):
        desenhar_texto(fonte, f"Pontos= {self.pontos}", cor_texto, 1, 20)
        return self.pontos

#Desenha a parede
parede_blocos = parede_blocos()
parede_blocos.criar_parede()

#Cria o objeto plataforma
plataforma_jogador = plataforma()

#Cria o objeto bola
bola_jogador = bola_jogo(plataforma_jogador.x + (plataforma_jogador.largura // 2), plataforma_jogador.y - plataforma_jogador.comprimento)


Inicio = True
while Inicio:
    #Determina um relogio virtual para que a atualizacao de tela seja de 60 frames por segundo
    relogio.tick(fps)
    #Cor de fundo do jogo
    tela.fill(cor_fundo)

    #Verifica o estado do jogo para saber se o jogo acabou ou nao 
    if not estado_bola:
        if game_over == 0:
            desenhar_texto(fonte, "CLIQUE ENTER PARA COMECAR", cor_texto, 70, comprimento_tela//2)
        elif game_over == 1:
            desenhar_texto(fonte, "VOCE VENCEU", cor_texto, 80, comprimento_tela//2)
        elif game_over == -1:
            desenhar_texto(fonte, "GAME OVER", cor_texto, 200, comprimento_tela//2)
            

    #Verifica se algum evento especifico aconteceu
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Inicio = False
        if pygame.key.get_pressed()[K_RETURN] and estado_bola == False:
            time.sleep(0.2)
            estado_bola = True
            bola_jogador.reset(plataforma_jogador.x + (plataforma_jogador.largura // 2), plataforma_jogador.y - plataforma_jogador.comprimento)
            plataforma_jogador.reset()
            parede_blocos.criar_parede()
    bola_jogador.print_point()
    
    #desenhar a plataforma, a parede e a bola na tela
    parede_blocos.desenhar_parede()
    bola_jogador.desenhar_bola()
    plataforma_jogador.desenhar_plataforma()
    
    if estado_bola:
        plataforma_jogador.movimento_plat()
        game_over = bola_jogador.movimento_bola()
        if game_over != 0:
            estado_bola = False

            
    pygame.display.update()


pygame.quit()