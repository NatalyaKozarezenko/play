import random

import pygame

from constants import (BISHOP_IMAGE, BACKGROUND_COLOR, CAST,
                       CUBE_HEIGHT, CUBE_WIDTH, PLAYER_IMAGE,
                       GRID_SIZE, KING_IMAGE, KNIGHT_IMAGE, LEFT_PANEL,
                       MENU_BORDER, MENU_HEIGHT, PAWN_IMAGE, QUEEN_IMAGE,
                       ROOK_IMAGE, SCREEN_HEIGHT, HELP_COLOR,
                       SCREEN_WIDTH, STRAT_HEIGHT, STRAT_WIDTH)

clock = pygame.time.Clock()

class Cube(pygame.sprite.Sprite):
    """Кубик."""

    def __init__(self, filename=PAWN_IMAGE):
        """Инициализация кубика."""
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert_alpha()
        self.image = pygame.transform.scale(
            self.image, (CUBE_WIDTH, CUBE_HEIGHT)
        )
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH + (LEFT_PANEL - CUBE_WIDTH) // 2
        self.rect.y = (SCREEN_HEIGHT - CUBE_HEIGHT) // 2

    def cast(self, screen):
        """Анимация броска кубика."""
        y_up = [-20, -40, -60, -80, -100, -80, -60, -40]
        image_sprite = {}
        for id, image in enumerate(CAST * 2):
            image_sprite[pygame.image.load(image)] = y_up[id]
        for image, value in image_sprite.items():
            self.reset(screen)
            screen.blit(
                pygame.transform.scale(image, (CUBE_WIDTH, CUBE_HEIGHT)),
                (self.rect.x, self.rect.y + value)
            )
            pygame.display.update()
            clock.tick(15)

    def generate_cube_values(self, font_text, message, screen):
        """Генерим выпавшее значение строны куба и вызываем отрисовку."""
        self.cast(screen)  # анимация броска кубика
        values = [
            PAWN_IMAGE, ROOK_IMAGE, KING_IMAGE,
            #  Пешка        Ладья       Король
            BISHOP_IMAGE, KNIGHT_IMAGE, QUEEN_IMAGE
            #   Слон        Конь          Ферзь
        ]

        image_cube = random.choice(values)
        self.reset(screen)
        help_text = font_text.render(message, True, HELP_COLOR)
        screen.blit(help_text, (self.rect.x, self.rect.y - 25))
        self.__init__(image_cube)
        return image_cube

    def reset(self, screen):
        """закрашиваем всю левую часть, кроме меню в чёрное."""
        reset_rect = pygame.Rect(
            (SCREEN_WIDTH + 1, MENU_BORDER + MENU_HEIGHT),
            (LEFT_PANEL, SCREEN_HEIGHT)
        )
        pygame.draw.rect(screen, BACKGROUND_COLOR, reset_rect)

class Player(pygame.sprite.Sprite):
    """Фишки игроков."""
    def __init__(self, filename=PLAYER_IMAGE):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert_alpha()
        self.image = pygame.transform.scale(
            self.image, (GRID_SIZE, GRID_SIZE)
        )
        self.rect = self.image.get_rect()
        self.rect.x = STRAT_WIDTH
        self.rect.y = STRAT_HEIGHT
        self.position = (self.rect.x, self.rect.y)
        self.double_step = False
        self.not_step = False
