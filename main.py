import pygame
import random
import sys

# Inicialização do Pygame
pygame.init()

# Configurações da Janela
LARGURA, ALTURA = 800, 600
janela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Astronauta: Missão Sobrevivência")

# Cores (RGB)
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERDE = (0, 255, 0)
VERMELHO = (255, 0, 0)
AZUL = (50, 150, 250)
AMARELO = (255, 215, 0)

# Relógio para controlar os FPS e o tempo
relogio = pygame.time.Clock()
FPS = 60

# --- CARREGAMENTO DE ASSETS (Caminho Relativo) ---
# Se você ainda não tiver as imagens na pasta, o jogo vai usar formas coloridas
try:
    imagem_jogador = pygame.image.load("imagens/jogador.png").convert_alpha()
    imagem_combustivel = pygame.image.load(
        "imagens/moeda.png").convert_alpha()  # Pode ser imagem de combustível/estrela
    imagem_jogador = pygame.transform.scale(imagem_jogador, (50, 50))
    imagem_combustivel = pygame.transform.scale(imagem_combustivel, (30, 30))
    TEM_IMAGENS = True
except:
    TEM_IMAGENS = False

# Fontes para os textos
fonte_menu = pygame.font.SysFont("Arial", 40, bold=True)
fonte_texto = pygame.font.SysFont("Arial", 25)


def mostrar_texto(texto, fonte, cor, x, y):
    superficie = fonte.render(texto, True, cor)
    retangulo = superficie.get_rect(center=(x, y))
    janela.blit(superficie, retangulo)


# --- TELA DE MENU ---
def tela_menu():
    while True:
        janela.fill(PRETO)

        mostrar_texto("ASTRONAUTA: MISSÃO ESPAÇO", fonte_menu, AZUL, LARGURA // 2, 130)

        # OBRIGATÓRIO: Mostrar comandos no menu
        mostrar_texto("COMANDOS:", fonte_texto, BRANCO, LARGURA // 2, 230)
        mostrar_texto("Setas Esquerda / Direita - Mover o Astronauta", fonte_texto, AMARELO, LARGURA // 2, 270)

        # Regras do Jogo
        mostrar_texto("REGRAS DO JOGO:", fonte_texto, BRANCO, LARGURA // 2, 340)
        mostrar_texto("1. Sobreviva aos meteoros para ganhar pontos por tempo.", fonte_texto, VERDE, LARGURA // 2, 380)
        mostrar_texto("2. Colete Tanques de Combustível para ganhar +15 pontos!", fonte_texto, VERDE, LARGURA // 2, 410)
        mostrar_texto("OBJETIVO: Alcance 300 pontos para vencer!", fonte_texto, BRANCO, LARGURA // 2, 460)

        mostrar_texto("Pressione ESPAÇO para Iniciar", fonte_menu, BRANCO, LARGURA // 2, 530)

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    return


# --- TELA DE FIM DE JOGO ---
def tela_fim(vitoria):
    while True:
        janela.fill(PRETO)

        if vitoria:
            mostrar_texto("MISSÃO CUMPRIDA! VOCÊ VOLTOU À TERRA!", fonte_menu, VERDE, LARGURA // 2, ALTURA // 2 - 50)
        else:
            mostrar_texto("GAME OVER! O ASTRONAUTA FOI ATINGIDO!", fonte_menu, VERMELHO, LARGURA // 2, ALTURA // 2 - 50)

        mostrar_texto("Pressione ESPAÇO para reiniciar ou ESC para sair", fonte_texto, BRANCO, LARGURA // 2,
                      ALTURA // 2 + 50)

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    return True
                if evento.key == pygame.K_ESCAPE:
                    return False


# --- LOOP PRINCIPAL DO JOGO ---
def jogar():
    # Variáveis do Astronauta
    jog_x = LARGURA // 2
    jog_y = ALTURA - 80
    jog_velocidade = 8
    jog_largura, jog_altura = 50, 50

    # Variáveis do Combustível (Item bom)
    comb_x = random.randint(0, LARGURA - 30)
    comb_y = -50
    comb_velocidade = 5

    # Variáveis do Meteoro (Desafio/Inimigo)
    met_x = random.randint(0, LARGURA - 50)
    met_y = -150
    met_velocidade = 6

    # Sistema de Pontos e Vidas
    pontos = 0
    vidas = 3

    # Variável para controlar o ganho de pontos por tempo
    contador_tempo = 0

    executando = True
    while executando:
        relogio.tick(FPS)
        janela.fill(PRETO)  # Fundo do espaço

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # 1. Movimentação do Astronauta
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and jog_x > 0:
            jog_x -= jog_velocidade
        if teclas[pygame.K_RIGHT] and jog_x < LARGURA - jog_largura:
            jog_x += jog_velocidade

        # 2. Lógica dos pontos por tempo (Ganha 1 ponto a cada 30 frames ~ meio segundo)
        contador_tempo += 1
        if contador_tempo >= 30:
            pontos += 1
            contador_tempo = 0

        # 3. Movimento dos Objetos caindo
        comb_y += comb_velocidade
        met_y += met_velocidade

        # Se o combustível passar, reseta no topo
        if comb_y > ALTURA:
            comb_x = random.randint(0, LARGURA - 30)
            comb_y = -50

        # Se o meteoro passar, reseta no topo e aumenta um pouquinho a velocidade do jogo
        if met_y > ALTURA:
            met_x = random.randint(0, LARGURA - 50)
            met_y = -150
            met_velocidade += 0.3

        # 4. Detecção de Colisões
        ret_astronauta = pygame.Rect(jog_x, jog_y, jog_largura, jog_altura)
        ret_combustivel = pygame.Rect(comb_x, comb_y, 30, 30)
        ret_meteoro = pygame.Rect(met_x, met_y, 50, 50)

        # Colisão com o Combustível (Bônus!)
        if ret_astronauta.colliderect(ret_combustivel):
            pontos += 15  # Ganha muitos pontos!
            comb_x = random.randint(0, LARGURA - 30)
            comb_y = -50

        # Colisão com o Meteoro (Dano!)
        if ret_astronauta.colliderect(ret_meteoro):
            vidas -= 1
            met_x = random.randint(0, LARGURA - 50)
            met_y = -150  # Reseta o meteoro para dar chance de recuperação

        # 5. Condições de Vitória e Derrota
        if pontos >= 300:
            return True
        if vidas <= 0:
            return False

        # 6. Desenhar elementos
        if TEM_IMAGENS:
            janela.blit(imagem_jogador, (jog_x, jog_y))
            janela.blit(imagem_combustivel, (comb_x, comb_y))
        else:
            # Caso não tenha imagens prontas ainda:
            pygame.draw.rect(janela, AZUL, ret_astronauta)  # Astronauta (Azul)
            pygame.draw.ellipse(janela, AMARELO, ret_combustivel)  # Combustível (Amarelo)

        # Desenha o meteoro sempre como um círculo vermelho/cinza para destacar
        pygame.draw.circle(janela, VERMELHO, (met_x + 25, met_y + 25), 25)

        # Placar na tela
        mostrar_texto(f"Pontuação: {pontos}/300", fonte_texto, BRANCO, 120, 30)
        mostrar_texto(f"Vidas: {vidas}", fonte_texto, VERMELHO, LARGURA - 100, 30)

        pygame.display.flip()


# --- FLUXO DO APLICATIVO ---
tela_menu()
jogando = True
while jogando:
    resultado_vitoria = jogar()
    jogando = tela_fim(resultado_vitoria)

pygame.quit()