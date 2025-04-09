#!/usr/bin/env python3

"""
Woodblock Puzzle Game - Versão Melhorada e Corrigida
---------------------------------------------------
Modificações aplicadas:
- Música de fundo alterada (Base64 8-bit)
- Configurações de som corrigidas
- Tamanho dos elementos da UI aumentado (exceto grelha 10x10)
- Correção do NameError em draw_rules
- Adição de prints de depuração para o crash do modo Humano
"""

import pygame
import sys
import os
import numpy as np
import random
import heapq
import traceback
import io
import base64
import wave
import tempfile

# Inicialização do Pygame
pygame.init()
pygame.mixer.init()

# Configurações de áudio
MUSIC_ENABLED = True
MUSIC_VOLUME = 0.5  # 50% do volume máximo

# Música codificada em base64 (uma melodia 8-bit simples)
# Substitui a melodia anterior por algo ligeiramente mais variado
BACKGROUND_MUSIC = """
UklGRvC1BABXQVZFZm10IBAAAAABAAEARKwAAIhYAQACABAAZGF0Ycy1BAAAADAA
awCyAAQBYAHGATYCrwIvA7cDRQTZBHAFCwapBkcH5geECCEJuwlSCuQKcgv6C30M
+QxuDd0NRA6kDv0OUA+cD+EPIBBaEI4QvhDqEBIRNxFaEXsRmhG4EdYR8xEREi8S
TRJrEooSqRLIEucSBhMjE0ATWhNxE4YTlxOjE6oTqxOmE5kThRNpE0QTFRPeEpwS
URL8EZ0RNBHCEEcQww84D6UOCw5rDcYMHQxxC8IKEgphCbEIAghVB6sGBAZiBcME
KgSVAwYDfAL3AXYB+gCBAAwAmv8o/7f+Rf7S/Vz94vxk/OD7VfvC+if6gvnU+Bv4
WPeK9rL10PTl8/Hy9vH08O/v5u7d7dbs0uvW6uPp/Ogl6GHnsuYd5qTlSuUT5QHl
GOVZ5cjlZuY15zfobenY6njsTu5Y8JfyCPWr9376fv2nAPgDbQcBC7IOeRJUFj0a
Lh4kIhomCSrtLcExgTUoObA8F0BYQ3BGW0kXTKFO+FAZUwRVt1Y0WHlZiFphWwdc
ely+XNRcv1yDXCJcoVsCW0laeVmXWKZXqFajVZhUilN9UnNRblBvT3hOi02oTNBL
AktASodJ10gwSI9H9EZcRsVFLkWURPVDTkOeQuFBF0E9QFE/UT48PRE80Dp2OQU4
ezbaNCEzUjFtL3UtaitQKSYn8SSzIm0gIx7XG40ZRRcEFcoSnBB6DmYMYgpwCI8G
wgQIA2EBz/9O/t78fvst+un41/fT9tj14/Tw8/3yB/IN8Qvw/+7n7cLsjutK6vbo
kOcZ5pLk/OJY4ajf7t0u3Graptjm1i7Vg9Pq0WjQAs+8zZ7Mq8vpyl3KDMr7yS3K
p8psy3/M483Zz6LRAdSz1rrZE9294LXk+eiD7VDyW/ee/BMCtAd6DV8TWRljH3Ql
hCuMMYM3Yz0lQ8BILk5pU2tYLl2uYeZl02lxbb1wt3Nddq54q3pUfKt9sn5qf9h/
/3/if4V/734ifiV9/Hutej15sXcOdlp0mXLPcAFvM21oa6Rp6Wc6ZphkBWOCYRBg
rl5dXRxc6VrEWatYm1eTVpFVklSTU5NSjVGBUGtPSU4YTdhLh0oiSahHGkZ1RLtC
6kAEPwk9+jrZOKY2ZTQWMr0vWy3zKogoHCayI00h8B6cHFQaGxjxFdoT1hHnDw0O
SgycCgUJgwcXBr8EeQNFAiEBCQD//vv9//wG/A/7F/ob+Rr4EPf99d30sfN28ivx
0e9n7u3sZOvN6SvofebJ5A/jU+GZ3+TdOdyd2hPZoddL1hfVCdQm03TS99Gy0avR
5tFl0ivTPNSa1UXXP9mJ2yHeCOE85LrngOuL79fzX/gf/RACLgdyDNYRUxfiHHsi
GCiwLT4zuTgbPlxDd0hlTSBSpFbrWvBesGIpZlZpN2zJbgxxAHOldPx1B3fId0B4
dXhoeB54mnfidvl15XSrc09y1nBFb6Jt8GszanForWbqZCtjdGHHXyZeklwMW5ZZ
L1jYVpFVV1QrUwtS9lDoT+FO3k3dTNxL10rNSbtIn0d4RkJF/EOmQj1BwD8wPos8
0ToDOSE3LDUkMw0x5i6yLHIqKijaJYcjMSHcHoscPxr7F8EVkxN0EWQPZw18C6QJ
4QczBpoEFQOlAUgA/v7F/Zr8fvtt+mb5Zvhr93P2e/WB9IPzfvJy8VvwOO8J7svs
f+sl6rvoQ+e+5S3kkeLs4ELflN3l2zral9j+1nTV/tOg0l/RP9BGz3fO183qzTTN
Os1+zQTOzs7ezzbR19LC1PjWdtk+3EzfnuIz5gbqFO5Y8s72cPs4ACEFJgo+D2QU
kRm+HuQj/CgALuoysjdUPMpADkUbSe5Mg1DVU+NWq1kqXF9eS2DtYUVjVmQgZadl
62XxZbxlUGWwZOFj52LGYYRgJV+tXSFchVrdWC9XfFXJUxhSblDLTjJNpUslSrRI
UEf8RbZEfUNSQjNBHkATPw4+Dj0RPBU7GDoWOQ84ADfmNcE0jTNLMvgwlC8dLpMs
9ipGKYQnryXJI9Mhzh+8HZ4bdxlIFxUV3hKnEHEOQAwVCvIH2gXOA9EB5P8H/jz8
g/re+E33z/Vk9AvzxPGO8GfvTu5B7T7sQ+tO6lzpbOh854nmkOWS5IvjeeJd4TTg
/t663WncCtue2SbYpNYY1YbT79FX0MDOLc2jyyXKt8hexxzG+MT0wxbDYsLbwYXB
ZcF9wdDBYsI0w0jEn8U7x8G4brtxvsjBccVpya3NOdIJ1xfcXOHU5njsQPIk+B7+ 
JQQzCj4QPxYuHAMitydDLZ8yxjexPFtBv0XZSaVNIFFHVBlXlVm7W4pdBF8rYP9g
hWG/YbFhX2HOYAJgAF/OXXBc7VpJWYtXtlXRU+BR6E/tTfJL/UkPSCtGVESMQtNA
Kz+VPQ88mzo2OeA3mDZbNSg0+zLUMa4wiC9fLjAt+Su2KmYpByiWJhEleCPJIQMg
Jh4yHCYaBBjLFX4THhGsDisMnAkDB2EEugER/2f8wPkf94b0+PF37wbtpupa6CPm
AuT34QTgKN5k3LbaHtmb1yzWztR/0z7SCNHaz7POjs1qzETLGsroyKzHZcYRxa7D
O8K3wCK/fL3Fu/65KbhItly0aLJxsHiugqyUqrKo4aYmpYajBqKtoH6fgZ65nSyd
35zWnBWdoJ16nqafJaH6oiWlp6d/qqytLbH+tB65h703wijHVMy20UfXAN3a4s7o
1O7k9Pb6AQEAB+kMtBJcGNgdISMyKAUtlTHdNdk5hT3fQOVDlkbwSPNKoUz6TQFP
t08fUD1QFlCsTwVPJk4TTdNLakrdSDNHcEWZQ7VBxj/TPd477DkAOB02RTR8MsEw
Fy9+LfYrfyoZKcIneiY+JQ0k5CLCIaMghR9lHkEdFhziGqEZUhjyFoAV+hNfEq0Q
5Q4FDQ4L/wjbBqEEUwL0/4P9A/t4+OP1R/Om8ATuZOvI6DLmp+Mn4bbeVdwH2s3X
qdWb06TRxM/8zUvMscosybvHXcYPxdDDnsJ2wVTAOL8evgO95LvAupS5Xbgat8i1
aLT3snWx4q8+roqsx6r2qBmnM6VIo1mha5+DnaSb05kWmHGW6ZSFk0mSOpFfkLyP
V48zj1WPwY96kISR4JKRlJiW9piqm7SeEqLDpcSpEa6msn+3l7znwWvHGs3v0uHY
6d4A5R3rOfFL90z9MwP7CJsODBRIGUkeCiOFJ7Yrmi8sM2w2VznsOyo+EkClQeRC
0UNvRMJEzESRRBdEYkN3QltBE0ClPhY9bDusOds3/TUYNDAySDBlLoksuCrzKDwn
lSX/I3oiByGkH1IeDx3ZG68ajxl2GGIXUBY/FSoUEBPuEcAQhg89DuIMcwvxCVgI
qQbjBAUDEQEG/+X8r/pl+Ar2n/Mn8aTuGOyH6fLmXuTM4UDfvNxD2tfXetUv0/fQ
1M7HzNHK8sgqx3rF4cNewu/Alb9MvhO957vHurC5nriRt4S2dbVitEezJLL1sLmv
b64UramrLaqgqAKnVKWYo8+h+58gnkCcX5qBmKqW35Qkk36R84+JjkSNKoxAi4yK
EorXieCJMYrOirmL9oyHjmyQqZI8lSWYY5v1ntiiCqeGq0mwTbWNugPAqcV4y2nR
dNeR3brj5ekL8CT2KfwPAtMHbA3UEgMY9RylIQwmKCr1LXAxljRoN+M5BzzWPVA/
d0BOQdZBFUIMQsJBOkF5QIU/Yj4VPaY7FzpwOLU26zQXMz4xYy+KLbgr7ikvKH4m
3CRLI8ohWyD9Hq8dcRxCGx8aBxn4F+8W6hXmFOET2BLIEa4QiA9VDhENuwtRCtII
PAeQBcwD8QEAAPj92vuo+WT3DvWq8jrwwO0wf1LzoV9uOywEwV57FZEKVqivTKAP
tUQJ6rJ9ERHFjc6NkGQnMTIn2LRb+mgR8tVmB1UeRebfnB2y1DqC9lYtHT8TzhtI
9rMyWcFVmipKq2ksDWw0ZJrr0pHtvTLZlzQOD9FNbPRUw4EPHlEn1SrgslrfiT0y
gK5mMwhh9LZhX0fIuTqOF7Y/gRm41lny8fBG7z+2w6jPlHEqxD2n3TkF11zx/kzd
n5Hk87b1r1A1m9r7hf+lOLx5HxxqFtHTb3NwZ5hZirhhdMKU4Hq7rDhZOaE4GRhO
9B53oRXjrll0u3jwsTx8jIVWUG7lIhzkwg5i5mglvDNW9DdY0qs6J5gLwVhfv4Bp
Xh4lhhBdYwID9xL5zY5Q7toEZxi9MOzPCWx3yZQ6jGVgF6NdgbhP+4b0ptw/xk+9
K5xjsqzX58gHEzDp0mktVuHw2z2I0lPdujErnpROAfg9M1ylMblVuE2gdKzzZGxF
c8XjLN7+25OHpAHv5YDNzD8iwy4hrzm4/z2pksUHYdYoJpL0+ekW+xd1VKYgFAwC
W8gVoM0A0ZnkwGbYWuJ7J6fQ==
""" 

