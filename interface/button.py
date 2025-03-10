import pygame

from constants import ALL_WIDTH, FONT, TEXT_COLOR


class Button():
    """Кнопка."""

    BUTTON_WIDTH, BUTTON_HEIGHT = 180, 50

    def __init__(self, x, y, text):
        """Дизан и текст кнопки."""
        font = pygame.font.Font(FONT, 20)
        self.rect = pygame.Rect(x, y, self.BUTTON_WIDTH, self.BUTTON_HEIGHT)
        self.text = text
        self.text_rendered = font.render(self.text, True, TEXT_COLOR)

    def draw(self, screen):
        """Кнопка на экран."""
        BUTTON_COLOR = (0, 214, 117)
        BORDER_COLOR = (0, 0, 0)
        BORDER_WIDTH = 1
        pygame.draw.rect(screen, BUTTON_COLOR, self.rect)
        pygame.draw.rect(screen, BORDER_COLOR, self.rect, BORDER_WIDTH)
        text_rect = self.text_rendered.get_rect(center=self.rect.center)
        screen.blit(self.text_rendered, text_rect)

    @staticmethod
    def create_buttons_upright(button_texts, y_position, between_buttons=100):
        """Создание списка кнопок для отображения на экране по вертикали."""
        buttons = []
        x_position = (ALL_WIDTH - Button.BUTTON_WIDTH) // 2
        for count_button in range(len(button_texts)):
            button = Button(
                x_position,
                y_position + count_button * between_buttons,
                button_texts[count_button]
            )
            buttons.append(button)
        return buttons

    @staticmethod
    def create_buttons_horizontally(
        screen, button_texts, y_position, between_buttons=50
    ):
        """Создание списка кнопок для отображения на экране по горизонтали."""
        buttons = []
        count_buttons = len(button_texts)
        x_position = (
            ALL_WIDTH - Button.BUTTON_WIDTH * count_buttons
            - between_buttons * (count_buttons - 1)
        ) // 2
        for count_button in range(len(button_texts)):
            button = Button(
                x_position + count_button * (
                    Button.BUTTON_WIDTH + between_buttons
                ),
                y_position,
                button_texts[count_button]
            )
            buttons.append(button)
        for button in buttons:
            button.draw(screen)
        pygame.display.update()
        return buttons

