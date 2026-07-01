#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
import sys
from pygame import Surface, Rect
from pygame.font import Font

from code.Const import WIN_WIDTH, WIN_HEIGHT, C_BLUE, C_WHITE, C_YELLOW, C_GREEN, MENU_OPTION


class Menu:
    def __init__(self, window):
        self.window = window
        try:
            # Caminho relativo correto baseado na sua nova árvore de arquivos
            import os

            DIRETORIO_BASE = os.path.dirname(os.path.dirname(__file__))
            PASTA_IMAGENS = os.path.join(DIRETORIO_BASE, "imagens")

            caminho = os.path.join(PASTA_IMAGENS, "fundo_menu.jpg")
            self.surf = pygame.image.load(caminho).convert()
        except Exception as e:
            print(f"Aviso: Não foi possível carregar o fundo do menu. Erro: {e}")
            self.surf = None

    def run(self):
        menu_option = 0

        # Se quiser colocar música depois, a lógica está pronta comentada aqui:
        # pygame.mixer_music.load('./assets/Menu.mp3')
        # pygame.mixer_music.play(-1)

        while True:
            # DESENHAR FUNDO
            if self.surf:
                self.window.blit(source=self.surf, dest=(0, 0))
            else:
                self.window.fill((0, 0, 0))  # Fundo preto caso falte imagem

            # TÍTULO DO JOGO
            self.menu_text(45, "ASTRONAUTA: MISSÃO ESPAÇO", C_BLUE, (WIN_WIDTH / 2, 80))

            # EXIBIÇÃO OBRIGATÓRIA DOS COMANDOS (Regra Uninter)
            self.menu_text(22, "COMANDOS:", C_WHITE, (WIN_WIDTH / 2, 170))
            self.menu_text(18, "Setas Esquerda / Direita - Mover o Astronauta", C_YELLOW, (WIN_WIDTH / 2, 205))

            # REGRAS E OBJETIVOS DO JOGO
            self.menu_text(22, "REGRAS DA MISSÃO:", C_WHITE, (WIN_WIDTH / 2, 260))
            self.menu_text(18, "1. Sobreviva aos meteoros (Pontos por tempo)", C_GREEN, (WIN_WIDTH / 2, 295))
            self.menu_text(18, "2. Colete Combustível para ganhar +15 pontos!", C_GREEN, (WIN_WIDTH / 2, 325))
            self.menu_text(20, "OBJETIVO: ALCANCE 300 PONTOS", C_WHITE, (WIN_WIDTH / 2, 370))

            # SELEÇÃO DE OPÇÕES (START / EXIT)
            for i in range(len(MENU_OPTION)):
                if i == menu_option:
                    self.menu_text(28, MENU_OPTION[i], C_YELLOW, (WIN_WIDTH / 2, 450 + 40 * i))
                else:
                    self.menu_text(28, MENU_OPTION[i], C_WHITE, (WIN_WIDTH / 2, 450 + 40 * i))

            pygame.display.flip()

            # CAPTURA DE EVENTOS DO TECLADO
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        if menu_option < len(MENU_OPTION) - 1:
                            menu_option += 1
                        else:
                            menu_option = 0

                    if event.key == pygame.K_UP:
                        if menu_option > 0:
                            menu_option -= 1
                        else:
                            menu_option = len(MENU_OPTION) - 1

                    if event.key == pygame.K_RETURN:  # ENTER seleciona
                        return MENU_OPTION[menu_option]

    def menu_text(self, text_size: int, text: str, text_color: tuple, text_center_pos: tuple):
        # Usando vinerhanditc  
        text_font: Font = pygame.font.SysFont(name='swis721', size=text_size, bold=True)
        text_surf: Surface = text_font.render(text, True, text_color)
        text_rect: Rect = text_surf.get_rect(center=text_center_pos)
        self.window.blit(source=text_surf, dest=text_rect)