def play_base64_audio(base64_string):
    audio_data = base64.b64decode(base64_string)
    
    # Salvar o áudio em um arquivo temporário
    with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_audio_file:
        temp_audio_file.write(audio_data)
        temp_audio_file.close()
        
        # Reproduzir o arquivo de áudio temporário
        pygame.mixer.init()
        pygame.mixer.music.load(temp_audio_file.name)
        pygame.mixer.music.play()

# Reproduzir o áudio
play_base64_audio(BACKGROUND_MUSIC)

# Função para carregar e tocar música
def load_and_play_music():
    if MUSIC_ENABLED:
        try:
            # Decodificar a música de base64
            music_data = base64.b64decode(BACKGROUND_MUSIC.strip())

            # Criar um objeto de arquivo em memória
            music_file = io.BytesIO(music_data)

            # Carregar e tocar a música
            pygame.mixer.music.load(music_file)
            pygame.mixer.music.set_volume(MUSIC_VOLUME)
            pygame.mixer.music.play(-1)  # -1 significa loop infinito
        except pygame.error as e: # Captura erros específicos do Pygame
            print(f"Erro do Pygame ao carregar ou tocar música: {e}")
            traceback.print_exc()
        except Exception as e:
            print(f"Erro inesperado ao carregar música: {e}")
            traceback.print_exc()

# Função para ajustar o volume da música
def set_music_volume(volume):
    global MUSIC_VOLUME
    MUSIC_VOLUME = max(0.0, min(1.0, volume))  # Garantir que o volume esteja entre 0 e 1
    pygame.mixer.music.set_volume(MUSIC_VOLUME)

# Função para ativar/desativar a música
def toggle_music():
    global MUSIC_ENABLED
    MUSIC_ENABLED = not MUSIC_ENABLED

    if MUSIC_ENABLED:
        # Se a música foi ativada, carregar e tocar (ou retomar se já carregada)
        # É mais seguro recarregar caso tenha havido algum problema
        try:
             # Verificar se a música está carregada antes de tocar/pausar
             if pygame.mixer.music.get_busy():
                 pygame.mixer.music.unpause() # Se estava pausada, retoma
             else:
                 # Se não estava tocando, carrega e toca
                 load_and_play_music()
        except pygame.error as e:
             print(f"Erro ao tentar tocar/retomar música: {e}")
             # Tenta carregar de novo como fallback
             load_and_play_music()
    else:
        # Se a música foi desativada, pausar
        try:
            pygame.mixer.music.pause()
        except pygame.error as e:
             print(f"Erro ao tentar pausar música: {e}")


# Constantes
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 900
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
CYAN = (0, 255, 255)

# Cores para o fundo amadeirado
WOOD_LIGHT = (240, 220, 180)
WOOD_MEDIUM = (210, 180, 140)
WOOD_DARK = (160, 120, 90)

# Lista de cores para as peças
PIECE_COLORS = [
    (255, 0, 0),      # Vermelho
    (0, 255, 0),      # Verde
    (0, 0, 255),      # Azul
    (255, 255, 0),    # Amarelo
    (255, 0, 255),    # Magenta
    (0, 255, 255),    # Ciano
    (255, 165, 0),    # Laranja
    (128, 0, 128),    # Roxo
    (165, 42, 42),    # Marrom
    (64, 224, 208)    # Turquesa
]

# Configuração da tela
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Woodblock Puzzle")
clock = pygame.time.Clock()

# Fontes (AUMENTADAS)
title_font = pygame.font.SysFont("Arial", 60, bold=True) # Aumentado de 48
menu_font = pygame.font.SysFont("Arial", 45)         # Aumentado de 36
button_font = pygame.font.SysFont("Arial", 30)        # Aumentado de 24
game_font = pygame.font.SysFont("Arial", 25)          # Aumentado de 20

#######################
# Classe Piece (Peça) #
#######################
class Piece:
    def __init__(self, shape=None, color=None):
        """
        Inicializa uma peça com uma forma e cor específicas.
        """
        if shape is None:
            self.shape = self.generate_random_shape()
        else:
            self.shape = shape

        if color is None:
            self.color = random.choice(PIECE_COLORS)
        else:
            self.color = color

        self.rows, self.cols = self.shape.shape

    def copy(self):
        """ Cria uma cópia profunda da peça. """
        return Piece(shape=self.shape.copy(), color=self.color)

    def generate_random_shape(self):
        """ Gera uma forma aleatória para a peça. """
        shapes = [
            np.array([[1]]),
            np.array([[1, 1]]), np.array([[1], [1]]),
            np.array([[1, 1, 1]]), np.array([[1], [1], [1]]),
            np.array([[1, 1], [1, 0]]), np.array([[1, 1], [0, 1]]),
            np.array([[1, 0], [1, 1]]), np.array([[0, 1], [1, 1]]),
            np.array([[1, 1, 0], [0, 1, 0]]), np.array([[0, 1, 0], [1, 1, 0]]),
            np.array([[1, 1, 1, 1]]), np.array([[1], [1], [1], [1]]),
            np.array([[1, 1], [1, 1]]),
            np.array([[1, 1, 0], [0, 1, 1]]), np.array([[0, 1, 1], [1, 1, 0]]),
            np.array([[1, 0, 0], [1, 1, 1]]), np.array([[0, 0, 1], [1, 1, 1]]),
            np.array([[1, 1, 1], [1, 0, 0]]), np.array([[1, 1, 1], [0, 0, 1]]),
            np.array([[1, 0], [1, 0], [1, 1]]), np.array([[0, 1], [0, 1], [1, 1]]),
            np.array([[1, 1], [1, 0], [1, 0]]), np.array([[1, 1], [0, 1], [0, 1]])
        ]
        return random.choice(shapes)

    def flip_horizontal(self):
        """ Inverte a peça horizontalmente. """
        self.shape = np.fliplr(self.shape)

    def flip_vertical(self):
        """ Inverte a peça verticalmente. """
        self.shape = np.flipud(self.shape)

    def draw(self, surface, x, y, cell_size):
        """ Desenha a peça na superfície. """
        for row in range(self.rows):
            for col in range(self.cols):
                if self.shape[row, col] == 1:
                    rect = pygame.Rect(
                        x + col * cell_size,
                        y + row * cell_size,
                        cell_size,
                        cell_size
                    )
                    pygame.draw.rect(surface, self.color, rect)
                    pygame.draw.rect(surface, BLACK, rect, 1)  # Borda

