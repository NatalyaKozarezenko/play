import random

import pygame

from constants import (BISHOP_IMAGE, BOARD_BACKGROUND_COLOR, CUBE_HEIGHT,
                       CUBE_WIDTH, DEFAULT_IMAGE, FONT, GRID_SIZE, KING_IMAGE,
                       KNIGHT_IMAGE, LEFT_PANEL, MENU_BORDER, MENU_HEIGHT,
                       PAWN_IMAGE, QUEEN_IMAGE, ROOK_IMAGE, SCREEN_HEIGHT,
                       SCREEN_WIDTH, STRAT_HEIGHT, STRAT_WIDTH)

clock = pygame.time.Clock()


class Cube(pygame.sprite.Sprite):
    """Кубик."""

    def __init__(self, filename=DEFAULT_IMAGE):
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
        image_sprite = {
            pygame.image.load('images/myrotation1.png'): -20,
            pygame.image.load('images/myrotation2.png'): -40,
            pygame.image.load('images/myrotation3.png'): -60,
            pygame.image.load('images/myrotation4.png'): -80,
            pygame.image.load('images/myrotation1.png'): -100,
            pygame.image.load('images/myrotation2.png'): -80,
            pygame.image.load('images/myrotation3.png'): -60,
            pygame.image.load('images/myrotation4.png'): -40,
            pygame.image.load('images/myrotation1.png'): -20
        }
        for image, value in image_sprite.items():
            # очищаем всю левую часть, кроме меню в чёрное.
            reset_rect = pygame.Rect(
                (SCREEN_WIDTH + 1, MENU_BORDER + MENU_HEIGHT),
                (LEFT_PANEL, SCREEN_HEIGHT)
            )
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, reset_rect)
            # думаю надо ли текст-подсказку
            # text = font.render('Бросаем кубик...', True, (255, 255, 255))
            # screen.blit(text, (self.rect.x - 40, self.rect.y - 25))
            screen.blit(
                pygame.transform.scale(image, (CUBE_WIDTH, CUBE_HEIGHT)),
                (self.rect.x, self.rect.y + value)
            )
            pygame.display.update()
            clock.tick(15)

    def draw(self, filename, message, screen):
        """Отрисовка выпавшей строны куба."""
        # закрасили
        player = pygame.Rect(
            (self.rect.x - 40, self.rect.y - 25),
            (CUBE_WIDTH + 100, CUBE_HEIGHT + 25)
        )
        pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, player)
        text = pygame.font.Font(FONT, 18).render(
            message, True, (255, 255, 255)
        )
        # выводим текст-подсказку
        screen.blit(text, (self.rect.x - 40, self.rect.y - 25))
        # отрисовали нужное
        self.__init__(filename)

    def generate_cube_values(self, message, screen):
        """Генерим выпавшее значение строны куба и вызываем отрисовку."""
        self.cast(screen)  # анимация броска кубика
        values = [
            PAWN_IMAGE, ROOK_IMAGE, KING_IMAGE,
            #  Пешка        Ладья       Король
            BISHOP_IMAGE, KNIGHT_IMAGE, QUEEN_IMAGE
            #   Слон        Конь          Ферзь
        ]

        image_cube = random.choice(values)
        self.draw(image_cube, message, screen)
        return image_cube


class Player(pygame.sprite.Sprite):
    """Фишки игроков."""
    def __init__(self, filename=DEFAULT_IMAGE):
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
