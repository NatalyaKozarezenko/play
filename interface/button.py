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


class RadioButton:
    """Радиокнопка. Доделать, а пока скрыто."""
    def __init__(self, x, y, text, font, font_color, is_selected=False):
        self.x = x
        self.y = y
        self.radius = 8
        self.color_border = (0, 0, 0)
        self.color_background = (255, 255, 255)
        self.text = text
        self.font = font
        self.font_color = font_color
        self.is_selected = is_selected
        self.width = 2

    def draw(self, screen):
        """Рисуем радиокнопку."""
        pygame.draw.circle(
            screen, self.color_background, (self.x, self.y), self.radius
        )
        pygame.draw.circle(
            screen,
            self.color_border,
            (self.x, self.y),
            self.radius,
            self.width
        )

        text_surface = self.font.render(self.text, True, self.font_color)
        text_rect = text_surface.get_rect(
            center=(self.x + self.radius + 20, self.y)
        )
        screen.blit(text_surface, text_rect)

        # если нажата рисуем точку внутри
        if self.is_selected:
            pygame.draw.circle(screen, self.color_border, (self.x, self.y), 3)

    def check_click(self, pos):
        # Нажал ли пользователь внутри радиуса кнопки
        distance = pygame.math.Vector2(
            self.x - pos[0], self.y - pos[1]
        ).length()
        if distance <= self.radius:
            self.is_selected = True
            return True
        return False

    def update(self, screen):
        """Рисуем радиокнопку."""
        pygame.draw.circle(
            screen, self.color_background, (self.x, self.y), self.radius
        )
        pygame.draw.circle(
            screen, self.color_border,
            (self.x, self.y), self.radius, self.width
        )

        # если нажата рисуем точку внутри
        if self.is_selected:
            pygame.draw.circle(screen, self.color_border, (self.x, self.y), 3)