#######################
# Classe Board (Tabuleiro) #
#######################
class Board:
    def __init__(self, size, difficulty="medium"):
        """ Inicializa o tabuleiro do jogo. """
        self.size = size
        self.difficulty = difficulty
        self.grid = np.zeros((size, size), dtype=int)
        self.colors = np.zeros((size, size, 3), dtype=int)
        self.score = 0

        if difficulty == "easy":
            self.num_initial_blocks = int(size * size * 0.1)
        elif difficulty == "medium":
            self.num_initial_blocks = int(size * size * 0.2)
        else: # hard
            self.num_initial_blocks = int(size * size * 0.3)

        self.initialize_board()
        self.available_pieces = [Piece() for _ in range(3)]

    def copy(self):
        """ Cria uma cópia profunda do tabuleiro. """
        new_board = Board(self.size, self.difficulty)
        new_board.grid = self.grid.copy()
        new_board.colors = self.colors.copy()
        new_board.score = self.score
        # Copiar available_pieces também é importante para a IA não modificar o original
        new_board.available_pieces = [p.copy() if p else None for p in self.available_pieces]
        return new_board

    def initialize_board(self):
        """ Inicializa o tabuleiro com blocos aleatórios. """
        self.grid.fill(0)
        self.colors.fill(0)
        blocks_added = 0
        while blocks_added < self.num_initial_blocks:
            row = random.randint(0, self.size - 1)
            col = random.randint(0, self.size - 1)
            if self.grid[row, col] == 0:
                self.grid[row, col] = 1
                self.colors[row, col] = random.choice(PIECE_COLORS)
                blocks_added += 1

    def can_place_piece(self, piece, row, col):
        """ Verifica se uma peça pode ser colocada em uma posição específica. """
        if piece is None: return False # Segurança
        if row < 0 or col < 0 or row + piece.rows > self.size or col + piece.cols > self.size:
            return False
        for r in range(piece.rows):
            for c in range(piece.cols):
                if piece.shape[r, c] == 1 and self.grid[row + r, col + c] == 1:
                    return False
        return True

    def place_piece(self, piece, row, col):
        """ Coloca uma peça no tabuleiro. """
        if piece is None: return False # Segurança
        if not self.can_place_piece(piece, row, col):
            return False
        for r in range(piece.rows):
            for c in range(piece.cols):
                if piece.shape[r, c] == 1:
                    self.grid[row + r, col + c] = 1
                    self.colors[row + r, col + c] = piece.color
        rows_cleared, cols_cleared = self.clear_lines()
        if rows_cleared > 0 or cols_cleared > 0:
            self.update_score(rows_cleared, cols_cleared)
        return True

    def clear_lines(self):
        """ Verifica e elimina linhas e colunas completas. """
        rows_to_clear = [r for r in range(self.size) if np.all(self.grid[r, :] == 1)]
        cols_to_clear = [c for c in range(self.size) if np.all(self.grid[:, c] == 1)]

        if not rows_to_clear and not cols_to_clear:
            return 0, 0

        # Criar cópia para animação (opcional, mas pode ser útil)
        # cleared_mask = np.zeros_like(self.grid)

        for row in rows_to_clear:
            self.grid[row, :] = 0
            self.colors[row, :] = 0
            # cleared_mask[row, :] = 1
        for col in cols_to_clear:
            self.grid[:, col] = 0
            self.colors[:, col] = 0
            # cleared_mask[:, col] = 1 # Marcar colunas também

        # TODO: Adicionar aqui uma pequena pausa ou animação se desejado

        return len(rows_to_clear), len(cols_to_clear)


    def update_score(self, rows_cleared, cols_cleared):
        """ Atualiza a pontuação. """
        base_points = 100
        size_multiplier = 1 if self.size == 5 else 2
        difficulty_multiplier = 1
        if self.difficulty == "medium": difficulty_multiplier = 1.5
        elif self.difficulty == "hard": difficulty_multiplier = 2.0
        combo_multiplier = 1 + 0.5 * (rows_cleared + cols_cleared - 1) if (rows_cleared + cols_cleared) > 0 else 1
        points = int(base_points * (rows_cleared + cols_cleared) * size_multiplier * difficulty_multiplier * combo_multiplier)
        self.score += points

    def generate_new_piece(self):
        """ Gera uma nova peça aleatória. """
        return Piece()

    def is_game_over(self):
        """ Verifica se o jogo acabou. """
        for piece in self.available_pieces:
            if piece is None: continue # Ignora espaços vazios
            # Otimização: Se a peça for maior que o tabuleiro, não pode ser colocada
            if piece.rows > self.size or piece.cols > self.size:
                continue
            for row in range(self.size - piece.rows + 1):
                for col in range(self.size - piece.cols + 1):
                    if self.can_place_piece(piece, row, col):
                        return False # Encontrou um movimento possível
        return True # Nenhuma peça pode ser colocada

    def draw(self, surface, x, y, cell_size):
        """ Desenha o tabuleiro na superfície. """
        board_width_pixels = self.size * cell_size
        board_height_pixels = self.size * cell_size
        board_rect = pygame.Rect(x, y, board_width_pixels, board_height_pixels)
        pygame.draw.rect(surface, GRAY, board_rect, border_radius=5) # Fundo ligeiramente diferente
        pygame.draw.rect(surface, BLACK, board_rect, 2, border_radius=5)

        for row in range(self.size):
            for col in range(self.size):
                cell_rect = pygame.Rect(
                    x + col * cell_size, y + row * cell_size,
                    cell_size, cell_size
                )
                if self.grid[row, col] == 1:
                    color = tuple(self.colors[row, col])
                    pygame.draw.rect(surface, color, cell_rect)
                else:
                    pygame.draw.rect(surface, WOOD_LIGHT, cell_rect) # Cor de fundo da célula vazia

                pygame.draw.rect(surface, WOOD_MEDIUM, cell_rect, 1) # Linhas da grelha

    # Modificado para aceitar e usar ui_cell_size
    def draw_available_pieces(self, surface, x, y, ui_cell_size):
        """
        Desenha as peças disponíveis na superfície.

        Args:
            surface: Superfície do pygame para desenhar
            x, y: Coordenadas do canto superior esquerdo da área das peças
            ui_cell_size: Tamanho de cada célula das peças na UI <<< MODIFICADO
        """
        spacing = 25  # Espaçamento aumentado entre as peças

        for i, piece in enumerate(self.available_pieces):
            if piece is None: continue # Adicionar verificação para caso a peça seja None

            # Usar ui_cell_size para calcular a área e posição
            # Assumir que a área de desenho deve ter espaço para uma peça 4x4 (ou o tamanho da peça, o que for maior)
            bg_width = max(4, piece.cols) * ui_cell_size
            bg_height = max(4, piece.rows) * ui_cell_size

            piece_area_x = x + i * (bg_width + spacing) # Calcular posição da área da peça
            piece_area_y = y

            # Desenhar fundo da área da peça
            bg_rect = pygame.Rect(piece_area_x, piece_area_y, bg_width, bg_height)
            pygame.draw.rect(surface, GRAY, bg_rect, border_radius=5) # Pequeno arredondamento
            pygame.draw.rect(surface, BLACK, bg_rect, 1, border_radius=5)

            # Centralizar a peça na área (usar ui_cell_size)
            offset_x = (bg_width - piece.cols * ui_cell_size) // 2
            offset_y = (bg_height - piece.rows * ui_cell_size) // 2

            # Desenhar a peça (passar ui_cell_size para o método draw da peça)
            piece.draw(surface, piece_area_x + offset_x, piece_area_y + offset_y, ui_cell_size)


# --- Classes de IA (GameState, AStarSearch, etc.) - Mantidas como estavam ---
# ... (O código das classes GameState, AStarSearch, GreedySearch, BFSSearch,
#      DFSSearch, DynamicStabilitySearch, CascadeSearch permanece o mesmo que você forneceu) ...
class GameState:
    def __init__(self, board, available_pieces, score=0, parent=None, action=None, depth=0):
        self.board = board
        self.available_pieces = available_pieces
        self.score = score
        self.parent = parent
        self.action = action
        self.depth = depth
    def __lt__(self, other): return self.score > other.score
    def get_possible_actions(self):
        actions = []
        for piece_index, piece in enumerate(self.available_pieces):
            if piece is None: continue
            for row in range(self.board.size - piece.rows + 1):
                for col in range(self.board.size - piece.cols + 1):
                    if self.board.can_place_piece(piece, row, col):
                        actions.append((piece_index, 0, row, col))
        return actions
    def apply_action(self, action):
        piece_index, rotation, row, col = action
        new_board = self.board.copy()
        new_pieces = [p.copy() if p else None for p in self.available_pieces]
        piece = new_pieces[piece_index]
        if new_board.place_piece(piece, row, col):
             new_pieces[piece_index] = new_board.generate_new_piece() # Gera nova peça APENAS se colocou com sucesso
        # Se place_piece falhar (o que não deveria acontecer se get_possible_actions estiver correto),
        # podemos querer lidar com isso, mas por agora assumimos que funciona.
        # Se a peça não puder ser colocada, o estado não deveria mudar muito,
        # mas a peça usada não seria substituída. Isso pode ser um problema para a IA.
        # Vamos garantir que generate_new_piece só acontece se place_piece retornar True.
        # A lógica atual já faz isso implicitamente dentro de place_piece.

        # CORREÇÃO: a peça usada deve ser removida ou substituída *após* ser usada
        # A lógica atual substitui a peça ANTES de saber se há game over, o que está errado.
        # Vamos refatorar ligeiramente. place_piece agora só coloca e retorna True/False.
        # A substituição acontece no nível do jogo (GamePlay/AIGamePlay).

        # Refatorando apply_action para refletir melhor o fluxo real:
        # 1. Copiar estado
        new_board_after_place = self.board.copy()
        new_pieces_after_place = [p.copy() if p else None for p in self.available_pieces]

        # 2. Tentar colocar a peça na cópia
        piece_to_place = new_pieces_after_place[piece_index]
        placed_successfully = new_board_after_place.place_piece(piece_to_place, row, col)

        # 3. Se colocou, "remover" a peça usada (ou gerar nova no lugar dela)
        if placed_successfully:
             new_pieces_after_place[piece_index] = new_board_after_place.generate_new_piece()
        else:
             # Se não conseguiu colocar (não deveria acontecer se veio de get_possible_actions),
             # o estado não muda efetivamente em relação à peça. Retornar o mesmo estado? Ou erro?
             # Por segurança, vamos assumir que a ação era válida.
             # Se não fosse, a busca da IA não deveria ter considerado esta ação.
             # Vamos manter a lógica original aqui, mas cientes da potencial inconsistência
             # se can_place_piece e place_piece não estiverem perfeitamente sincronizados.
             # A lógica original de substituir a peça parece ser a intenção para a simulação da IA.
             # Vamos reverter para a substituição original, mas garantir que generate_new_piece é chamado.
             new_pieces_after_place[piece_index] = new_board_after_place.generate_new_piece() # Mantém a substituição

        return GameState(
            board=new_board_after_place, # Usar o tabuleiro após a tentativa de colocar
            available_pieces=new_pieces_after_place,
            score=new_board_after_place.score,
            parent=self, action=action, depth=self.depth + 1
        )

    def is_terminal(self): return self.board.is_game_over()

