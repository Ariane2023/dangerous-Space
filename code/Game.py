#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
import random
import sys
from code.Const import WIN_WIDTH, WIN_HEIGHT, FPS, C_BLACK, C_WHITE, C_RED, C_GREEN, C_BLUE, C_YELLOW
from code.Menu import Menu


class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        pygame.display.set_caption("Astronauta: Missão Sobrevivência")
        self.clock = pygame.time.Clock()

        # Descobre a pasta principal do projeto (dangerous space) de forma segura
        import os
        DIRETORIO_BASE = os.path.dirname(os.path.dirname(__file__))
        PASTA_IMAGENS = os.path.join(DIRETORIO_BASE, "imagens")

        # Carregamento de Imagens da Gameplay com Caminho Absoluto Dinâmico
        try:
            # 1. Personagem e Item (Atenção aos nomes exatos dos arquivos na sua pasta!)
            caminho_jogador = os.path.join(PASTA_IMAGENS, "player.png")
            self.imagem_jogador = pygame.image.load(caminho_jogador).convert_alpha()
            self.imagem_jogador = pygame.transform.scale(self.imagem_jogador, (50, 50))

            caminho_moeda = os.path.join(PASTA_IMAGENS, "coin.png")
            self.imagem_combustivel = pygame.image.load(caminho_moeda).convert_alpha()
            self.imagem_combustivel = pygame.transform.scale(self.imagem_combustivel, (30, 30))

            # 2. Fundos das Telas
            caminho_fundo_jogo = os.path.join(PASTA_IMAGENS, "fundo_jogo.jpg")
            self.img_fundo_jogo = pygame.image.load(caminho_fundo_jogo).convert()
            self.img_fundo_jogo = pygame.transform.scale(self.img_fundo_jogo, (WIN_WIDTH, WIN_HEIGHT))

            caminho_fundo_fim = os.path.join(PASTA_IMAGENS, "fundo_fim.png")
            self.img_fundo_fim = pygame.image.load(caminho_fundo_fim).convert()
            self.img_fundo_fim = pygame.transform.scale(self.img_fundo_fim, (WIN_WIDTH, WIN_HEIGHT))

            self.tem_imagens = True
            print("Sucesso: Todas as imagens da gameplay foram carregadas!")
        except Exception as e:
            # Se der erro em alguma, esta impressão vai-te dizer qual arquivo falhou!
            print(f"Aviso: Erro ao carregar imagens da gameplay. Detalhes: {e}")
            self.tem_imagens = False

    def run(self):

        
        while True:
            # 1. Instancia e roda o Menu modular
            menu = Menu(self.window)
            menu_return = menu.run()

            # 2. Se o jogador escolher jogar
            if menu_return == "START GAME":
                vitoria = self.jogar()
                
                # Exibe a tela de fim e armazena se quer continuar jogando
                jogando_fim = self.tela_fim(vitoria)
                if not jogando_fim:
                    pygame.quit()
                    sys.exit()
                    
            # 3. Se escolher sair no menu
            elif menu_return == "EXIT":
                pygame.quit()
                sys.exit()


    def jogar(self):
        # Variáveis do Astronauta
        jog_x = WIN_WIDTH // 2
        jog_y = WIN_HEIGHT - 80
        jog_velocidade = 8
        jog_largura, jog_altura = 50, 50

        # Variáveis do Combustível (Item bom)
        comb_x = random.randint(0, WIN_WIDTH - 30)
        comb_y = -50
        comb_velocidade = 5

        # Variáveis do Meteoro (Inimigo)
        met_x = random.randint(0, WIN_WIDTH - 50)
        met_y = -150
        met_velocidade = 6

        # Pontuação e Vidas
        pontos = 0
        vidas = 3
        contador_tempo = 0

        executando = True
        while executando:
            self.clock.tick(FPS)

            # Desenha o fundo da gameplay
            if self.tem_imagens:
                self.window.blit(self.img_fundo_jogo, (0, 0))
            else:
                self.window.fill(C_BLACK)

            # Eventos de fechar o jogo
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Movimentação do Astronauta
            teclas = pygame.key.get_pressed()
            if teclas[pygame.K_LEFT] and jog_x > 0:
                jog_x -= jog_velocidade
            if teclas[pygame.K_RIGHT] and jog_x < WIN_WIDTH - jog_largura:
                jog_x += jog_velocidade

            # Lógica de pontos automáticos por tempo
            contador_tempo += 1
            if contador_tempo >= 30: # Meio segundo em 60 FPS
                pontos += 1
                contador_tempo = 0

            # Queda dos objetos
            comb_y += comb_velocidade
            met_y += met_velocidade

            if comb_y > WIN_HEIGHT:
                comb_x = random.randint(0, WIN_WIDTH - 30)
                comb_y = -50

            if met_y > WIN_HEIGHT:
                met_x = random.randint(0, WIN_WIDTH - 50)
                met_y = -150
                met_velocidade += 0.3 # Deixa o jogo gradualmente mais difícil

            # Criação de Retângulos para Colisão
            ret_astronauta = pygame.Rect(jog_x, jog_y, jog_largura, jog_altura)
            ret_combustivel = pygame.Rect(comb_x, comb_y, 30, 30)
            ret_meteoro = pygame.Rect(met_x, met_y, 50, 50)

            # Colisão com Combustível (+15 Pontos)
            if ret_astronauta.colliderect(ret_combustivel):
                pontos += 15
                comb_x = random.randint(0, WIN_WIDTH - 30)
                comb_y = -50

            # Colisão com Meteoro (Dano)
            if ret_astronauta.colliderect(ret_meteoro):
                vidas -= 1
                met_x = random.randint(0, WIN_WIDTH - 50)
                met_y = -150

            # Condições de Vitória e Derrota
            if pontos >= 300:
                return True
            if vidas <= 0:
                return False

            # Desenho dos elementos na tela
            if self.tem_imagens:
                self.window.blit(self.imagem_jogador, (jog_x, jog_y))
                self.window.blit(self.imagem_combustivel, (comb_x, comb_y))
            else:
                pygame.draw.rect(self.window, C_BLUE, ret_astronauta)
                pygame.draw.ellipse(self.window, C_YELLOW, ret_combustivel)

            # Meteoro desenhado como círculo de destaque
            pygame.draw.circle(self.window, C_RED, (met_x + 25, met_y + 25), 25)

            # Interface de texto da gameplay
            self.game_text(25, f"Pontuação: {pontos}/300", C_WHITE, (120, 30))
            self.game_text(25, f"Vidas: {vidas}", C_RED, (WIN_WIDTH - 100, 30))

            pygame.display.flip()

    def tela_fim(self, vitoria):
        while True:
            if self.tem_imagens:
                self.window.blit(self.img_fundo_fim, (0, 0))
            else:
                self.window.fill(C_BLACK)

            if vitoria:
                self.game_text(35, "MISSÃO CUMPRIDA! VOCÊ VOLTOU À TERRA!", C_GREEN, (WIN_WIDTH / 2, WIN_HEIGHT / 2 - 50))
            else:
                self.game_text(35, "GAME OVER! O ASTRONAUTA FOI ATINGIDO!", C_RED, (WIN_WIDTH / 2, WIN_HEIGHT / 2 - 50))

            self.game_text(22, "Pressione ESPAÇO para ir ao Menu ou ESC para Sair", C_WHITE, (WIN_WIDTH / 2, WIN_HEIGHT / 2 + 40))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return True # Volta para o fluxo principal (menu)
                    if event.key == pygame.K_ESCAPE:
                        return False # Encerra o jogo

    def game_text(self, text_size: int, text: str, text_color: tuple, text_center_pos: tuple):
        text_font = pygame.font.SysFont(name="Lucida Sans Typewriter", size=text_size, bold=True)
        text_surf = text_font.render(text, True, text_color)
        text_rect = text_surf.get_rect(center=text_center_pos)
        self.window.blit(source=text_surf, dest=text_rect)