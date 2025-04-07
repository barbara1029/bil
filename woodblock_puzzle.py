#!/usr/bin/env python3

"""
Woodblock Puzzle Game - Versão Melhorada
---------------------------------------------------
Esta versão contém melhorias solicitadas:
1. Novas heurísticas: estabilidade dinâmica e cascata
2. Melhor eficiência na jogabilidade humana
3. Fundo amadeirado claro
4. Janela redimensionada com elementos centralizados
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

# Inicialização do Pygame
pygame.init()
pygame.mixer.init()

# Configurações de áudio
MUSIC_ENABLED = True
MUSIC_VOLUME = 0.5  # 50% do volume máximo

# Música codificada em base64 (uma melodia simples gerada proceduralmente)
# Esta é uma música de 8-bit simples codificada diretamente no código
BACKGROUND_MUSIC = """
UklGRiQFAABXQVZFZm10IBAAAAABAAEARKwAAIhYAQACABAAZGF0YQAFAACBgIF/gn6Df4GBgYF/gn6Df4GBgYF/
gn6Df4GBgYF/gn6Df4GBgYF/gn6Df4GBgYF/gn6Df4GBgYF/gn6Df4GBgYF/gn6Df4GBgYF/gn6Df4GBgYF/gn6D
f4GBgYF/gn6Df4GBgYF/gn6Df4GBgYF/gn6Df4GBgYF/gn6Df4GBgYF/gn6Df4GBgYF/gn6Df4GBgYF/gn6Df4GB
gYF/gn6Df4GBgYF/gn6Df4GBgYF/gn6Df4GBgYF/gn6Df4GBgYF/gn6Df4GBgYF/gn6Df4GBgYF/gn6Df4GBgYF/
gn6Df4GBgYF/gn6Df4GBgYF/gn6Df4GBgYF/gn6Df4GBgYF/gn6Df4GBgYF/gn6Df4GBgYF/gn6Df4GBgYF/gn6D
f4GBgYF/gn6Df4GBgYF/gn6Df4GBgYF/gn6Df4GBgYF/gn6Df4GBgYF/gn6Df4GBgYF/gn6Df4GBgYF/gn6Df4GB
gYF/gn6Df4GBgYF/gn6Df4GBgYF/gn6Df4GBgYF/gn6Df4GBgYF/gn6Df4GBgYF/gn6Df4GBgYF/gn6Df4GBgYF/
gn6Df4GBgYF/gn6Df4GBgYF/gn6Df4GBgYF/gn6Df4GBgYF/gn6Df4GBgYF/gn6Df4GBgYF/gn6Df4GBgYF/gn6D
f4GBgYF/gn6Df4GBgYF/gn6Df4GBgYF/gn6Df4GBgYF/gn6Df4GBgYF/gn6Df4GBgYF/gn6Df4GBgYF/gn6Df4GB
gYF/gn6Df4GBgYF/gn6Df4GBgYF/gn6Df4GBgYF/gn6Df4GBgYF/gn6Df4GBgYF/gn6Df4GBgYF/gn6Df4GBgYF/
gn6Df4GBgYF/gn6Df4GBgYF/gn6Df4GBgYF/gn6Df4GBgYF/gn6Df4GBgYF/gn6Df4GBgYF/gn6Df4GBgYF/gn6D
f4GBgYF/gn6Df4GBgYF/gn6Df4GBgYF/gn6Df4GBgYF/gn6Df4GBgYF/gn6Df4GBgYF/gn6Df4GBgYF/gn6Df4GB
gYF/gn6Df4GBgYF/gn6Df4GBgYF/gn6Df4GBgYF/gn6Df4GBgYF/gn6Df4GBgYF/gn6Df4GBgYF/gn6Df4GBgYF/
gn6Df4GBgYF/gn6Df4GBgYF/gn6Df4GBgYF/gn6Df4GBgYF/gn6Df4GBgYF/gn6Df4GBgYF/gn6Df4GBgYF/gn6D
f4GBgYF/gn6Df4GBgYF/gn6Df4GBgYF/gn6Df4GBgYF/gn6Df4GBgYF/gn6Df4GBgYF/gn6Df4GBgYF/gn6Df4GB
gYF/gn6Df4GBgYF/gn6Df4GBgYF/gn6Df4GBgYF/gn6Df4GBgYF/gn6Df4GBgYF/gn6Df4GBgYF/gn6Df4GBgYF/
gn6Df4GBgYF/gn6Df4GBgYF/gn6Df4GBgYF/gn6Df4GBgYF/gn6Df4GBgYF/gn6Df4GBgYF/gn6Df4GBgYF/gn6D
f4GBgYF/gn6Df4GBgYF/gn6Df4GBgYF/gn6Df4GBgYF/gn6Df4GBgYF/gn6Df4GBgYF/gn6Df4GBgYF/gn6Df4GB
gYF/gn6Df4GBgYF/gn6Df4GBgYF/gn6Df4GBgYF/gn6Df4GBgYF/gn6Df4GBgYF/gn6Df4GBgYF/gn6Df4GBgYF/
gn6Df4GBgYF/gn6Df4GBgYF/gn6Df4GBgYF/gn6Df4GBgYF/gn6Df4GBgYF/gn6Df4GBgYF/gn6Df4GBgYF/gn6D
f4GBgYF/gn6Df4GBgYF/gn6Df4GBgYF/gn6Df4GBgYF/gn6Df4GBgYF/gn6Df4GBgYF/gn6Df4GBgYF/gn6Df4GB
"""

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
        except Exception as e:
            print(f"Erro ao carregar música: {e}")
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
        # Se a música foi ativada, tocar
        pygame.mixer.music.play(-1)
    else:
        # Se a música foi desativada, pausar
        pygame.mixer.music.pause()
# Constantes - Aumentando o tamanho da janela
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

# Fontes
title_font = pygame.font.SysFont("Arial", 48, bold=True)
menu_font = pygame.font.SysFont("Arial", 36)
button_font = pygame.font.SysFont("Arial", 24)
game_font = pygame.font.SysFont("Arial", 20)

#######################
# Classe Piece (Peça) #
#######################

class Piece:

    def __init__(self, shape=None, color=None):
        """
        Inicializa uma peça com uma forma e cor específicas.
        
        Args:
            shape: Matriz numpy representando a forma da peça (1 = bloco, 0 = vazio)
            color: Cor da peça (RGB)
        """
        if shape is None:
            # Gerar uma forma aleatória se nenhuma for fornecida
            self.shape = self.generate_random_shape()
        else:
            self.shape = shape
            
        if color is None:
            # Escolher uma cor aleatória se nenhuma for fornecida
            self.color = random.choice(PIECE_COLORS)
        else:
            self.color = color
            
        self.rows, self.cols = self.shape.shape
        
    def copy(self):
        """
        Cria uma cópia profunda da peça.
        
        Returns:
            Nova instância de Piece com os mesmos atributos
        """
        return Piece(shape=self.shape.copy(), color=self.color)
        
    def generate_random_shape(self):
        """
        Gera uma forma aleatória para a peça.
        
        Returns:
            Matriz numpy representando a forma da peça
        """
        # Lista de formas possíveis (1 = bloco, 0 = vazio)
        shapes = [
            # Formas de 1 bloco
            np.array([[1]]),
            
            # Formas de 2 blocos
            np.array([[1, 1]]),
            np.array([[1], [1]]),
            
            # Formas de 3 blocos
            np.array([[1, 1, 1]]),
            np.array([[1], [1], [1]]),
            np.array([[1, 1], [1, 0]]),
            np.array([[1, 1], [0, 1]]),
            np.array([[1, 0], [1, 1]]),
            np.array([[0, 1], [1, 1]]),
            np.array([[1, 1, 0], [0, 1, 0]]),
            np.array([[0, 1, 0], [1, 1, 0]]),
            
            # Formas de 4 blocos
            np.array([[1, 1, 1, 1]]),
            np.array([[1], [1], [1], [1]]),
            np.array([[1, 1], [1, 1]]),
            np.array([[1, 1, 0], [0, 1, 1]]),
            np.array([[0, 1, 1], [1, 1, 0]]),
            np.array([[1, 0, 0], [1, 1, 1]]),
            np.array([[0, 0, 1], [1, 1, 1]]),
            np.array([[1, 1, 1], [1, 0, 0]]),
            np.array([[1, 1, 1], [0, 0, 1]]),
            np.array([[1, 0], [1, 0], [1, 1]]),
            np.array([[0, 1], [0, 1], [1, 1]]),
            np.array([[1, 1], [1, 0], [1, 0]]),
            np.array([[1, 1], [0, 1], [0, 1]])
        ]
        
        # Escolher uma forma aleatória
        return random.choice(shapes)
    
    # Método de rotação removido conforme solicitado
    
    def flip_horizontal(self):
        """
        Inverte a peça horizontalmente.
        """
        self.shape = np.fliplr(self.shape)
        
    def flip_vertical(self):
        """
        Inverte a peça verticalmente.
        """
        self.shape = np.flipud(self.shape)
        
    def draw(self, surface, x, y, cell_size):
        """
        Desenha a peça na superfície.
        
        Args:
            surface: Superfície do pygame para desenhar
            x, y: Coordenadas do canto superior esquerdo
            cell_size: Tamanho de cada célula da peça
        """
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
        """
        Inicializa o tabuleiro do jogo.
        
        Args:
            size: Tamanho do tabuleiro (5 para 5x5, 10 para 10x10)
            difficulty: Dificuldade do jogo ("easy", "medium", "hard")
        """
        self.size = size
        self.difficulty = difficulty
        self.grid = np.zeros((size, size), dtype=int)
        self.colors = np.zeros((size, size, 3), dtype=int)
        self.score = 0
        
        # Configurações baseadas na dificuldade
        if difficulty == "easy":
            self.num_initial_blocks = int(size * size * 0.1)  # 10% do tabuleiro preenchido
        elif difficulty == "medium":
            self.num_initial_blocks = int(size * size * 0.2)  # 20% do tabuleiro preenchido
        else:  # hard
            self.num_initial_blocks = int(size * size * 0.3)  # 30% do tabuleiro preenchido
            
        # Preencher o tabuleiro com blocos iniciais
        self.initialize_board()
        
        # Gerar as peças iniciais
        self.available_pieces = [Piece() for _ in range(3)]
        
    def copy(self):
        """
        Cria uma cópia profunda do tabuleiro.
        
        Returns:
            Nova instância de Board com os mesmos atributos
        """
        new_board = Board(self.size, self.difficulty)
        new_board.grid = self.grid.copy()
        new_board.colors = self.colors.copy()
        new_board.score = self.score
        return new_board
        
    def initialize_board(self):
        """
        Inicializa o tabuleiro com blocos aleatórios.
        """
        # Limpar o tabuleiro
        self.grid = np.zeros((self.size, self.size), dtype=int)
        self.colors = np.zeros((self.size, self.size, 3), dtype=int)
        
        # Adicionar blocos aleatórios
        blocks_added = 0
        while blocks_added < self.num_initial_blocks:
            row = random.randint(0, self.size - 1)
            col = random.randint(0, self.size - 1)
            
            if self.grid[row, col] == 0:
                self.grid[row, col] = 1
                color = random.choice(PIECE_COLORS)
                self.colors[row, col] = color
                blocks_added += 1
                
    def can_place_piece(self, piece, row, col):
        """
        Verifica se uma peça pode ser colocada em uma posição específica.
        
        Args:
            piece: Objeto Piece a ser colocado
            row, col: Coordenadas da célula superior esquerda
            
        Returns:
            True se a peça pode ser colocada, False caso contrário
        """
        # Verificar se a peça está dentro dos limites do tabuleiro
        if row < 0 or col < 0 or row + piece.rows > self.size or col + piece.cols > self.size:
            return False
            
        # Verificar se a peça não sobrepõe blocos existentes
        for r in range(piece.rows):
            for c in range(piece.cols):
                if piece.shape[r, c] == 1 and self.grid[row + r, col + c] == 1:
                    return False
                    
        return True
        
    def place_piece(self, piece, row, col):
        """
        Coloca uma peça no tabuleiro.
        
        Args:
            piece: Objeto Piece a ser colocado
            row, col: Coordenadas da célula superior esquerda
            
        Returns:
            True se a peça foi colocada com sucesso, False caso contrário
        """
        if not self.can_place_piece(piece, row, col):
            return False
            
        # Colocar a peça no tabuleiro
        for r in range(piece.rows):
            for c in range(piece.cols):
                if piece.shape[r, c] == 1:
                    self.grid[row + r, col + c] = 1
                    self.colors[row + r, col + c] = piece.color
                    
        # Verificar e eliminar linhas e colunas completas
        rows_cleared, cols_cleared = self.clear_lines()
        
        # Atualizar a pontuação
        if rows_cleared > 0 or cols_cleared > 0:
            self.update_score(rows_cleared, cols_cleared)
            
        return True
        
    def clear_lines(self):
        """
        Verifica e elimina linhas e colunas completas.
        
        Returns:
            Tupla (rows_cleared, cols_cleared) com o número de linhas e colunas eliminadas
        """
        rows_to_clear = []
        cols_to_clear = []
        
        # Verificar linhas completas
        for row in range(self.size):
            if np.all(self.grid[row, :] == 1):
                rows_to_clear.append(row)
                
        # Verificar colunas completas
        for col in range(self.size):
            if np.all(self.grid[:, col] == 1):
                cols_to_clear.append(col)
                
        # Limpar linhas
        for row in rows_to_clear:
            self.grid[row, :] = 0
            self.colors[row, :] = 0
            
        # Limpar colunas
        for col in cols_to_clear:
            self.grid[:, col] = 0
            self.colors[:, col] = 0
            
        return len(rows_to_clear), len(cols_to_clear)
        
    def update_score(self, rows_cleared, cols_cleared):
        """
        Atualiza a pontuação com base nas linhas e colunas eliminadas.
        
        Args:
            rows_cleared: Número de linhas eliminadas
            cols_cleared: Número de colunas eliminadas
        """
        # Pontuação base por linha/coluna
        base_points = 100
        
        # Bônus por tamanho do tabuleiro
        size_multiplier = 1 if self.size == 5 else 2
        
        # Bônus por dificuldade
        difficulty_multiplier = 1
        if self.difficulty == "medium":
            difficulty_multiplier = 1.5
        elif self.difficulty == "hard":
            difficulty_multiplier = 2
            
        # Bônus por eliminar múltiplas linhas/colunas de uma vez
        combo_multiplier = 1 + 0.5 * (rows_cleared + cols_cleared - 1)
        
        # Calcular pontuação total
        points = int(base_points * (rows_cleared + cols_cleared) * size_multiplier * difficulty_multiplier * combo_multiplier)
        
        # Adicionar à pontuação atual
        self.score += points
        
    def generate_new_piece(self):
        """
        Gera uma nova peça aleatória.
        
        Returns:
            Objeto Piece gerado
        """
        return Piece()
        
    def is_game_over(self):
        """
        Verifica se o jogo acabou (nenhuma peça disponível pode ser colocada).
        
        Returns:
            True se o jogo acabou, False caso contrário
        """
        # Verificar cada peça disponível
        for piece in self.available_pieces:
            # Tentar todas as posições possíveis
            for row in range(self.size - piece.rows + 1):
                for col in range(self.size - piece.cols + 1):
                    if self.can_place_piece(piece, row, col):
                        return False
            
        # Se chegou aqui, nenhuma peça pode ser colocada
        return True
        
    def draw(self, surface, x, y, cell_size):
        """
        Desenha o tabuleiro na superfície.
        
        Args:
            surface: Superfície do pygame para desenhar
            x, y: Coordenadas do canto superior esquerdo
            cell_size: Tamanho de cada célula do tabuleiro
        """
        # Desenhar o fundo do tabuleiro
        board_rect = pygame.Rect(x, y, self.size * cell_size, self.size * cell_size)
        pygame.draw.rect(surface, GRAY, board_rect)
        pygame.draw.rect(surface, BLACK, board_rect, 2)
        
        # Desenhar as células
        for row in range(self.size):
            for col in range(self.size):
                cell_rect = pygame.Rect(
                    x + col * cell_size,
                    y + row * cell_size,
                    cell_size,
                    cell_size
                )
                
                if self.grid[row, col] == 1:
                    # Célula ocupada
                    color = tuple(self.colors[row, col])
                    pygame.draw.rect(surface, color, cell_rect)
                else:
                    # Célula vazia
                    pygame.draw.rect(surface, WHITE, cell_rect)
                    
                # Desenhar borda da célula
                pygame.draw.rect(surface, BLACK, cell_rect, 1)
                
    def draw_available_pieces(self, surface, x, y, cell_size):
        """
        Desenha as peças disponíveis na superfície.
        
        Args:
            surface: Superfície do pygame para desenhar
            x, y: Coordenadas do canto superior esquerdo
            cell_size: Tamanho de cada célula das peças
        """
        spacing = 20  # Espaçamento entre as peças
        
        for i, piece in enumerate(self.available_pieces):
            piece_x = x + i * (4 * cell_size + spacing)
            piece_y = y
            
            # Desenhar fundo da área da peça
            bg_width = max(4, piece.cols) * cell_size
            bg_height = max(4, piece.rows) * cell_size
            bg_rect = pygame.Rect(piece_x, piece_y, bg_width, bg_height)
            pygame.draw.rect(surface, GRAY, bg_rect)
            pygame.draw.rect(surface, BLACK, bg_rect, 1)
            
            # Centralizar a peça na área
            offset_x = (bg_width - piece.cols * cell_size) // 2
            offset_y = (bg_height - piece.rows * cell_size) // 2
            
            # Desenhar a peça
            piece.draw(surface, piece_x + offset_x, piece_y + offset_y, cell_size)

#######################
# Classes para Algoritmos de IA #
#######################

class GameState:
    """
    Representa um estado do jogo para os algoritmos de busca.
    """
    def __init__(self, board, available_pieces, score=0, parent=None, action=None, depth=0):
        self.board = board  # Cópia do tabuleiro
        self.available_pieces = available_pieces  # Lista de peças disponíveis
        self.score = score  # Pontuação atual
        self.parent = parent  # Estado pai (para reconstruir o caminho)
        self.action = action  # Ação que levou a este estado
        self.depth = depth  # Profundidade na árvore de busca
        
    def __lt__(self, other):
        """
        Comparação para uso em filas de prioridade.
        """
        return self.score > other.score  # Priorizar estados com maior pontuação
        
    def get_possible_actions(self):
        """
        Retorna todas as ações possíveis a partir deste estado.
        Cada ação é uma tupla (piece_index, rotation, row, col).
        Nota: rotation sempre será 0 já que a rotação foi removida.
        """
        actions = []
        
        for piece_index, piece in enumerate(self.available_pieces):
            # Tentar todas as posições no tabuleiro
            for row in range(self.board.size - piece.rows + 1):
                for col in range(self.board.size - piece.cols + 1):
                    if self.board.can_place_piece(piece, row, col):
                        # rotation é sempre 0 já que não há rotação
                        actions.append((piece_index, 0, row, col))
            
        return actions
        
    def apply_action(self, action):
        """
        Aplica uma ação e retorna o novo estado resultante.
        """
        piece_index, rotation, row, col = action
        
        # Criar cópias profundas do tabuleiro e peças
        new_board = self.board.copy()
        new_pieces = [piece.copy() for piece in self.available_pieces]
        
        # Colocar a peça no tabuleiro (sem rotação)
        piece = new_pieces[piece_index]
        new_board.place_piece(piece, row, col)
        
        # Gerar nova peça para substituir a usada
        new_pieces[piece_index] = new_board.generate_new_piece()
        
        # Criar e retornar o novo estado
        return GameState(
            board=new_board,
            available_pieces=new_pieces,
            score=new_board.score,
            parent=self,
            action=action,
            depth=self.depth + 1
        )
        
    def is_terminal(self):
        """
        Verifica se este é um estado terminal (fim de jogo).
        """
        return self.board.is_game_over()

class AStarSearch:
    """
    Implementação do algoritmo A* para resolver o jogo Woodblock.
    """
    def __init__(self):
        self.nodes_explored = 0
        self.max_depth = 0
        
    def heuristic(self, state):
        """
        Função heurística para estimar o valor de um estado.
        Combina pontuação atual com potencial futuro.
        """
        # Pontuação atual
        score_value = state.score
        
        # Potencial de completar linhas/colunas
        board = state.board
        potential = 0
        
        # Contar células preenchidas em cada linha e coluna
        for i in range(board.size):
            row_filled = np.sum(board.grid[i, :])
            col_filled = np.sum(board.grid[:, i])
            
            # Quanto mais próximo de completar, maior o potencial
            row_potential = (row_filled / board.size) ** 2 * 100
            col_potential = (col_filled / board.size) ** 2 * 100
            
            potential += row_potential + col_potential
            
        # Espaços vazios disponíveis (quanto mais, melhor)
        empty_spaces = np.sum(board.grid == 0)
        space_value = empty_spaces * 5
        
        # Combinar os fatores
        return score_value + potential + space_value
        
    def search(self, initial_state, max_iterations=1000):
        """
        Executa a busca A* a partir do estado inicial.
        
        Args:
            initial_state: Estado inicial do jogo
            max_iterations: Número máximo de iterações
            
        Returns:
            Melhor sequência de ações encontrada
        """
        self.nodes_explored = 0
        self.max_depth = 0
        
        # Fila de prioridade para os estados a serem explorados
        open_set = []
        
        # Conjunto de estados já visitados (para evitar ciclos)
        closed_set = set()
        
        # Adicionar o estado inicial à fila
        f_value = self.heuristic(initial_state)
        heapq.heappush(open_set, (f_value, initial_state))
        
        best_state = initial_state
        best_score = initial_state.score
        
        # Loop principal
        iterations = 0
        while open_set and iterations < max_iterations:
            iterations += 1
            
            # Obter o estado com menor valor f
            _, current_state = heapq.heappop(open_set)
            self.nodes_explored += 1
            
            # Atualizar profundidade máxima
            self.max_depth = max(self.max_depth, current_state.depth)
            
            # Verificar se é um estado terminal ou melhor que o atual melhor
            if current_state.score > best_score:
                best_state = current_state
                best_score = current_state.score
                
            if current_state.is_terminal():
                best_state = current_state
                break
                
            # Gerar todos os estados sucessores
            for action in current_state.get_possible_actions():
                next_state = current_state.apply_action(action)
                
                # Calcular o valor f para o novo estado
                f_value = -self.heuristic(next_state)  # Negativo porque heapq é min-heap
                
                # Adicionar à fila de prioridade
                heapq.heappush(open_set, (f_value, next_state))
                
        # Reconstruir o caminho a partir do melhor estado encontrado
        path = []
        state = best_state
        while state.parent is not None:
            path.append(state.action)
            state = state.parent
            
        # Inverter o caminho para obter a sequência correta
        path.reverse()
        
        return path, best_state.score, self.nodes_explored, self.max_depth

class GreedySearch:
    """
    Implementação do algoritmo Greedy Search para resolver o jogo Woodblock.
    """
    def __init__(self):
        self.nodes_explored = 0
        self.max_depth = 0
        
    def evaluate(self, state, action):
        """
        Avalia o valor de uma ação a partir de um estado.
        """
        # Simular a ação para ver o resultado
        next_state = state.apply_action(action)
        
        # Pontuação direta
        score_gain = next_state.score - state.score
        
        # Potencial de completar linhas/colunas
        board = next_state.board
        potential = 0
        
        # Contar células preenchidas em cada linha e coluna
        for i in range(board.size):
            row_filled = np.sum(board.grid[i, :])
            col_filled = np.sum(board.grid[:, i])
            
            # Quanto mais próximo de completar, maior o potencial
            row_potential = (row_filled / board.size) ** 2 * 50
            col_potential = (col_filled / board.size) ** 2 * 50
            
            potential += row_potential + col_potential
            
        # Valor total da ação
        return score_gain + potential
        
    def search(self, initial_state, max_depth=100):
        """
        Executa a busca gulosa a partir do estado inicial.
        
        Args:
            initial_state: Estado inicial do jogo
            max_depth: Profundidade máxima de busca
            
        Returns:
            Sequência de ações encontrada
        """
        self.nodes_explored = 0
        self.max_depth = 0
        
        current_state = initial_state
        path = []
        
        # Loop principal
        while len(path) < max_depth and not current_state.is_terminal():
            self.nodes_explored += 1
            self.max_depth = max(self.max_depth, len(path))
            
            # Obter todas as ações possíveis
            actions = current_state.get_possible_actions()
            
            if not actions:
                break
                
            # Avaliar cada ação e escolher a melhor
            best_action = None
            best_value = float('-inf')
            
            for action in actions:
                value = self.evaluate(current_state, action)
                
                if value > best_value:
                    best_value = value
                    best_action = action
                    
            # Aplicar a melhor ação
            path.append(best_action)
            current_state = current_state.apply_action(best_action)
            
        return path, current_state.score, self.nodes_explored, self.max_depth

class BFSSearch:
    """
    Implementação do algoritmo Breadth-First Search para resolver o jogo Woodblock.
    """
    def __init__(self):
        self.nodes_explored = 0
        self.max_depth = 0
        
    def search(self, initial_state, max_iterations=1000):
        """
        Executa a busca em largura a partir do estado inicial.
        
        Args:
            initial_state: Estado inicial do jogo
            max_iterations: Número máximo de iterações
            
        Returns:
            Sequência de ações encontrada
        """
        self.nodes_explored = 0
        self.max_depth = 0
        
        # Fila para BFS
        queue = []
        queue.append(initial_state)
        
        # Conjunto de estados visitados
        visited = set()
        
        best_state = initial_state
        best_score = initial_state.score
        
        # Loop principal
        iterations = 0
        while queue and iterations < max_iterations:
            iterations += 1
            
            # Obter o próximo estado da fila
            current_state = queue.pop(0)
            self.nodes_explored += 1
            
            # Atualizar profundidade máxima
            self.max_depth = max(self.max_depth, current_state.depth)
            
            # Verificar se é um estado terminal ou melhor que o atual melhor
            if current_state.score > best_score:
                best_state = current_state
                best_score = current_state.score
                
            if current_state.is_terminal():
                best_state = current_state
                break
                
            # Gerar todos os estados sucessores
            for action in current_state.get_possible_actions():
                next_state = current_state.apply_action(action)
                
                # Adicionar à fila se não foi visitado
                state_hash = hash(str(next_state.board.grid))
                if state_hash not in visited:
                    visited.add(state_hash)
                    queue.append(next_state)
                    
        # Reconstruir o caminho a partir do melhor estado encontrado
        path = []
        state = best_state
        while state.parent is not None:
            path.append(state.action)
            state = state.parent
            
        # Inverter o caminho para obter a sequência correta
        path.reverse()
        
        return path, best_state.score, self.nodes_explored, self.max_depth

class DFSSearch:
    """
    Implementação do algoritmo Depth-First Search para resolver o jogo Woodblock.
    """
    def __init__(self):
        self.nodes_explored = 0
        self.max_depth = 0
        
    def search(self, initial_state, max_depth=20):
        """
        Executa a busca em profundidade a partir do estado inicial.
        
        Args:
            initial_state: Estado inicial do jogo
            max_depth: Profundidade máxima de busca
            
        Returns:
            Sequência de ações encontrada
        """
        self.nodes_explored = 0
        self.max_depth = 0
        
        # Pilha para DFS
        stack = []
        stack.append(initial_state)
        
        # Conjunto de estados visitados
        visited = set()
        
        best_state = initial_state
        best_score = initial_state.score
        
        # Loop principal
        while stack:
            # Obter o próximo estado da pilha
            current_state = stack.pop()
            self.nodes_explored += 1
            
            # Atualizar profundidade máxima
            self.max_depth = max(self.max_depth, current_state.depth)
            
            # Verificar se é um estado terminal ou melhor que o atual melhor
            if current_state.score > best_score:
                best_state = current_state
                best_score = current_state.score
                
            if current_state.is_terminal():
                best_state = current_state
                break
                
            # Verificar se atingiu a profundidade máxima
            if current_state.depth >= max_depth:
                continue
                
            # Gerar todos os estados sucessores
            for action in current_state.get_possible_actions():
                next_state = current_state.apply_action(action)
                
                # Adicionar à pilha se não foi visitado
                state_hash = hash(str(next_state.board.grid))
                if state_hash not in visited:
                    visited.add(state_hash)
                    stack.append(next_state)
                    
        # Reconstruir o caminho a partir do melhor estado encontrado
        path = []
        state = best_state
        while state.parent is not None:
            path.append(state.action)
            state = state.parent
            
        # Inverter o caminho para obter a sequência correta
        path.reverse()
        
        return path, best_state.score, self.nodes_explored, self.max_depth

#######################
# Implementação da heurística de estabilidade dinâmica #
#######################

class DynamicStabilitySearch:
    """
    Implementação do algoritmo de busca com heurística de estabilidade dinâmica.
    """
    def __init__(self):
        self.nodes_explored = 0
        self.max_depth = 0
        
    def evaluate_stability(self, board):
        """
        Avalia a estabilidade do tabuleiro atual.
        
        Args:
            board: Objeto Board a ser avaliado
            
        Returns:
            Valor numérico representando a estabilidade
        """
        stability_score = 0
        grid = board.grid
        size = board.size
        
        # 1. Avaliar contato entre blocos (mais contato = mais estável)
        for row in range(size):
            for col in range(size):
                if grid[row, col] == 1:
                    # Contar vizinhos (blocos adjacentes)
                    neighbors = 0
                    
                    # Verificar os quatro vizinhos (cima, baixo, esquerda, direita)
                    if row > 0 and grid[row-1, col] == 1:
                        neighbors += 1
                    if row < size-1 and grid[row+1, col] == 1:
                        neighbors += 1
                    if col > 0 and grid[row, col-1] == 1:
                        neighbors += 1
                    if col < size-1 and grid[row, col+1] == 1:
                        neighbors += 1
                    
                    # Blocos com mais vizinhos são mais estáveis
                    stability_score += neighbors * 5
        
        # 2. Avaliar distribuição dos blocos (evitar concentração em uma área)
        # Dividir o tabuleiro em quadrantes e calcular a variância da ocupação
        quadrant_size = max(1, size // 2)  # Garantir que quadrant_size seja pelo menos 1
        quadrant_counts = [0, 0, 0, 0]  # Contagem de blocos em cada quadrante
        
        # Quadrante superior esquerdo
        for r in range(quadrant_size):
            for c in range(quadrant_size):
                if r < size and c < size and grid[r, c] == 1:
                    quadrant_counts[0] += 1
        
        # Quadrante superior direito
        for r in range(quadrant_size):
            for c in range(quadrant_size, size):
                if r < size and c < size and grid[r, c] == 1:
                    quadrant_counts[1] += 1
        
        # Quadrante inferior esquerdo
        for r in range(quadrant_size, size):
            for c in range(quadrant_size):
                if r < size and c < size and grid[r, c] == 1:
                    quadrant_counts[2] += 1
        
        # Quadrante inferior direito
        for r in range(quadrant_size, size):
            for c in range(quadrant_size, size):
                if r < size and c < size and grid[r, c] == 1:
                    quadrant_counts[3] += 1
        
        # Calcular a média de blocos por quadrante
        avg_blocks = sum(quadrant_counts) / 4.0
        
        # Calcular a variância (quanto menor, mais equilibrado)
        variance = sum((count - avg_blocks) ** 2 for count in quadrant_counts) / 4.0
        
        # Penalizar alta variância (distribuição desequilibrada)
        stability_score -= variance * 2
        
        return stability_score
    
    def evaluate(self, state, action):
        """
        Avalia o valor de uma ação a partir de um estado.
        
        Args:
            state: Estado atual do jogo
            action: Ação a ser avaliada
            
        Returns:
            Valor numérico representando a qualidade da ação
        """
        try:
            # Simular a ação para ver o resultado
            next_state = state.apply_action(action)
            
            # Pontuação direta (ganho de pontos)
            score_gain = next_state.score - state.score
            
            # Estabilidade do tabuleiro após a ação
            stability = self.evaluate_stability(next_state.board)
            
            # Potencial de completar linhas/colunas
            board = next_state.board
            potential = 0
            
            # Contar células preenchidas em cada linha e coluna
            for i in range(board.size):
                row_filled = sum(board.grid[i, :])
                col_filled = sum(board.grid[:, i])
                
                # Quanto mais próximo de completar, maior o potencial
                # Função quadrática para dar mais peso quando está próximo de completar
                row_potential = (row_filled / board.size) ** 2 * 100
                col_potential = (col_filled / board.size) ** 2 * 100
                
                potential += row_potential + col_potential
            
            # Espaços vazios disponíveis (quanto mais, melhor)
            empty_spaces = np.sum(board.grid == 0)
            space_value = empty_spaces * 3
            
            # Valor total da ação (combinação ponderada dos fatores)
            return score_gain * 2 + stability * 1.5 + potential + space_value
        except Exception as e:
            print(f"Erro na avaliação da estabilidade dinâmica: {e}")
            return float('-inf')  # Retornar um valor muito baixo em caso de erro
    
    def search(self, initial_state, max_depth=20):
        """
        Executa a busca com heurística de estabilidade dinâmica a partir do estado inicial.
        
        Args:
            initial_state: Estado inicial do jogo
            max_depth: Profundidade máxima de busca
            
        Returns:
            Sequência de ações encontrada
        """
        try:
            self.nodes_explored = 0
            self.max_depth = 0
            
            current_state = initial_state
            path = []
            
            # Loop principal
            while len(path) < max_depth and not current_state.is_terminal():
                self.nodes_explored += 1
                self.max_depth = max(self.max_depth, len(path))
                
                # Obter todas as ações possíveis
                actions = current_state.get_possible_actions()
                
                if not actions:
                    break
                    
                # Avaliar cada ação e escolher a melhor
                best_action = None
                best_value = float('-inf')
                
                for action in actions:
                    value = self.evaluate(current_state, action)
                    
                    if value > best_value:
                        best_value = value
                        best_action = action
                        
                # Aplicar a melhor ação
                if best_action is not None:
                    path.append(best_action)
                    current_state = current_state.apply_action(best_action)
                else:
                    break  # Se não encontrou uma ação válida, encerrar a busca
                
            return path, current_state.score, self.nodes_explored, self.max_depth
        except Exception as e:
            print(f"Erro na busca de estabilidade dinâmica: {e}")
            traceback.print_exc()
            return [], 0, 0, 0  # Retornar valores vazios em caso de erro

#######################
# Implementação da heurística de cascata #
#######################

class CascadeSearch:
    """
    Implementação do algoritmo de busca com heurística de cascata.
    """
    def __init__(self):
        self.nodes_explored = 0
        self.max_depth = 0
        
    def evaluate_cascade_potential(self, board):
        """
        Avalia o potencial de cascata do tabuleiro atual.
        
        Args:
            board: Objeto Board a ser avaliado
            
        Returns:
            Valor numérico representando o potencial de cascata
        """
        try:
            cascade_score = 0
            grid = board.grid
            size = board.size
            
            # 1. Avaliar linhas e colunas quase completas (potencial de eliminação)
            near_complete_threshold = 0.7  # Considerar quase completa se 70% preenchida
            
            for i in range(size):
                # Contar células preenchidas em cada linha e coluna
                row_filled = sum(grid[i, :])
                col_filled = sum(grid[:, i])
                
                # Calcular porcentagem de preenchimento
                row_percent = row_filled / size
                col_percent = col_filled / size
                
                # Pontuação para linhas/colunas quase completas
                if row_percent >= near_complete_threshold and row_percent < 1.0:
                    # Quanto mais próximo de completar, maior a pontuação
                    # Função exponencial para dar mais peso quando está muito próximo de completar
                    cascade_score += (row_percent ** 3) * 200
                    
                if col_percent >= near_complete_threshold and col_percent < 1.0:
                    cascade_score += (col_percent ** 3) * 200
            
            # 2. Avaliar padrões de "escada" (blocos adjacentes em diagonal)
            # Estes padrões tendem a criar oportunidades de cascata
            for row in range(size - 1):
                for col in range(size - 1):
                    # Padrão diagonal descendente (↘)
                    if grid[row, col] == 1 and grid[row+1, col+1] == 1:
                        cascade_score += 10
                    
                    # Padrão diagonal ascendente (↗)
                    if row > 0 and col < size-1 and grid[row, col+1] == 1 and grid[row-1, col] == 1:
                        cascade_score += 10
            
            # 3. Avaliar grupos de células preenchidas adjacentes
            # Grupos maiores têm maior potencial de criar cascatas
            visited = set()
            
            def count_group_size(r, c):
                if (r, c) in visited or r < 0 or c < 0 or r >= size or c >= size or grid[r, c] == 0:
                    return 0
                    
                visited.add((r, c))
                size_count = 1
                
                # Verificar células adjacentes (cima, baixo, esquerda, direita)
                size_count += count_group_size(r-1, c)
                size_count += count_group_size(r+1, c)
                size_count += count_group_size(r, c-1)
                size_count += count_group_size(r, c+1)
                
                return size_count
            
            # Encontrar e pontuar todos os grupos
            for row in range(size):
                for col in range(size):
                    if grid[row, col] == 1 and (row, col) not in visited:
                        group_size = count_group_size(row, col)
                        # Grupos maiores recebem pontuação exponencial
                        cascade_score += group_size ** 1.5
            
            return cascade_score
        except Exception as e:
            print(f"Erro na avaliação do potencial de cascata: {e}")
            return 0  # Retornar zero em caso de erro
    
    def evaluate(self, state, action):
        """
        Avalia o valor de uma ação a partir de um estado.
        
        Args:
            state: Estado atual do jogo
            action: Ação a ser avaliada
            
        Returns:
            Valor numérico representando a qualidade da ação
        """
        try:
            # Simular a ação para ver o resultado
            next_state = state.apply_action(action)
            
            # Pontuação direta (ganho de pontos)
            score_gain = next_state.score - state.score
            
            # Potencial de cascata após a ação
            cascade_potential = self.evaluate_cascade_potential(next_state.board)
            
            # Verificar se a ação resultou em eliminação de linhas/colunas
            # (isso é capturado indiretamente pelo score_gain, mas queremos dar peso extra)
            elimination_bonus = 0
            if score_gain > 0:
                elimination_bonus = score_gain * 2  # Dobrar o valor de eliminações
            
            # Espaços vazios disponíveis (quanto mais, melhor)
            board = next_state.board
            empty_spaces = np.sum(board.grid == 0)
            space_value = empty_spaces * 2
            
            # Valor total da ação (combinação ponderada dos fatores)
            return score_gain * 3 + cascade_potential * 2 + elimination_bonus + space_value
        except Exception as e:
            print(f"Erro na avaliação da cascata: {e}")
            return float('-inf')  # Retornar um valor muito baixo em caso de erro
    
    def search(self, initial_state, max_depth=20):
        """
        Executa a busca com heurística de cascata a partir do estado inicial.
        
        Args:
            initial_state: Estado inicial do jogo
            max_depth: Profundidade máxima de busca
            
        Returns:
            Sequência de ações encontrada
        """
        try:
            self.nodes_explored = 0
            self.max_depth = 0
            
            current_state = initial_state
            path = []
            
            # Loop principal
            while len(path) < max_depth and not current_state.is_terminal():
                self.nodes_explored += 1
                self.max_depth = max(self.max_depth, len(path))
                
                # Obter todas as ações possíveis
                actions = current_state.get_possible_actions()
                
                if not actions:
                    break
                    
                # Avaliar cada ação e escolher a melhor
                best_action = None
                best_value = float('-inf')
                
                for action in actions:
                    value = self.evaluate(current_state, action)
                    
                    if value > best_value:
                        best_value = value
                        best_action = action
                        
                # Aplicar a melhor ação
                if best_action is not None:
                    path.append(best_action)
                    current_state = current_state.apply_action(best_action)
                else:
                    break  # Se não encontrou uma ação válida, encerrar a busca
                
            return path, current_state.score, self.nodes_explored, self.max_depth
        except Exception as e:
            print(f"Erro na busca de cascata: {e}")
            traceback.print_exc()
            return [], 0, 0, 0  # Retornar valores vazios em caso de erro

#######################
# Classe Button (Botão) #
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
        # Desenha o botão
        pygame.draw.rect(surface, self.current_color, self.rect, border_radius=10)
        pygame.draw.rect(surface, BLACK, self.rect, 2, border_radius=10)
        
        # Renderiza o texto
        text_surface = button_font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
        
    def update(self, mouse_pos):
        # Verifica se o mouse está sobre o botão
        if self.rect.collidepoint(mouse_pos):
            self.current_color = self.hover_color
            self.is_hovered = True
        else:
            self.current_color = self.color
            self.is_hovered = False
            
    def is_clicked(self, event):
        # Verifica se o botão foi clicado
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.is_hovered
        return False

#######################
# Classe GamePlay (Modo Humano) #
#######################

class GamePlay:
    def __init__(self, board_size, difficulty, game_mode):
        self.board_size = board_size
        self.difficulty = difficulty
        self.game_mode = game_mode
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
        
        # Peça selecionada
        self.selected_piece_index = None
        self.selected_piece_offset_x = 0
        self.selected_piece_offset_y = 0
        
        # Botão de voltar ao menu
        self.back_button = Button(SCREEN_WIDTH - 120, SCREEN_HEIGHT - 60, 100, 40, "Menu")
        
        # Estado do jogo
        self.game_over = False
        
        # Área de previsão para melhorar a jogabilidade humana
        self.preview_row = None
        self.preview_col = None
        
    def handle_events(self, event):
        mouse_pos = pygame.mouse.get_pos()
        
        # Verificar clique no botão de voltar
        if self.back_button.is_clicked(event):
            self.game_over = False
            return "menu"
            
        # Verificar se o jogo acabou
        if self.game_over:
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                self.game_over = False
                return "menu"
            return None
            
        # Verificar clique nas peças disponíveis
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Verificar se clicou em alguma peça disponível
            for i, piece in enumerate(self.board.available_pieces):
                piece_x = self.pieces_x + i * (4 * self.cell_size + 20)
                piece_y = self.pieces_y
                
                # Área da peça
                bg_width = max(4, piece.cols) * self.cell_size
                bg_height = max(4, piece.rows) * self.cell_size
                
                piece_rect = pygame.Rect(piece_x, piece_y, bg_width, bg_height)
                
                if piece_rect.collidepoint(mouse_pos):
                    self.selected_piece_index = i
                    self.selected_piece_offset_x = mouse_pos[0] - piece_x
                    self.selected_piece_offset_y = mouse_pos[1] - piece_y
                    break
                    
        # Verificar soltura do mouse (colocar peça)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.selected_piece_index is not None:
            # Calcular a posição da célula no tabuleiro
            board_col = (mouse_pos[0] - self.board_x) // self.cell_size
            board_row = (mouse_pos[1] - self.board_y) // self.cell_size
            
            # Verificar se a posição está dentro do tabuleiro
            if (0 <= board_row < self.board_size and 
                0 <= board_col < self.board_size):
                
                # Tentar colocar a peça
                piece = self.board.available_pieces[self.selected_piece_index]
                if self.board.place_piece(piece, board_row, board_col):
                    # Peça colocada com sucesso, gerar nova peça
                    self.board.available_pieces[self.selected_piece_index] = self.board.generate_new_piece()
                    
                    # Verificar se o jogo acabou
                    if self.board.is_game_over():
                        self.game_over = True
            
            # Resetar a seleção
            self.selected_piece_index = None
            self.preview_row = None
            self.preview_col = None
            
        # Atualizar a previsão de posicionamento
        elif event.type == pygame.MOUSEMOTION and self.selected_piece_index is not None:
            # Calcular a posição da célula no tabuleiro
            board_col = (mouse_pos[0] - self.board_x) // self.cell_size
            board_row = (mouse_pos[1] - self.board_y) // self.cell_size
            
            # Verificar se a posição está dentro do tabuleiro
            if (0 <= board_row < self.board_size and 
                0 <= board_col < self.board_size):
                self.preview_row = board_row
                self.preview_col = board_col
            else:
                self.preview_row = None
                self.preview_col = None
            
        return None
        
    def update(self, mouse_pos):
        # Atualizar botões
        self.back_button.update(mouse_pos)
        
    def draw(self, surface):
        # Desenhar o fundo amadeirado
        draw_wooden_background(surface)
        
        # Desenhar o tabuleiro
        self.board.draw(surface, self.board_x, self.board_y, self.cell_size)
        
        # Desenhar as peças disponíveis
        self.board.draw_available_pieces(surface, self.pieces_x, self.pieces_y, self.cell_size)
        
        # Desenhar a previsão de posicionamento
        if self.selected_piece_index is not None and self.preview_row is not None and self.preview_col is not None:
            piece = self.board.available_pieces[self.selected_piece_index]
            can_place = self.board.can_place_piece(piece, self.preview_row, self.preview_col)
            
            # Desenhar a previsão com transparência
            preview_surface = pygame.Surface((piece.cols * self.cell_size, piece.rows * self.cell_size), pygame.SRCALPHA)
            for row in range(piece.rows):
                for col in range(piece.cols):
                    if piece.shape[row, col] == 1:
                        rect = pygame.Rect(
                            col * self.cell_size,
                            row * self.cell_size,
                            self.cell_size,
                            self.cell_size
                        )
                        # Verde transparente se pode colocar, vermelho transparente se não
                        color = (*piece.color, 128) if can_place else (255, 0, 0, 128)
                        pygame.draw.rect(preview_surface, color, rect)
                        pygame.draw.rect(preview_surface, (0, 0, 0, 128), rect, 1)
            
            # Desenhar a previsão no tabuleiro
            surface.blit(preview_surface, (self.board_x + self.preview_col * self.cell_size, 
                                          self.board_y + self.preview_row * self.cell_size))
        
        # Desenhar a peça selecionada (seguindo o mouse)
        if self.selected_piece_index is not None:
            mouse_pos = pygame.mouse.get_pos()
            piece = self.board.available_pieces[self.selected_piece_index]
            piece_x = mouse_pos[0] - self.selected_piece_offset_x
            piece_y = mouse_pos[1] - self.selected_piece_offset_y
            piece.draw(surface, piece_x, piece_y, self.cell_size)
            
        # Desenhar botões
        self.back_button.draw(surface)
        
        # Desenhar pontuação
        score_text = game_font.render(f"Pontuação: {self.board.score}", True, BLACK)
        surface.blit(score_text, (20, 20))
        
        # Desenhar informações do jogo
        info_text = game_font.render(
            f"Tabuleiro: {self.board_size}x{self.board_size} | Dificuldade: {self.difficulty}",
            True, BLACK
        )
        surface.blit(info_text, (20, 50))
        
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
            
            # Instrução para continuar
            continue_text = button_font.render("Clique para continuar", True, WHITE)
            continue_rect = continue_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))
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
        button_width = 300
        button_height = 50
        button_x = SCREEN_WIDTH // 2 - button_width // 2
        button_spacing = 70
        
        self.menu_buttons = [
            Button(button_x, 200, button_width, button_height, "Jogar"),
            Button(button_x, 200 + button_spacing, button_width, button_height, "Melhor Pontuação"),
            Button(button_x, 200 + 2 * button_spacing, button_width, button_height, "Regras"),
            Button(button_x, 200 + 3 * button_spacing, button_width, button_height, "Configurações"),
            Button(button_x, 200 + 4 * button_spacing, button_width, button_height, "Sair")
        ]
        
        # Botões de seleção de tabuleiro
        self.board_buttons = [
            Button(button_x, 250, button_width, button_height, "Tabuleiro 5x5"),
            Button(button_x, 250 + button_spacing, button_width, button_height, "Tabuleiro 10x10"),
            Button(button_x, 250 + 3 * button_spacing, button_width, button_height, "Voltar")
        ]
        
        # Botões de dificuldade
        self.difficulty_buttons = [
            Button(button_x, 200, button_width, button_height, "Fácil"),
            Button(button_x, 200 + button_spacing, button_width, button_height, "Médio"),
            Button(button_x, 200 + 2 * button_spacing, button_width, button_height, "Difícil"),
            Button(button_x, 200 + 4 * button_spacing, button_width, button_height, "Voltar")
        ]
        
        # Botões de modo de jogo
        self.mode_buttons = [
            Button(button_x, 120, button_width, button_height, "Humano"),
            Button(button_x, 120 + button_spacing, button_width, button_height, "A*"),
            Button(button_x, 120 + 2 * button_spacing, button_width, button_height, "Greedy Search"),
            Button(button_x, 120 + 3 * button_spacing, button_width, button_height, "BFS"),
            Button(button_x, 120 + 4 * button_spacing, button_width, button_height, "DFS"),
            Button(button_x, 120 + 5 * button_spacing, button_width, button_height, "Estabilidade Dinâmica"),
            Button(button_x, 120 + 6 * button_spacing, button_width, button_height, "Cascata"),
            Button(button_x, 120 + 7 * button_spacing, button_width, button_height, "Voltar")
        ]
        
        # Botões de configurações de som
        self.sound_buttons = [
            Button(button_x, 200, button_width, button_height, "Som: Ligado" if MUSIC_ENABLED else "Som: Desligado"),
            Button(button_x, 200 + button_spacing, button_width, button_height, "Volume +"),
            Button(button_x, 200 + 2 * button_spacing, button_width, button_height, "Volume -"),
            Button(button_x, 200 + 4 * button_spacing, button_width, button_height, "Voltar")
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
        # Verificar cliques nos botões de configurações
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            
            # Botão de ligar/desligar som
            if self.sound_buttons[0].is_clicked_pos(mouse_pos):
                toggle_music()
                # Atualizar o texto do botão
                self.sound_buttons[0].text = "Som: Ligado" if MUSIC_ENABLED else "Som: Desligado"
                
            # Botão de aumentar volume
            elif self.sound_buttons[1].is_clicked_pos(mouse_pos):
                new_volume = min(1.0, MUSIC_VOLUME + 0.1)
                set_music_volume(new_volume)
                
            # Botão de diminuir volume
            elif self.sound_buttons[2].is_clicked_pos(mouse_pos):
                new_volume = max(0.0, MUSIC_VOLUME - 0.1)
                set_music_volume(new_volume)
                
            # Botão de voltar
            elif self.sound_buttons[3].is_clicked_pos(mouse_pos):
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
        # Desenha o título
        title_surface = title_font.render("Woodblock Puzzle", True, BLACK)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(title_surface, title_rect)
        
        # Desenha os botões
        for button in self.menu_buttons:
            button.draw(screen)
            
    def draw_board_selection(self):
        # Desenha o título
        title_surface = title_font.render("Selecione o Tabuleiro", True, BLACK)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(title_surface, title_rect)
        
        # Desenha os botões
        for button in self.board_buttons:
            button.draw(screen)
            
    def draw_difficulty_selection(self):
        # Desenha o título
        title_surface = title_font.render("Selecione a Dificuldade", True, BLACK)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(title_surface, title_rect)
        
        # Desenha os botões
        for button in self.difficulty_buttons:
            button.draw(screen)
            
    def draw_mode_selection(self):
        # Desenha o título
        title_surface = title_font.render("Selecione o Modo de Jogo", True, BLACK)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 70))
        screen.blit(title_surface, title_rect)
        
        # Desenha os botões
        for button in self.mode_buttons:
            button.draw(screen)
            
    def draw_best_score(self):
        # Desenha o título
        title_surface = title_font.render("Melhor Pontuação", True, BLACK)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(title_surface, title_rect)
        
        # Desenha a pontuação
        score_surface = menu_font.render(f"Pontuação: {self.best_score}", True, BLACK)
        score_rect = score_surface.get_rect(center=(SCREEN_WIDTH // 2, 250))
        screen.blit(score_surface, score_rect)
        
        # Instrução para voltar
        back_surface = button_font.render("Clique para voltar", True, BLACK)
        back_rect = back_surface.get_rect(center=(SCREEN_WIDTH // 2, 500))
        screen.blit(back_surface, back_rect)
        
    def draw_rules(self):
        # Desenha o título
        title_surface = title_font.render("Regras do Jogo", True, BLACK)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 50))
        screen.blit(title_surface, title_rect)
        
        # Regras do jogo
        rules = [
            "- O objetivo é completar linhas e colunas no tabuleiro.",
            "- Você tem 3 peças disponíveis para colocar no tabuleiro.",
            "- Quando uma peça é colocada, uma nova é gerada.",
            "- Ao completar uma linha ou coluna, ela é eliminada.",
            "- O jogo termina quando nenhuma das 3 peças disponíveis",
            "  couber nos espaços vazios do tabuleiro."
        ]
        
        for i, rule in enumerate(rules):
            rule_surface = button_font.render(rule, True, BLACK)
            rule_rect = rule_surface.get_rect(center=(SCREEN_WIDTH // 2, 120 + i * 40))
            screen.blit(rule_surface, rule_rect)
        
        # Instrução para voltar
        back_surface = button_font.render("Clique para voltar", True, BLACK)
        back_rect = back_surface.get_rect(center=(SCREEN_WIDTH // 2, 500))
        screen.blit(back_surface, back_rect)
        
    def draw_settings(self):
        # Desenha o título
        title_surface = title_font.render("Configurações", True, BLACK)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(title_surface, title_rect)
        
        # Desenha os botões de configurações de som
        for button in self.sound_buttons:
            button.draw(screen)
            
        # Exibe o volume atual
        volume_text = f"Volume atual: {int(MUSIC_VOLUME * 100)}%"
        volume_surface = menu_font.render(volume_text, True, BLACK)
        volume_rect = volume_surface.get_rect(center=(SCREEN_WIDTH // 2, 350))
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