# --- Classes AStar, Greedy, BFS, DFS, DynamicStability, Cascade ---
# MANTIDAS COMO ESTAVAM NO CÓDIGO FORNECIDO
class AStarSearch:
    def __init__(self): self.nodes_explored = 0; self.max_depth = 0
    def heuristic(self, state):
        score_value = state.score; board = state.board; potential = 0
        for i in range(board.size):
            row_filled = np.sum(board.grid[i, :]); col_filled = np.sum(board.grid[:, i])
            potential += (row_filled / board.size)**2*100 + (col_filled / board.size)**2*100
        empty_spaces = np.sum(board.grid == 0); space_value = empty_spaces * 5
        return score_value + potential + space_value
    def search(self, initial_state, max_iterations=1000):
        self.nodes_explored = 0; self.max_depth = 0; open_set = []; closed_set = set()
        f_value = self.heuristic(initial_state) # Heurística deve ser positiva aqui
        heapq.heappush(open_set, (f_value, initial_state)) # Armazenar (f_value, state)
        best_state = initial_state; best_score = initial_state.score; iterations = 0
        while open_set and iterations < max_iterations:
            iterations += 1
            # A* usa f = g + h. Aqui 'g' seria -profundidade ou 0, e 'h' a heurística.
            # A heurística atual parece mais um valor de estado 'v'.
            # Se quisermos A*, priorizamos f = profundidade + (-heuristica_potencial) ou algo assim.
            # A implementação atual parece mais uma Best-First Search baseada na heurística.
            # Vamos manter como está, mas notar que não é A* canônico.
            # Prioridade baseada no valor da heurística (maior é melhor).
            # Como heapq é min-heap, usamos -heuristic.
            f_value, current_state = heapq.heappop(open_set)
            self.nodes_explored += 1; self.max_depth = max(self.max_depth, current_state.depth)

            # Usar hash do grid para closed_set
            current_hash = hash(current_state.board.grid.tobytes())
            if current_hash in closed_set: continue
            closed_set.add(current_hash)

            if current_state.score > best_score: best_state = current_state; best_score = current_state.score
            if current_state.is_terminal():
                 # Mesmo se for terminal, pode não ser o melhor score encontrado
                 # break # Não fazer break necessariamente, continuar explorando outros ramos se max_iterations permitir
                 continue # Continua explorando outros nós na open_set

            for action in current_state.get_possible_actions():
                next_state = current_state.apply_action(action)
                next_hash = hash(next_state.board.grid.tobytes())
                if next_hash not in closed_set:
                    f_val = -self.heuristic(next_state) # Prioridade é -valor (maior valor tem menor f_val)
                    heapq.heappush(open_set, (f_val, next_state)) # Adiciona com prioridade

        path = []; state = best_state
        while state.parent is not None: path.append(state.action); state = state.parent
        path.reverse()
        # O score retornado deve ser o do best_state encontrado
        return path, best_state.score, self.nodes_explored, self.max_depth

class GreedySearch:
    def __init__(self): self.nodes_explored = 0; self.max_depth = 0
    def evaluate(self, state, action):
        next_state = state.apply_action(action); score_gain = next_state.score - state.score
        board = next_state.board; potential = 0
        for i in range(board.size):
            row_filled = np.sum(board.grid[i, :]); col_filled = np.sum(board.grid[:, i])
            potential += (row_filled / board.size)**2*50 + (col_filled / board.size)**2*50
        return score_gain + potential
    def search(self, initial_state, max_depth=100):
        self.nodes_explored = 0; self.max_depth = 0
        current_state = initial_state; path = []
        while len(path) < max_depth and not current_state.is_terminal():
            self.nodes_explored += 1; self.max_depth = max(self.max_depth, len(path))
            actions = current_state.get_possible_actions()
            if not actions: break
            best_action = None; best_value = float('-inf')
            for action in actions:
                value = self.evaluate(current_state, action)
                if value > best_value: best_value = value; best_action = action
            if best_action is None: break # Se não há ação boa, parar
            path.append(best_action); current_state = current_state.apply_action(best_action)
        return path, current_state.score, self.nodes_explored, self.max_depth

class BFSSearch:
    def __init__(self): self.nodes_explored = 0; self.max_depth = 0
    def search(self, initial_state, max_iterations=1000):
        self.nodes_explored = 0; self.max_depth = 0; queue = []; queue.append(initial_state)
        visited = set(); visited.add(hash(initial_state.board.grid.tobytes())) # Hash inicial
        best_state = initial_state; best_score = initial_state.score; iterations = 0
        while queue and iterations < max_iterations:
            iterations += 1; current_state = queue.pop(0); self.nodes_explored += 1
            self.max_depth = max(self.max_depth, current_state.depth)
            # Encontrou um estado com score melhor
            if current_state.score > best_score: best_state = current_state; best_score = current_state.score
            # Não parar no primeiro terminal, continuar busca até limite
            if current_state.is_terminal(): continue

            for action in current_state.get_possible_actions():
                next_state = current_state.apply_action(action)
                state_hash = hash(next_state.board.grid.tobytes())
                if state_hash not in visited:
                    visited.add(state_hash); queue.append(next_state)

        path = []; state = best_state
        while state.parent is not None: path.append(state.action); state = state.parent
        path.reverse()
        return path, best_state.score, self.nodes_explored, self.max_depth

class DFSSearch:
    def __init__(self): self.nodes_explored = 0; self.max_depth = 0
    def search(self, initial_state, max_depth_limit=20): # Renomeado para evitar conflito
        self.nodes_explored = 0; self.max_depth = 0; stack = []; stack.append(initial_state)
        visited = set() # Visited por profundidade pode ser necessário para evitar ciclos longos
        best_state = initial_state; best_score = initial_state.score
        while stack:
            current_state = stack.pop(); self.nodes_explored += 1
            self.max_depth = max(self.max_depth, current_state.depth)

            # Hash considerando profundidade para evitar voltar ao mesmo grid em menor profundidade
            state_hash = (hash(current_state.board.grid.tobytes()), current_state.depth)
            if state_hash in visited: continue
            visited.add(state_hash)

            if current_state.score > best_score: best_state = current_state; best_score = current_state.score
            # Não parar necessariamente no terminal, pode haver score melhor
            if current_state.is_terminal(): continue
            if current_state.depth >= max_depth_limit: continue

            # Adicionar ações à pilha (ordem pode importar, talvez inverter para explorar "melhores" primeiro?)
            possible_actions = current_state.get_possible_actions()
            # random.shuffle(possible_actions) # Opcional: Aleatorizar ordem
            for action in reversed(possible_actions): # Empilhar em ordem inversa para processar ~ordem normal
                next_state = current_state.apply_action(action)
                # Verifica hash simples (sem profundidade) para não adicionar se já explorado mais fundo
                simple_hash = hash(next_state.board.grid.tobytes())
                # Não vamos adicionar à pilha se já visitamos este *estado exato* nesta profundidade ou mais raso
                # A lógica de visited no início do loop já cuida disso.
                stack.append(next_state)

        path = []; state = best_state
        while state.parent is not None: path.append(state.action); state = state.parent
        path.reverse()
        return path, best_state.score, self.nodes_explored, self.max_depth

