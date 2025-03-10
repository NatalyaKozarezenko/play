"""План-прехват:
0. лишние отрисовки ПРОВЕРИТЬ???
1. Настройки: уровень компа, выбор фишки, язык
2. добавить Музыку
3. Мобильная версия
"""

import random
import pygame

from constants import (
    ALL_WIDTH, BACKGROUND_SCENE, BACKGROUND_LOSS_SCENE, BACKGROUND_MAIN_SCENE,
    BACKGROUND_MENU_SCENE, BEETWEEN_HEAD_1_TEXT, BETWEEN_HEAD_HEAD_1,
    BOARD_BORDER_X_R, BOARD_BORDER_Y, BOARD_HEIGHT, BOARD_WIDTH,
    CELL_DOUBLE_STEP_COLOR, CELL_NOT_STEP_COLOR, COMP_IMAGE,
    COUNT_DOUBLE_STEP, COUNT_GRID, COUNT_NOT_STEP,
    FINISH_HEIGHT, FINISH_IMAGE, FINISH_WIDTH, TEXT_COLOR, FONT, GRID_SIZE,
    HELP_COLOR, LINE_COLOR, MENU, MENU_BORDER, MENU_HEIGHT, MENU_WIDTH,
    HELP_MESSAGE, NAME_PLAY, PLAYER_IMAGE, SCREEN_HEIGHT,
    SCREEN_WIDTH, ICO_IMAGE, BUTTON_TEXTS_MENU_SCENE, NAME_RULES_SCENE, RULES,
    BETWEEN_TEXT, BUTTON_TEXTS_RULES_SCENE, BUTTON_TEXTS_LOSS_SCENE,
    WIN_TEXTS, TEXTS_LOSS_SCENE, QWESTION_TEXT, BUTTON_TEXTS_WIN_SCENE,
    DEFAULT_IMAGE, STRAT_WIDTH, STRAT_HEIGHT
)
from interface.button import Button
from interface.cells import Cell, Cells, CellsHelp
from interface.sprites import Cube, Player

