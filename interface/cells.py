from random import randint

import pygame

from constants import (BISHOP_IMAGE, BACKGROUND_COLOR, BOARD_BORDER_X_R,
                       BOARD_BORDER_Y, BOARD_HEIGHT, BOARD_WIDTH, COUNT_GRID,
                       FINISH_HEIGHT, FINISH_WIDTH, GRID_SIZE, KING_IMAGE,
                       KNIGHT_IMAGE, LINE_COLOR, PAWN_IMAGE, QUEEN_IMAGE,
                       ROOK_IMAGE, START_IMAGE, STRAT_HEIGHT, STRAT_WIDTH)

used_cells = [(STRAT_WIDTH, STRAT_HEIGHT), (FINISH_WIDTH, FINISH_HEIGHT)]


class Cell:
    """Одиночная ячейка."""

    def __init__(self, position=None):
        """Пустая базовая чейка."""
        self.color = BACKGROUND_COLOR
        self.position = position

    def draw(self, screen, color=None, position=None):
        """Закрашиваем ячейку в цвет или СТАРТ."""
        if color is None:
            color = self.color
        if position is None:
            position = self.position
        if self.position == (STRAT_WIDTH, STRAT_HEIGHT):
            scale = pygame.transform.scale(
                pygame.image.load(START_IMAGE).convert(),
                (GRID_SIZE - 2, GRID_SIZE - 2)
            )
            screen.blit(scale, position)
        else:
            cell = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, color, cell)
            pygame.draw.rect(screen, LINE_COLOR, cell, 1)


class Cells(Cell):
    """Класс ячеек поля."""

    def __init__(self, count=0, color=None):
        """Характеристика ячеек."""
        self.count = count
        self.color = color
        self.positions = []
        self.general_position()

    def general_position(self):
        """Задаем случайное положение."""
        while len(self.positions) < self.count:
            position = self.randomize_position()
            if position not in used_cells:
                list.append(used_cells, position)
                list.append(self.positions, position)

    def draw(self, screen):
        """Рисуем ячейки."""
        for self.position in self.positions:
            super().draw(screen)

    def randomize_position(self):
        """Вычисляем случайное положение ячейки."""
        return (
            BOARD_BORDER_X_R + randint(0, COUNT_GRID - 1) * GRID_SIZE,
            BOARD_BORDER_Y + randint(0, COUNT_GRID - 1) * GRID_SIZE
        )


class CellsHelp():
    """Ячейки-подсказки, куда можно ходить."""

    def __init__(self):
        """Начальное значение."""
        self.positions = []

    def get_position_screen(self, step_x, step_y, *player_position):
        """Не включаем поля, выходящие за пределы поля."""
        x = player_position[0] + GRID_SIZE * step_x
        y = player_position[1] + GRID_SIZE * step_y
        if (BOARD_BORDER_X_R <= x < BOARD_WIDTH + BOARD_BORDER_X_R
           and BOARD_BORDER_Y <= y < BOARD_HEIGHT + BOARD_BORDER_Y):
            self.positions.append((x, y))

    def get_position(self, value, position):
        """Позиции полей куда можно пойти по значению кубика."""
        piece_offset = {
            # Пешка – ход вверх на одну клетку.
            PAWN_IMAGE: [(0, -1)],
            # Ладья – ходит вверх или низ, или вправо, или влево на 2 клетки.
            ROOK_IMAGE: [(0, -2), (0, 2), (2, 0), (-2, 0)],
            # Король – ходит в любом направлении на 1 клетку.
            KING_IMAGE: [
                (0, -1), (0, 1), (1, 0), (-1, 0),
                (1, -1), (1, 1), (-1, 1), (-1, -1)
            ],
            # Слон – ходит по диагонали в любую сторону на 2 клетки.
            BISHOP_IMAGE: [(2, -2), (2, 2), (-2, 2), (-2, -2)],
            # Конь – «буквой Г».
            KNIGHT_IMAGE: [
                (2, 1), (2, -1), (-1, -2), (1, -2),
                (-1, 2), (1, 2), (-2, 1), (-2, -1)
            ],
            # Ферзь – ходит в любую сторону на 2 клетки.
            QUEEN_IMAGE: [
                (0, -2), (0, 2), (2, 0), (-2, 0),
                (2, -2), (2, 2), (-2, 2), (-2, -2)
            ]
        }

        offset = piece_offset.get(value, [])
        for step_x, step_y in offset:
            self.get_position_screen(step_x, step_y, *position)

    def draw(self, color, screen):
        """Бордер для ячеек-подсказок."""
        for self.position in self.positions:
            rect = pygame.Rect(self.position, (GRID_SIZE + 1, GRID_SIZE + 1))
            pygame.draw.rect(screen, color, rect, 1)