class DynamicStabilitySearch:
    def __init__(self): self.nodes_explored = 0; self.max_depth = 0
    def evaluate_stability(self, board):
        stability_score = 0; grid = board.grid; size = board.size
        for r in range(size):
            for c in range(size):
                if grid[r,c]==1:
                    n=0
                    if r>0 and grid[r-1,c]==1: n+=1
                    if r<size-1 and grid[r+1,c]==1: n+=1
                    if c>0 and grid[r,c-1]==1: n+=1
                    if c<size-1 and grid[r,c+1]==1: n+=1
                    stability_score += n*5
        q_size = max(1,size//2); q_counts=[0]*4
        for r in range(q_size):
             for c in range(q_size):
                  if r<size and c<size and grid[r,c]==1: q_counts[0]+=1
             for c in range(q_size, size):
                  if r<size and c<size and grid[r,c]==1: q_counts[1]+=1
        for r in range(q_size, size):
             for c in range(q_size):
                  if r<size and c<size and grid[r,c]==1: q_counts[2]+=1
             for c in range(q_size, size):
                  if r<size and c<size and grid[r,c]==1: q_counts[3]+=1
        if sum(q_counts) == 0: return stability_score # Evitar divisão por zero se tabuleiro vazio
        avg_b = sum(q_counts) / 4.0; variance = sum((ct-avg_b)**2 for ct in q_counts)/4.0
        stability_score -= variance*2
        return stability_score
    def evaluate(self, state, action):
        try:
            next_state = state.apply_action(action); score_gain = next_state.score - state.score
            stability = self.evaluate_stability(next_state.board); board = next_state.board; potential = 0
            for i in range(board.size):
                r_fill = sum(board.grid[i,:]); c_fill = sum(board.grid[:,i])
                potential += (r_fill/board.size)**2*100 + (c_fill/board.size)**2*100
            empty = np.sum(board.grid==0); space = empty*3
            return score_gain*2 + stability*1.5 + potential + space
        except Exception as e: print(f"Erro DS evaluate: {e}"); return float('-inf')
    def search(self, initial_state, max_depth=5): # Profundidade menor para heurísticas complexas
        # Esta é uma busca GULOSA usando a heurística complexa, não A* ou similar.
        # Similar ao GreedySearch, mas com função 'evaluate' diferente.
        try:
            self.nodes_explored=0; self.max_depth=0; current_state=initial_state; path=[]
            while len(path)<max_depth and not current_state.is_terminal():
                self.nodes_explored+=1; self.max_depth=max(self.max_depth, len(path))
                actions = current_state.get_possible_actions();
                if not actions: break
                best_action = None; best_value = float('-inf')
                for action in actions:
                    value = self.evaluate(current_state, action)
                    if value > best_value: best_value=value; best_action=action
                if best_action is not None:
                    path.append(best_action); current_state = current_state.apply_action(best_action)
                else: break
            return path, current_state.score, self.nodes_explored, self.max_depth
        except Exception as e: print(f"Erro DS search: {e}"); traceback.print_exc(); return [],0,0,0

class CascadeSearch:
    def __init__(self): self.nodes_explored = 0; self.max_depth = 0
    def evaluate_cascade_potential(self, board):
        try:
            cascade_score = 0; grid = board.grid; size = board.size
            near_comp_thresh = 0.7;
            for i in range(size):
                r_fill = sum(grid[i,:]); c_fill = sum(grid[:,i])
                r_pct = r_fill/size; c_pct = c_fill/size
                if r_pct >= near_comp_thresh and r_pct < 1.0: cascade_score += (r_pct**3)*200
                if c_pct >= near_comp_thresh and c_pct < 1.0: cascade_score += (c_pct**3)*200
            for r in range(size-1):
                for c in range(size-1):
                    if grid[r,c]==1 and grid[r+1,c+1]==1: cascade_score += 10
                    if r>0 and c<size-1 and grid[r,c+1]==1 and grid[r-1,c]==1: cascade_score += 10 # Erro aqui antes, corrigido
            visited = set()
            def count_group_size(r,c):
                if not (0<=r<size and 0<=c<size) or (r,c) in visited or grid[r,c]==0: return 0
                visited.add((r,c)); size_count=1
                size_count += count_group_size(r-1,c); size_count += count_group_size(r+1,c)
                size_count += count_group_size(r,c-1); size_count += count_group_size(r,c+1)
                return size_count
            for r in range(size):
                for c in range(size):
                    if grid[r,c]==1 and (r,c) not in visited:
                        group_size = count_group_size(r,c); cascade_score += group_size**1.5
            return cascade_score
        except Exception as e: print(f"Erro CS potential: {e}"); return 0
    def evaluate(self, state, action):
        try:
            next_state=state.apply_action(action); score_gain = next_state.score - state.score
            cascade_potential = self.evaluate_cascade_potential(next_state.board)
            elim_bonus = score_gain * 2 if score_gain > 0 else 0
            board = next_state.board; empty = np.sum(board.grid==0); space = empty*2
            return score_gain*3 + cascade_potential*2 + elim_bonus + space
        except Exception as e: print(f"Erro CS evaluate: {e}"); return float('-inf')
    def search(self, initial_state, max_depth=5): # Profundidade menor
        # Busca GULOSA usando a heurística de cascata.
        try:
            self.nodes_explored=0; self.max_depth=0; current_state=initial_state; path=[]
            while len(path)<max_depth and not current_state.is_terminal():
                self.nodes_explored+=1; self.max_depth=max(self.max_depth, len(path))
                actions = current_state.get_possible_actions()
                if not actions: break
                best_action=None; best_value = float('-inf')
                for action in actions:
                    value = self.evaluate(current_state, action)
                    if value > best_value: best_value=value; best_action=action
                if best_action is not None:
                     path.append(best_action); current_state = current_state.apply_action(best_action)
                else: break
            return path, current_state.score, self.nodes_explored, self.max_depth
        except Exception as e: print(f"Erro CS search: {e}"); traceback.print_exc(); return [],0,0,0

#######################
# Classe Button (Botão) #
# (Mantida como estava, funcional)
#######################
class Button:
    def __init__(self, x, y, width, height, text, color=(200, 200, 200), hover_color=(150, 150, 150)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.current_color = color
        self.is_hovered = False

    def draw(self, surface):
        pygame.draw.rect(surface, self.current_color, self.rect, border_radius=10)
        pygame.draw.rect(surface, BLACK, self.rect, 2, border_radius=10)
        text_surface = button_font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def update(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.current_color = self.hover_color
            self.is_hovered = True
        else:
            self.current_color = self.color
            self.is_hovered = False

    def is_clicked(self, event):
        # Verifica se o evento é um clique ESQUERDO do mouse E se o mouse está sobre o botão
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered:
            return True
        return False


#######################
# Classe GamePlay (Modo Humano) #
# (Com ajustes de UI e debug prints)
#######################
class GamePlay:
    def __init__(self, board_size, difficulty, game_mode):
        print(f"DEBUG: Entrando em GamePlay.__init__ com board_size={board_size}, difficulty={difficulty}") # DEBUG
        self.board_size = board_size
        self.difficulty = difficulty
        self.game_mode = game_mode
        print("DEBUG: Inicializando Board...") # DEBUG
        self.board = Board(board_size, difficulty)
        print("DEBUG: Board inicializado.") # DEBUG

        # Manter cálculo do cell_size para a GRELHA
        self.cell_size = min(500 // board_size, 60) # Sem alterações aqui para não afetar 10x10

        # Definir um tamanho de célula para a UI (peças fora do tabuleiro)
        self.ui_cell_size = 35 # Pode ajustar este valor

        # Calcular posição do tabuleiro para centralizar
        board_width_pixels = board_size * self.cell_size
        self.board_x = (SCREEN_WIDTH - board_width_pixels) // 2
        self.board_y = 150 # Ajustado Y para dar espaço ao título/score

        # Posição das peças disponíveis (usar ui_cell_size) - Centralizado
        piece_area_width = 4 * self.ui_cell_size # Largura da área de uma peça
        spacing = 25 # Espaço entre áreas de peças
        pieces_total_width = 3 * piece_area_width + 2 * spacing # 3 peças + 2 espaços
        self.pieces_x = (SCREEN_WIDTH - pieces_total_width) // 2
        self.pieces_y = self.board_y + board_width_pixels + 40 # Ajustado Y

        print("DEBUG: Posições calculadas.") # DEBUG

        # Peça selecionada
        self.selected_piece_index = None
        self.selected_piece_offset_x = 0
        self.selected_piece_offset_y = 0

        # Botão de voltar ao menu (USAR TAMANHOS ATUALIZADOS)
        back_button_width = 150 # Botão menor que os do menu principal
        back_button_height = 50
        self.back_button = Button(
            SCREEN_WIDTH - back_button_width - 20,
            SCREEN_HEIGHT - back_button_height - 20,
            back_button_width, back_button_height, "Menu"
        )
        print("DEBUG: Botão Voltar criado.") # DEBUG

        # Estado do jogo
        self.game_over = False

        # Área de previsão
        self.preview_row = None
        self.preview_col = None
        print("DEBUG: GamePlay.__init__ concluído.") # DEBUG


    def handle_events(self, event):
        mouse_pos = pygame.mouse.get_pos()

        # Botão Voltar tem prioridade
        if self.back_button.is_clicked(event):
            # Não precisamos de setar game_over aqui, apenas retornar ao menu
            return "menu"

        # Se o jogo acabou, qualquer clique/tecla retorna ao menu
        if self.game_over:
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                return "menu"
            return None # Ignora outros eventos se game over

        # Lógica de arrastar e soltar peças
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Verificar clique nas peças disponíveis
            for i, piece in enumerate(self.board.available_pieces):
                if piece is None: continue # Ignora se não há peça

                # Calcular a área de clique da peça usando ui_cell_size
                bg_width = max(4, piece.cols) * self.ui_cell_size
                bg_height = max(4, piece.rows) * self.ui_cell_size
                piece_area_x = self.pieces_x + i * (bg_width + 25) # Usar o mesmo espaçamento de draw
                piece_rect = pygame.Rect(piece_area_x, self.pieces_y, bg_width, bg_height)

                if piece_rect.collidepoint(mouse_pos):
                    self.selected_piece_index = i
                    # Calcular offset relativo ao canto da ÁREA da peça
                    self.selected_piece_offset_x = mouse_pos[0] - piece_area_x
                    self.selected_piece_offset_y = mouse_pos[1] - self.pieces_y
                    # Limpar previsão ao pegar nova peça
                    self.preview_row = None
                    self.preview_col = None
                    break # Sai do loop for assim que encontra a peça clicada

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.selected_piece_index is not None:
            # Soltar a peça
            piece = self.board.available_pieces[self.selected_piece_index]
            if piece is None: # Segurança
                 self.selected_piece_index = None
                 return None

            # Calcular posição de soltura na grelha
            # Ajustar pelo offset para o centro da peça arrastada (aproximado)
            piece_center_x = mouse_pos[0] - self.selected_piece_offset_x + (piece.cols * self.ui_cell_size) / 2
            piece_center_y = mouse_pos[1] - self.selected_piece_offset_y + (piece.rows * self.ui_cell_size) / 2

            board_col = int((piece_center_x - self.board_x) / self.cell_size)
            board_row = int((piece_center_y - self.board_y) / self.cell_size)

            # Tentar colocar a peça na posição calculada (canto superior esquerdo)
            if self.board.place_piece(piece, board_row, board_col):
                # Sucesso: gerar nova peça e verificar game over
                self.board.available_pieces[self.selected_piece_index] = self.board.generate_new_piece()
                if self.board.is_game_over():
                    self.game_over = True
            # Se não conseguiu colocar, a peça volta visualmente para a área (não precisa de código extra aqui)

            # Resetar seleção
            self.selected_piece_index = None
            self.preview_row = None
            self.preview_col = None

        elif event.type == pygame.MOUSEMOTION and self.selected_piece_index is not None:
             # Atualizar previsão enquanto arrasta
             piece = self.board.available_pieces[self.selected_piece_index]
             if piece is None: return None # Segurança

             # Calcular centro da peça arrastada
             piece_center_x = mouse_pos[0] - self.selected_piece_offset_x + (piece.cols * self.ui_cell_size) / 2
             piece_center_y = mouse_pos[1] - self.selected_piece_offset_y + (piece.rows * self.ui_cell_size) / 2

             # Calcular célula alvo na grelha
             target_col = int((piece_center_x - self.board_x) / self.cell_size)
             target_row = int((piece_center_y - self.board_y) / self.cell_size)

             # Verificar se pode colocar nesta posição
             if self.board.can_place_piece(piece, target_row, target_col):
                 self.preview_row = target_row
                 self.preview_col = target_col
             else:
                 # Se não pode colocar no alvo exato, limpar previsão
                 self.preview_row = None
                 self.preview_col = None

        return None # Nenhum estado de jogo alterado

    def update(self, mouse_pos):
        # Atualizar estado do botão (hover)
        self.back_button.update(mouse_pos)

    def draw(self, surface):
        # Desenhar o fundo amadeirado
        draw_wooden_background(surface)

        # Desenhar o tabuleiro (usar self.cell_size)
        self.board.draw(surface, self.board_x, self.board_y, self.cell_size)

        # Desenhar as peças disponíveis (USAR self.ui_cell_size)
        self.board.draw_available_pieces(surface, self.pieces_x, self.pieces_y, self.ui_cell_size)

        # Desenhar a previsão (usa self.cell_size porque é sobre a GRELHA)
        if self.selected_piece_index is not None and self.preview_row is not None and self.preview_col is not None:
            piece = self.board.available_pieces[self.selected_piece_index]
            if piece: # Segurança
                # Desenhar a previsão com transparência
                preview_surface = pygame.Surface((piece.cols * self.cell_size, piece.rows * self.cell_size), pygame.SRCALPHA)
                preview_surface.fill((0,0,0,0)) # Preencher com transparente
                # Reutilizar draw da peça com cor alterada
                temp_color = (0, 255, 0, 128) # Verde transparente para válido
                for r in range(piece.rows):
                    for c in range(piece.cols):
                        if piece.shape[r, c] == 1:
                            rect = pygame.Rect(c * self.cell_size, r * self.cell_size, self.cell_size, self.cell_size)
                            pygame.draw.rect(preview_surface, temp_color, rect)
                            pygame.draw.rect(preview_surface, (0,0,0,128), rect, 1) # Borda

                surface.blit(preview_surface, (self.board_x + self.preview_col * self.cell_size,
                                              self.board_y + self.preview_row * self.cell_size))

        # Desenhar a peça selecionada (seguindo o mouse) (USAR self.ui_cell_size)
        if self.selected_piece_index is not None:
            piece = self.board.available_pieces[self.selected_piece_index]
            if piece: # Segurança
                mouse_pos = pygame.mouse.get_pos()
                # Desenhar a peça arrastada com tamanho UI, posicionada pelo offset do clique
                draw_x = mouse_pos[0] - self.selected_piece_offset_x
                draw_y = mouse_pos[1] - self.selected_piece_offset_y
                piece.draw(surface, draw_x, draw_y, self.ui_cell_size)

        # Desenhar botão Voltar
        self.back_button.draw(surface)

        # Desenhar pontuação (usar fonte maior game_font, ajustar posição)
        score_text = game_font.render(f"Pontuação: {self.board.score}", True, BLACK)
        surface.blit(score_text, (30, 30))

        # Desenhar informações do jogo (usar fonte maior game_font, ajustar posição)
        info_text_str = f"Tabuleiro: {self.board_size}x{self.board_size} | Dificuldade: {self.difficulty}"
        info_text = game_font.render(info_text_str, True, BLACK)
        surface.blit(info_text, (30, 65)) # Abaixo da pontuação

        # Desenhar mensagem de game over (usar fontes maiores)
        if self.game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180)) # Um pouco mais escuro
            surface.blit(overlay, (0, 0))

            game_over_text = title_font.render("GAME OVER", True, RED)
            game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100)) # Ajustar Y
            surface.blit(game_over_text, game_over_rect)

            final_score_text = menu_font.render(f"Pontuação Final: {self.board.score}", True, WHITE)
            final_score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)) # Ajustar Y
            surface.blit(final_score_text, final_score_rect)

            # Instrução para continuar (usar fonte maior, ajustar Y)
            continue_text = button_font.render("Clique ou Pressione Tecla para voltar ao Menu", True, WHITE)
            continue_rect = continue_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80)) # Ajustar Y
            surface.blit(continue_text, continue_rect)