pygame.init()
screen = pygame.display.set_mode((ALL_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(NAME_PLAY)
pygame.display.set_icon(pygame.image.load(ICO_IMAGE))

clock = pygame.time.Clock()
current_scene = None

font_head = pygame.font.Font(FONT, 30)
font_head_1 = pygame.font.Font(FONT, 25)
font_text = pygame.font.Font(FONT, 18)


class Menu():
    def __init__(self):
        self.menu_image = pygame.transform.scale(
            pygame.image.load(MENU), (MENU_WIDTH, MENU_HEIGHT)
        )
        self.menuimagerect = self.menu_image.get_rect()
        self.menuimagerect.topright = (ALL_WIDTH - MENU_BORDER, MENU_BORDER)

    def draw(self, screen):
        screen.blit(self.menu_image, self.menuimagerect)


menu = Menu()
cells_not_step = Cells(COUNT_NOT_STEP, CELL_NOT_STEP_COLOR)
cells_double_step = Cells(COUNT_DOUBLE_STEP, CELL_DOUBLE_STEP_COLOR)
cells_help = CellsHelp()
cube = Cube()
player = Player(PLAYER_IMAGE)
comp = Player(COMP_IMAGE)


def draw_field():
    """Разлиновываем поле и ячейку ФИНИШ."""
    for i in range(0, COUNT_GRID + 1):
        pygame.draw.line(
            screen,
            LINE_COLOR,
            (BOARD_BORDER_X_R + GRID_SIZE * i, BOARD_BORDER_Y),
            (BOARD_BORDER_X_R + GRID_SIZE * i, BOARD_HEIGHT + BOARD_BORDER_Y),
            width=1
        )
        pygame.draw.line(
            screen,
            LINE_COLOR,
            (BOARD_BORDER_X_R, GRID_SIZE * i + BOARD_BORDER_Y),
            (BOARD_BORDER_X_R + BOARD_WIDTH, GRID_SIZE * i + BOARD_BORDER_Y),
            width=1
        )
    scale = pygame.transform.scale(
        pygame.image.load(FINISH_IMAGE).convert(),
        (GRID_SIZE - 2, GRID_SIZE - 2)
    )
    screen.blit(scale, (FINISH_WIDTH + 2, FINISH_HEIGHT + 2))


def get_position_new_cell(mouse_position, good_positions):
    """Может ли пользователь ходить на то поле, на которое он нажал."""
    mouse_x, mouse_y = mouse_position
    for position in good_positions:
        good_x, good_y = position
        if (good_x <= mouse_x <= good_x + GRID_SIZE
                and good_y <= mouse_y <= good_y + GRID_SIZE):
            return (good_x, good_y)
    # кликнул туда, куда ходить не может
    return None


def check_double_not_step(
        object, opponent, cells_double_step, cells_not_step
):
    """Проверка на дополнительный ход, пропуск хода."""
    object.double_step = object.position in cells_double_step.positions
    if opponent.not_step:
        object.double_step = True
        opponent.not_step = False
    object.not_step = object.position in cells_not_step.positions
    if object.double_step == object.not_step == True:
        object.double_step = False
        object.not_step = False


def reset_old_position(
        game_object1, game_object2, cells_double_step, cells_not_step
):
    """Возврат нормального вида ячейки когда ушли."""
    cell = Cell(game_object1.position)
    if game_object1.position in cells_double_step.positions:
        cell.draw(screen, CELL_DOUBLE_STEP_COLOR)
    elif game_object1.position in cells_not_step.positions:
        cell.draw(screen, CELL_NOT_STEP_COLOR)
    else:
        cell.draw(screen)
    if game_object1.position == game_object2.position:
        screen.blit(game_object2.image, game_object2.position)


def switch_scene(scene):
    """Смена сцены."""
    global current_scene
    current_scene = scene


def get_comp_new_position(
        level, cells_help, cells_double_step, cells_not_step
):
    """Выбор ячейки куда пойти компа в соответствии с уровнем."""
    if (FINISH_WIDTH, FINISH_HEIGHT) in cells_help.positions:
        return (FINISH_WIDTH, FINISH_HEIGHT)
    if level == 0:
        return random.choice(cells_help.positions)
    best_position = []
    count_to_finish = {}
    if level == 1:
        for position in cells_help.positions:
            if position in cells_double_step.positions:
                best_position.append(position)
            else:
                x, y = position
                count = (FINISH_WIDTH - x) // GRID_SIZE
                + (y - FINISH_HEIGHT) // GRID_SIZE
                if position in cells_not_step.positions:
                    count_to_finish[position] = (abs(count), 'bad')
                else:
                    count_to_finish[position] = (abs(count), 'ok')
        ok_positions = {
            key: value for key, value in count_to_finish.items()
            if value[1] == 'ok'
        }
        if ok_positions:
            min_distance = min(ok_positions.values(), key=lambda x: x[0])[0]
            best_position = [
                key for key, value in ok_positions.items()
                if value[0] == min_distance
            ]
            great_position = [
                pos for pos in best_position
                if pos in cells_double_step.positions
            ]
            if great_position:
                return random.choice(great_position)
            if best_position:
                return random.choice(best_position)
        bad_positions = {
            key: value for key, value in count_to_finish.items()
            if value[1] == 'bad'
        }
        if bad_positions:
            min_distance = min(bad_positions.values(), key=lambda x: x[0])[0]
            return random.choice(
                [key for key, value in bad_positions.items()
                 if value[0] == min_distance]
            )

    return random.choice(cells_help.positions)


def draw_in_position(image, new_position, opponent_image, opponent_position):
    """Рисуем фишку в новой ячейке или две фишки, если они в одной ячейки."""
    if new_position == opponent_position:
        cell = Cell(new_position)
        cell.draw(screen)
        x, y = new_position
        screen.blit(image, (x + 18, y))
        screen.blit(opponent_image, (x - 18, y))
    else:
        screen.blit(image, new_position)


def background_menu(screen, image=DEFAULT_IMAGE, size=(ALL_WIDTH, SCREEN_HEIGHT)):
    """Фоновая картинка и кнопка меню."""
    background = pygame.transform.scale(
        pygame.image.load(image).convert(), size
    )
    screen.blit(background, (0, 0))
    menu.draw(screen)


def main_scene():
    """Главная сцена игры."""
    background_menu(
        screen, BACKGROUND_MAIN_SCENE,
        (SCREEN_WIDTH, SCREEN_HEIGHT)
    )

    draw_field()
    player.position = comp.position = (STRAT_WIDTH, STRAT_HEIGHT)

    cells_not_step.draw(screen)
    cells_double_step.draw(screen)
    draw_in_position(player.image, player.position, comp.image, comp.position)

    end_play = False
    while not end_play:
        if not comp.double_step and not player.not_step:
            value = cube.generate_cube_values(font_text, HELP_MESSAGE, screen)
            screen.blit(cube.image, cube.rect)
            cells_help.get_position(value, player.position)
            if cells_help.positions != []:
                cells_help.draw(HELP_COLOR, screen)
                pygame.display.flip()

                new_position = None
                while not end_play and new_position is None:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            end_play = True
                            switch_scene(None)
                        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                                new_position = event.pos
                    if new_position:
                        if menu.menuimagerect.collidepoint(new_position):
                            end_play = True
                            switch_scene(rules_scene)
                        else:
                            new_position = get_position_new_cell(
                                new_position, cells_help.positions
                            )
                if new_position is not None:
                    reset_old_position(
                        player, comp, cells_double_step, cells_not_step
                    )
                    player.position = new_position
                    draw_in_position(
                        player.image, player.position, comp.image, comp.position
                    )
                    cells_help.draw(LINE_COLOR, screen)
                    cells_help.positions = []
                    pygame.display.flip()
                    if player.position == (FINISH_WIDTH, FINISH_HEIGHT):
                        end_play = True
                        switch_scene(winning_screne)
                    check_double_not_step(
                        player, comp, cells_double_step, cells_not_step
                    )

        if not player.double_step and not end_play and not comp.not_step:
            value = cube.generate_cube_values(font_text, '', screen)
            cells_help.get_position(value, comp.position)

            level = 1
            if cells_help.positions != []:
                reset_old_position(
                    comp, player, cells_double_step, cells_not_step
                )
                comp.position = get_comp_new_position(
                    level, cells_help, cells_double_step, cells_not_step
                )
                draw_in_position(
                    comp.image, comp.position, player.image, player.position
                )
                cells_help.positions = []
                if comp.position == (FINISH_WIDTH, FINISH_HEIGHT):
                    switch_scene(loss_screne)
                    end_play = True
                check_double_not_step(
                    comp, player, cells_double_step, cells_not_step
                )


def handle_events(buttons, button_scenes, scene_name=True):
    """Определяем что нажато и меняем сцену."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            scene_name = False
            switch_scene(None)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and buttons is not None:
                for button in buttons:
                    if button.rect.collidepoint(event.pos):
                        for scene, button_text in button_scenes.items():
                            if button.text == button_text:
                                switch_scene(scene)
                                scene_name = False
                                screen.fill((0, 0, 0))
                                menu.draw(screen)
    pygame.display.flip()
    return scene_name


def print_text(texts, text_position_y, between_text, text_position_x=100, font=font_text):
    """Выводим абзац текста сцена Правила игры."""
    for text in texts:
        text_render = font.render(text, True, TEXT_COLOR)
        screen.blit(text_render, (text_position_x, text_position_y))
        text_position_y += between_text


def rules_scene():
    """Правила игры."""
    background_menu(screen, BACKGROUND_SCENE)
    head_text = font_head.render(NAME_RULES_SCENE, True, TEXT_COLOR)
    text_width, text_height = head_text.get_size()
    screen.blit(head_text, ((ALL_WIDTH - text_width) // 2, 15 + text_height))

    position_text = BETWEEN_TEXT * 6
    for value in RULES:
        print_text(value, position_text, BETWEEN_TEXT)
        position_text += BETWEEN_TEXT * (len(value) + 2)

    buttons = Button.create_buttons_horizontally(
        screen, BUTTON_TEXTS_RULES_SCENE, position_text + 50
    )
    button_scenes = {
        main_scene: BUTTON_TEXTS_RULES_SCENE[0]
    }

    rules_game = True
    while rules_game:
        rules_game = handle_events(buttons, button_scenes)


def winning_screne():
    """Выигрыш."""
    image_sprite = [
        f'images/mfinish_{str(i).zfill(4)}.png' for i in range(1, 18)
    ]
    image_sprite = [pygame.image.load(image) for image in image_sprite]
    for image in image_sprite:
        screen.fill((0, 0, 0))
        screen.blit(
            pygame.transform.scale(
                image, (screen.get_width(), screen.get_height())
            ),
            (0, 0)
        )
        pygame.display.update()
        clock.tick(20)

    text_in_screen = font_head.render(random.choice(WIN_TEXTS), True, TEXT_COLOR)
    text_position_y = 600
    screen.blit(
        text_in_screen,
        text_in_screen.get_rect(
            center=(screen.get_width() // 2, text_position_y)
        )
    )
    qwestion = font_head.render(QWESTION_TEXT, True, TEXT_COLOR)
    text_position_y += 30
    screen.blit(
        qwestion,
        qwestion.get_rect(center=(screen.get_width() // 2, text_position_y))
    )

    buttons = Button.create_buttons_horizontally(
        screen, BUTTON_TEXTS_WIN_SCENE, text_position_y + 30
    )
    button_scenes = {
        main_scene: BUTTON_TEXTS_WIN_SCENE[0]
    }
    winning = True
    while winning:
        winning = handle_events(buttons, button_scenes)


def loss_screne():
    """Проигрыш."""

    background = pygame.transform.scale(
        pygame.image.load(BACKGROUND_LOSS_SCENE).convert_alpha(), (ALL_WIDTH, SCREEN_HEIGHT)
    )
    screen.blit(background, (0, 0))
    menu.draw(screen)
    print_text(TEXTS_LOSS_SCENE, 180, 50, 420, font_head)

    buttons = Button.create_buttons_horizontally(
        screen, BUTTON_TEXTS_LOSS_SCENE, 440
    )
    button_scenes = {
        main_scene: BUTTON_TEXTS_LOSS_SCENE[0],
    }
    loss = True
    while loss:
        loss = handle_events(buttons, button_scenes)


if __name__ == '__main__':
    """При запуске сразу открываем игру."""
    switch_scene(main_scene)
    while current_scene is not None:
        current_scene()
    pygame.quit()