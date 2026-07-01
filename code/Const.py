#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame
# Configurações da Janela
WIN_WIDTH = 750
WIN_HEIGHT = 530
FPS = 60

# Cores (RGB)
C_BLACK = (0, 0, 0)
C_WHITE = (255, 255, 255)
C_RED = (255, 0, 0)
C_GREEN = (0, 255, 0)
C_BLUE = (50, 150, 250)
C_YELLOW = (255, 215, 0)
C_ORANGE = (255, 128, 0)

# Opções do Menu Estilo o Jogo do Professor
MENU_OPTION = ["START GAME", "EXIT"]

#Para ver as fontes disponíveis
import pygame

pygame.init()
print(pygame.font.get_fonts())