#######################
# Classe AIGamePlay (Modo IA) #
#######################

class AIGamePlay:
    def __init__(self, board_size, difficulty, algorithm):
        self.board_size = board_size
        self.difficulty = difficulty
        self.algorithm = algorithm
        self.board = Board(board_size, difficulty)
        
        # Calcular o tamanho das células com base no tamanho do tabuleiro
        self.cell_size = min(500 // board_size, 60)  # Aumentado para melhor visualização
        
        # Calcular a posição do tabuleiro para centralizá-lo
        self.board_x = (SCREEN_WIDTH - board_size * self.cell_size) // 2
        self.board_y = 120
        
        # Posição das peças disponíveis - Centralizado
        pieces_width = 3 * (4 * self.cell_size + 20)
        self.pieces_x = (SCREEN_WIDTH - pieces_width) // 2
        self.pieces_y = self.board_y + board_size * self.cell_size + 30
        
        # Botão de voltar ao menu
        self.back_button = Button(SCREEN_WIDTH - 120, SCREEN_HEIGHT - 60, 100, 40, "Menu")
        
        # Estado do jogo
        self.game_over = False
        self.running = True
        self.move_delay = 500  # Atraso entre movimentos em milissegundos
        self.last_move_time = pygame.time.get_ticks()
        
        # Informações do algoritmo
        self.moves_made = 0
        self.nodes_explored = 0
        self.max_depth = 0
        
        # Inicializar o algoritmo de IA
        self.ai_algorithm = self.initialize_algorithm()
        
        # Plano de ações (movimentos) calculado pelo algoritmo
        self.action_plan = []
        
    def initialize_algorithm(self):
        """
        Inicializa o algoritmo de IA com base na seleção do usuário.
        """
        try:
            if self.algorithm == "astar":
                return AStarSearch()
            elif self.algorithm == "greedy":
                return GreedySearch()
            elif self.algorithm == "bfs":
                return BFSSearch()
            elif self.algorithm == "dfs":
                return DFSSearch()
            elif self.algorithm == "dynamic_stability":
                return DynamicStabilitySearch()
            elif self.algorithm == "cascade":
                return CascadeSearch()
            else:
                # Fallback para Greedy se algo der errado
                return GreedySearch()
        except Exception as e:
            print(f"Erro ao inicializar algoritmo: {e}")
            return GreedySearch()  # Fallback seguro
            
    def handle_events(self, event):
        # Verificar clique no botão de voltar
        if self.back_button.is_clicked(event):
            self.running = False
            return "menu"
            
        # Verificar se o jogo acabou
        if self.game_over:
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                self.running = False
                return "menu"
                
        return None
        
    def update(self, mouse_pos):
        # Atualizar botão de voltar
        self.back_button.update(mouse_pos)
        
        # Se o jogo estiver rodando e não tiver acabado, fazer um movimento
        current_time = pygame.time.get_ticks()
        if self.running and not self.game_over and current_time - self.last_move_time > self.move_delay:
            self.make_ai_move()
            self.last_move_time = current_time
            
    def make_ai_move(self):
        """
        Executa um movimento da IA com base no algoritmo selecionado.
        """
        try:
            # Se não tiver um plano de ações, calcular um novo
            if not self.action_plan:
                # Criar um estado inicial para o algoritmo
                initial_state = GameState(
                    board=self.board.copy(),  # Usar cópia para evitar modificações indesejadas
                    available_pieces=[piece.copy() for piece in self.board.available_pieces]  # Copiar peças também
                )
                
                # Executar o algoritmo para obter um plano de ações
                if self.algorithm == "astar":
                    self.action_plan, final_score, nodes, depth = self.ai_algorithm.search(initial_state, max_iterations=100)
                elif self.algorithm == "greedy":
                    self.action_plan, final_score, nodes, depth = self.ai_algorithm.search(initial_state, max_depth=20)
                elif self.algorithm == "bfs":
                    self.action_plan, final_score, nodes, depth = self.ai_algorithm.search(initial_state, max_iterations=100)
                elif self.algorithm == "dfs":
                    self.action_plan, final_score, nodes, depth = self.ai_algorithm.search(initial_state, max_depth=10)
                elif self.algorithm == "dynamic_stability":
                    self.action_plan, final_score, nodes, depth = self.ai_algorithm.search(initial_state, max_depth=5)
                elif self.algorithm == "cascade":
                    self.action_plan, final_score, nodes, depth = self.ai_algorithm.search(initial_state, max_depth=5)
                    
                # Atualizar estatísticas
                self.nodes_explored = nodes
                self.max_depth = depth
                
            # Se tiver ações no plano, executar a próxima
            if self.action_plan:
                # Obter a próxima ação
                piece_index, rotation, row, col = self.action_plan.pop(0)
                
                # Colocar a peça no tabuleiro (sem rotação)
                piece = self.board.available_pieces[piece_index]
                if self.board.place_piece(piece, row, col):
                    # Peça colocada com sucesso, gerar nova peça
                    self.board.available_pieces[piece_index] = self.board.generate_new_piece()
                    self.moves_made += 1
                    
            # Se não tiver mais ações ou o jogo acabou, verificar game over
            if not self.action_plan or self.board.is_game_over():
                # Recalcular um novo plano se ainda não acabou
                if not self.board.is_game_over():
                    self.action_plan = []  # Limpar o plano para recalcular na próxima atualização
                else:
                    self.game_over = True
        except Exception as e:
            print(f"Erro ao fazer movimento da IA: {e}")
            traceback.print_exc()
            # Em caso de erro, limpar o plano para tentar novamente na próxima atualização
            self.action_plan = []
            
    def draw(self, surface):
        # Desenhar o fundo amadeirado
        draw_wooden_background(surface)
        
        # Desenhar o tabuleiro
        self.board.draw(surface, self.board_x, self.board_y, self.cell_size)
        
        # Desenhar as peças disponíveis
        self.board.draw_available_pieces(surface, self.pieces_x, self.pieces_y, self.cell_size)
        
        # Desenhar botão de voltar
        self.back_button.draw(surface)
        
        # Desenhar pontuação
        score_text = game_font.render(f"Pontuação: {self.board.score}", True, BLACK)
        surface.blit(score_text, (20, 20))
        
        # Desenhar informações do jogo
        info_text = game_font.render(
            f"Tabuleiro: {self.board_size}x{self.board_size} | Dificuldade: {self.difficulty} | Algoritmo: {self.algorithm}",
            True, BLACK
        )
        surface.blit(info_text, (20, 50))
        
        # Desenhar estatísticas do algoritmo
        stats_text = game_font.render(
            f"Movimentos: {self.moves_made} | Nós explorados: {self.nodes_explored} | Profundidade máx: {self.max_depth}",
            True, BLACK
        )
        surface.blit(stats_text, (20, 80))
        
        # Desenhar mensagem de game over
        if self.game_over:
            # Fundo semi-transparente
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))
            surface.blit(overlay, (0, 0))
            
            # Mensagem de game over
            game_over_text = title_font.render("GAME OVER", True, RED)
            game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
            surface.blit(game_over_text, game_over_rect)
            
            # Pontuação final
            final_score_text = menu_font.render(f"Pontuação Final: {self.board.score}", True, WHITE)
            final_score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
            surface.blit(final_score_text, final_score_rect)
            
            # Estatísticas do algoritmo
            ai_stats_text = button_font.render(
                f"Movimentos: {self.moves_made} | Nós explorados: {self.nodes_explored}",
                True, WHITE
            )
            ai_stats_rect = ai_stats_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
            surface.blit(ai_stats_text, ai_stats_rect)
            
            # Instrução para continuar
            continue_text = button_font.render("Clique para continuar", True, WHITE)
            continue_rect = continue_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
            surface.blit(continue_text, continue_rect)

#######################
# Função para desenhar o fundo amadeirado #
#######################

def draw_wooden_background(surface):
    """
    Desenha um fundo amadeirado claro na superfície.
    """
    # Preencher o fundo com a cor base
    surface.fill(WOOD_LIGHT)
    
    # Desenhar padrões de madeira (linhas verticais com variação de cor)
    grain_spacing = 20
    grain_width_range = (2, 5)
    
    for x in range(0, SCREEN_WIDTH, grain_spacing):
        # Variação aleatória na posição para um efeito mais natural
        offset = random.randint(-5, 5)
        x_pos = x + offset
        
        # Largura variável para cada linha
        width = random.randint(*grain_width_range)
        
        # Cor variável para cada linha (tons de madeira)
        color_variation = random.randint(-20, 20)
        grain_color = (
            min(255, max(0, WOOD_MEDIUM[0] + color_variation)),
            min(255, max(0, WOOD_MEDIUM[1] + color_variation)),
            min(255, max(0, WOOD_MEDIUM[2] + color_variation))
        )
        
        # Desenhar a linha vertical
        pygame.draw.line(surface, grain_color, (x_pos, 0), (x_pos, SCREEN_HEIGHT), width)
    
    # Desenhar alguns nós de madeira para um efeito mais realista
    num_knots = random.randint(3, 7)
    for _ in range(num_knots):
        x = random.randint(0, SCREEN_WIDTH)
        y = random.randint(0, SCREEN_HEIGHT)
        radius = random.randint(5, 15)
        
        # Desenhar círculos concêntricos para o nó
        pygame.draw.circle(surface, WOOD_DARK, (x, y), radius)
        pygame.draw.circle(surface, WOOD_MEDIUM, (x, y), radius - 2)
        
        # Desenhar anéis ao redor do nó
        for r in range(radius + 5, radius + 25, 5):
            # Círculo não completo (arco)
            start_angle = random.randint(0, 30)
            end_angle = random.randint(330, 360)
            rect = pygame.Rect(x - r, y - r, r * 2, r * 2)
            pygame.draw.arc(surface, WOOD_DARK, rect, 
                           start_angle * (3.14159 / 180), 
                           end_angle * (3.14159 / 180), 
                           2)

#######################
# Classe Game (Jogo Principal) #
#######################

class Game:
    def __init__(self):
        self.state = "menu"
        self.best_score = 0
        self.load_best_score()
        
        # Carregar e iniciar a música de fundo
        load_and_play_music()
        
        # Botões do menu principal
        button_width = 360   # Aumentado de 300
        button_height = 60   # Aumentado de 50
        button_x = SCREEN_WIDTH // 2 - button_width // 2
        button_spacing = 85 # Aumentado de 70
        menu_start_y = 250 # Ajustar Y inicial para centralizar melhor
        self.button_x = SCREEN_WIDTH // 2 - button_width // 2

        self.menu_buttons = [
            Button(button_x, menu_start_y, button_width, button_height, "Jogar"),
            Button(button_x, menu_start_y + button_spacing, button_width, button_height, "Melhor Pontuação"),
            Button(button_x, menu_start_y + 2 * button_spacing, button_width, button_height, "Regras"),
            Button(button_x, menu_start_y + 3 * button_spacing, button_width, button_height, "Configurações"),
            Button(button_x, menu_start_y + 4 * button_spacing, button_width, button_height, "Sair")
        ]
        
        # Botões de seleção de tabuleiro
        board_start_y = 280 # Ajustar Y
        self.board_buttons = [
            Button(button_x, board_start_y, button_width, button_height, "Tabuleiro 5x5"),
            Button(button_x, board_start_y + button_spacing, button_width, button_height, "Tabuleiro 10x10"),
            Button(button_x, board_start_y + 3 * button_spacing, button_width, button_height, "Voltar") # Ajustar Y se necessário
        ]

        # Botões de dificuldade (Usar novos tamanhos e espaçamento)
        difficulty_start_y = 250 # Ajustar Y
        self.difficulty_buttons = [
            Button(button_x, difficulty_start_y, button_width, button_height, "Fácil"),
            Button(button_x, difficulty_start_y + button_spacing, button_width, button_height, "Médio"),
            Button(button_x, difficulty_start_y + 2 * button_spacing, button_width, button_height, "Difícil"),
            Button(button_x, difficulty_start_y + 4 * button_spacing, button_width, button_height, "Voltar") # Ajustar Y se necessário
        ]

        # Botões de modo de jogo (Usar novos tamanhos e espaçamento)
        mode_start_y = 150 # Ajustar Y
        mode_spacing = 75 # Pode precisar de um espaçamento ligeiramente diferente aqui
        self.mode_buttons = [
            Button(button_x, mode_start_y, button_width, button_height, "Humano"),
            Button(button_x, mode_start_y + mode_spacing, button_width, button_height, "A*"),
            Button(button_x, mode_start_y + 2 * mode_spacing, button_width, button_height, "Greedy Search"),
            Button(button_x, mode_start_y + 3 * mode_spacing, button_width, button_height, "BFS"),
            Button(button_x, mode_start_y + 4 * mode_spacing, button_width, button_height, "DFS"),
            Button(button_x, mode_start_y + 5 * mode_spacing, button_width, button_height, "Estabilidade Dinâmica"),
            Button(button_x, mode_start_y + 6 * mode_spacing, button_width, button_height, "Cascata"),
            Button(button_x, mode_start_y + 8 * mode_spacing, button_width, button_height, "Voltar") # Ajustar Y se necessário
        ]

        # Botões de configurações de som (Usar novos tamanhos e espaçamento)
        settings_start_y = 250 # Ajustar Y
        self.sound_buttons = [
            Button(button_x, settings_start_y, button_width, button_height, "Som: Ligado" if MUSIC_ENABLED else "Som: Desligado"),
            Button(button_x, settings_start_y + button_spacing, button_width, button_height, "Volume +"),
            Button(button_x, settings_start_y + 2 * button_spacing, button_width, button_height, "Volume -"),
            Button(button_x, settings_start_y + 4 * button_spacing, button_width, button_height, "Voltar") # Ajustar Y se necessário
        ]
        
        # Configurações do jogo
        self.board_size = 5  # Padrão: 5x5
        self.difficulty = "medium"  # Padrão: médio
        self.game_mode = "human"  # Padrão: humano
        
        # Instância do jogo
        self.gameplay = None
        
    def load_best_score(self):
        # Carrega a melhor pontuação do arquivo, se existir
        try:
            if os.path.exists("best_score.txt"):
                with open("best_score.txt", "r") as f:
                    self.best_score = int(f.read().strip())
        except:
            self.best_score = 0
            
    def save_best_score(self):
        # Salva a melhor pontuação em um arquivo
        with open("best_score.txt", "w") as f:
            f.write(str(self.best_score))
            
    def run(self):
        running = True
        
        while running:
            mouse_pos = pygame.mouse.get_pos()
            
            # Gerenciamento de eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
                # Gerenciamento de cliques nos botões
                if self.state == "menu":
                    self.handle_menu_events(event)
                elif self.state == "board_selection":
                    self.handle_board_selection_events(event)
                elif self.state == "difficulty_selection":
                    self.handle_difficulty_selection_events(event)
                elif self.state == "mode_selection":
                    self.handle_mode_selection_events(event)
                elif self.state == "best_score":
                    if event.type == pygame.KEYDOWN or (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                        self.state = "menu"
                elif self.state == "rules":
                    if event.type == pygame.KEYDOWN or (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                        self.state = "menu"
                elif self.state == "settings":
                    self.handle_settings_events(event)
                elif self.state == "game":
                    # Gerenciar eventos do jogo
                    if self.gameplay:
                        result = self.gameplay.handle_events(event)
                        if result == "menu":
                            self.state = "menu"
                            
                            # Atualizar melhor pontuação, se necessário
                            if hasattr(self.gameplay, 'board') and self.gameplay.board.score > self.best_score:
                                self.best_score = self.gameplay.board.score
                                self.save_best_score()
                                
                            self.gameplay = None
            
            # Atualização dos botões e elementos do jogo
            if self.state == "menu":
             for button in self.menu_buttons:
                button.update(mouse_pos)
            elif self.state == "board_selection":
             for button in self.board_buttons:
                button.update(mouse_pos)
            elif self.state == "difficulty_selection":
             for button in self.difficulty_buttons:
                button.update(mouse_pos)
            elif self.state == "mode_selection":
             for button in self.mode_buttons:
                button.update(mouse_pos)
        # ADICIONADO: Atualizar botões de configurações
            elif self.state == "settings":
             for button in self.sound_buttons:
                button.update(mouse_pos)
            elif self.state == "game":
             if self.gameplay:
                self.gameplay.update(mouse_pos)
            
            # Renderização
            # Desenhar o fundo amadeirado em todos os estados
            draw_wooden_background(screen)
            
            if self.state == "menu":
                self.draw_menu()
            elif self.state == "board_selection":
                self.draw_board_selection()
            elif self.state == "difficulty_selection":
                self.draw_difficulty_selection()
            elif self.state == "mode_selection":
                self.draw_mode_selection()
            elif self.state == "best_score":
                self.draw_best_score()
            elif self.state == "rules":
                self.draw_rules()
            elif self.state == "settings":
                self.draw_settings()
            elif self.state == "game":
                if self.gameplay:
                    self.gameplay.draw(screen)
            
            pygame.display.flip()
            clock.tick(FPS)
            
        pygame.quit()
        sys.exit()
        
    def handle_menu_events(self, event):
        if self.menu_buttons[0].is_clicked(event):  # Jogar
            self.state = "board_selection"
        elif self.menu_buttons[1].is_clicked(event):  # Melhor Pontuação
            self.state = "best_score"
        elif self.menu_buttons[2].is_clicked(event):  # Regras
            self.state = "rules"
        elif self.menu_buttons[3].is_clicked(event):  # Configurações
            self.state = "settings"
        elif self.menu_buttons[4].is_clicked(event):  # Sair
            pygame.quit()
            sys.exit()
            
    def handle_board_selection_events(self, event):
        if self.board_buttons[0].is_clicked(event):  # 5x5
            self.board_size = 5
            self.state = "difficulty_selection"
        elif self.board_buttons[1].is_clicked(event):  # 10x10
            self.board_size = 10
            self.state = "difficulty_selection"
        elif self.board_buttons[2].is_clicked(event):  # Voltar
            self.state = "menu"
            
    def handle_difficulty_selection_events(self, event):
        if self.difficulty_buttons[0].is_clicked(event):  # Fácil
            self.difficulty = "easy"
            self.state = "mode_selection"
        elif self.difficulty_buttons[1].is_clicked(event):  # Médio
            self.difficulty = "medium"
            self.state = "mode_selection"
        elif self.difficulty_buttons[2].is_clicked(event):  # Difícil
            self.difficulty = "hard"
            self.state = "mode_selection"
        elif self.difficulty_buttons[3].is_clicked(event):  # Voltar
            self.state = "board_selection"
            
    def handle_settings_events(self, event):
        # Verificar cliques nos botões de configurações (CORRIGIDO)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Botão de ligar/desligar som
            if self.sound_buttons[0].is_clicked(event): # Usar is_clicked(event)
                toggle_music()
                # Atualizar o texto do botão
                self.sound_buttons[0].text = "Som: Ligado" if MUSIC_ENABLED else "Som: Desligado"

            # Botão de aumentar volume
            elif self.sound_buttons[1].is_clicked(event): # Usar is_clicked(event)
                new_volume = min(1.0, MUSIC_VOLUME + 0.1)
                set_music_volume(new_volume)

            # Botão de diminuir volume
            elif self.sound_buttons[2].is_clicked(event): # Usar is_clicked(event)
                new_volume = max(0.0, MUSIC_VOLUME - 0.1)
                set_music_volume(new_volume)

            # Botão de voltar
            elif self.sound_buttons[3].is_clicked(event): # Usar is_clicked(event)
                self.state = "menu"
            
    def handle_mode_selection_events(self, event):
        if self.mode_buttons[0].is_clicked(event):  # Humano
            self.game_mode = "human"
            self.state = "game"
            self.start_game()
        elif self.mode_buttons[1].is_clicked(event):  # A*
            self.game_mode = "astar"
            self.state = "game"
            self.start_game()
        elif self.mode_buttons[2].is_clicked(event):  # Greedy Search
            self.game_mode = "greedy"
            self.state = "game"
            self.start_game()
        elif self.mode_buttons[3].is_clicked(event):  # BFS
            self.game_mode = "bfs"
            self.state = "game"
            self.start_game()
        elif self.mode_buttons[4].is_clicked(event):  # DFS
            self.game_mode = "dfs"
            self.state = "game"
            self.start_game()
        elif self.mode_buttons[5].is_clicked(event):  # Estabilidade Dinâmica
            self.game_mode = "dynamic_stability"
            self.state = "game"
            self.start_game()
        elif self.mode_buttons[6].is_clicked(event):  # Cascata
            self.game_mode = "cascade"
            self.state = "game"
            self.start_game()
        elif self.mode_buttons[7].is_clicked(event):  # Voltar
            self.state = "difficulty_selection"
            
    def start_game(self):
        # Inicializa o jogo com as configurações selecionadas
        try:
            if self.game_mode == "human":
                self.gameplay = GamePlay(self.board_size, self.difficulty, self.game_mode)
            else:
                self.gameplay = AIGamePlay(self.board_size, self.difficulty, self.game_mode)
        except Exception as e:
            print(f"Erro ao iniciar o jogo: {e}")
            traceback.print_exc()
            self.state = "menu"  # Voltar ao menu em caso de erro
        
    def draw_menu(self):
        # Desenha o título (Ajustar Y)
        title_surface = title_font.render("Woodblock Puzzle", True, BLACK)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 120)) # Ajustado Y
        screen.blit(title_surface, title_rect)

        # Desenha os botões (já usam as novas posições/tamanhos)
        for button in self.menu_buttons:
            button.draw(screen)

    def draw_board_selection(self):
        # Desenha o título (Ajustar Y)
        title_surface = title_font.render("Selecione o Tabuleiro", True, BLACK)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 120)) # Ajustado Y
        screen.blit(title_surface, title_rect)
        for button in self.board_buttons: button.draw(screen)

    def draw_difficulty_selection(self):
        # Desenha o título (Ajustar Y)
        title_surface = title_font.render("Selecione a Dificuldade", True, BLACK)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 120)) # Ajustado Y
        screen.blit(title_surface, title_rect)
        for button in self.difficulty_buttons: button.draw(screen)

    def draw_mode_selection(self):
        # Desenha o título (Ajustar Y)
        title_surface = title_font.render("Selecione o Modo de Jogo", True, BLACK)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 80)) # Ajustado Y
        screen.blit(title_surface, title_rect)
        for button in self.mode_buttons: button.draw(screen)

    def draw_best_score(self):
        # Desenha o título (Ajustar Y)
        title_surface = title_font.render("Melhor Pontuação", True, BLACK)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 120)) # Ajustado Y
        screen.blit(title_surface, title_rect)

        # Desenha a pontuação (usar fonte maior, ajustar Y)
        score_surface = menu_font.render(f"Pontuação: {self.best_score}", True, BLACK)
        score_rect = score_surface.get_rect(center=(SCREEN_WIDTH // 2, 300)) # Ajustado Y
        screen.blit(score_surface, score_rect)

        # Instrução para voltar (usar fonte maior, ajustar Y)
        back_surface = button_font.render("Clique para voltar", True, BLACK)
        back_rect = back_surface.get_rect(center=(SCREEN_WIDTH // 2, 550)) # Ajustado Y
        screen.blit(back_surface, back_rect)

    def draw_rules(self):
        # Desenha o título (Ajustar Y)
        title_surface = title_font.render("Regras do Jogo", True, BLACK)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 80)) # Ajustado Y
        screen.blit(title_surface, title_rect)

        rules = [
            "- O objetivo é completar linhas e colunas no tabuleiro.",
            "- O jogador tem 3 peças disponíveis para colocar no tabuleiro.",
            "- Quando uma peça é colocada, uma nova é gerada.",
            "- Ao completar uma linha ou coluna, ela é eliminada.",
            "- O jogo termina quando nenhuma das 3 peças disponíveis",
            "  couber nos espaços vazios do tabuleiro."
        ]
        rules_start_y = 180 # Ajustar Y
        rules_spacing = 50  # Aumentar espaçamento entre linhas
        for i, rule in enumerate(rules):
            # Usar fonte maior
            rule_surface = button_font.render(rule, True, BLACK)
            # Recalcular posição centralizada
            rule_rect = rule_surface.get_rect(center=(SCREEN_WIDTH // 2, rules_start_y + i * rules_spacing)) # Alinhar à esquerda perto do centro
            screen.blit(rule_surface, rule_rect)

        # Instrução para voltar (usar fonte maior, ajustar Y)
        back_surface = button_font.render("Clique para voltar", True, BLACK)
        back_rect = back_surface.get_rect(center=(SCREEN_WIDTH // 2, 600)) # Ajustado Y
        screen.blit(back_surface, back_rect)

    def draw_settings(self):
         # Desenha o título (Ajustar Y)
        title_surface = title_font.render("Configurações", True, BLACK)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 120)) # Ajustado Y
        screen.blit(title_surface, title_rect)

        # Desenha os botões (já usam as novas posições/tamanhos)
        for button in self.sound_buttons:
            button.draw(screen)

        # Exibe o volume atual (usar fonte maior, ajustar Y)
        volume_text = f"Volume atual: {int(MUSIC_VOLUME * 100)}%"
        volume_surface = menu_font.render(volume_text, True, BLACK)
        # Colocar abaixo dos botões de +/-
        volume_y = self.sound_buttons[2].rect.bottom + 40 # Abaixo do botão Vol-
        volume_rect = volume_surface.get_rect(center=(SCREEN_WIDTH // 2, volume_y))
        screen.blit(volume_surface, volume_rect)

# Inicia o jogo
if __name__ == "__main__":
    try:
        game = Game()
        game.run()
    except Exception as e:
        print(f"Erro fatal: {e}")
        traceback.print_exc()
        pygame.quit()
        sys.exit(1)