"""План-прехват:
0. лишние отрисовки ПРОВЕРИТЬ???
1. Настройки: уровень компа, выбор фишки, язык
2. добавить Музыку
3. Мобильная версия
"""
# from moviepy import VideoFileClip
import random

# from tkinter import *
# from tkinter import Button as tkButton
import pygame

# from random import randint
# from moviepy import ImageSequenceClip
from constants import (ALL_WIDTH, BACKGROUND_IMAGE, BACKGROUND_IMAGE_LOSS,
                       BACKGROUND_IMAGE_MAIN, BACKGROUND_IMAGE_MENU,
                       BEETWEEN_HEAD_1_TEXT, BETWEEN_HEAD_HEAD_1,
                       BOARD_BORDER_X_R, BOARD_BORDER_Y, BOARD_HEIGHT,
                       BOARD_WIDTH, CELL_DOUBLE_STEP_COLOR,
                       CELL_NOT_STEP_COLOR, COMP_IMAGE, COUNT_DOUBLE_STEP,
                       COUNT_GRID, COUNT_NOT_STEP, DEFAULT_IMAGE,
                       FINISH_HEIGHT, FINISH_IMAGE, FINISH_WIDTH, FONT,
                       FONT_COLOR, GRID_SIZE, HELP_COLOR, LINE_COLOR, MENU,
                       MENU_BORDER, MENU_HEIGHT, MENU_WIDTH, NAME_PLAY,
                       PLAYER_IMAGE, SCREEN_HEIGHT, SCREEN_WIDTH)
from interface.button import Button, RadioButton
from interface.cells import Cell, Cells, CellsHelp
from interface.sprites import Cube, Player

pygame.init()     # подготовки модулей pygame к работе
clock = pygame.time.Clock()  # для вращения кубика

# Задаем экран
screen = pygame.display.set_mode((ALL_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(NAME_PLAY)

current_scene = None

font_head = pygame.font.Font(FONT, 30)  # заголовок
font_head_1 = pygame.font.Font(FONT, 25)  # подзаголовок
font_text = pygame.font.Font(FONT, 18)   # обычный текст


class Menu():
    def __init__(self):
        self.menu_image = pygame.transform.scale(
            pygame.image.load(MENU), (MENU_WIDTH, MENU_HEIGHT)
        )
        # делаем из картинки прямоугольник
        self.menuimagerect = self.menu_image.get_rect()
        # устанавливаем в правый верхний угол
        self.menuimagerect.topright = (ALL_WIDTH - MENU_BORDER, MENU_BORDER)

    def draw(self, screen):
        screen.blit(self.menu_image, self.menuimagerect)


menu = Menu()


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
    # "ФИНИШ" вправо верх, не угол +2 - чтоб сетка была видна хорошо
    screen.blit(scale, (FINISH_WIDTH + 2, FINISH_HEIGHT + 2))


def handle_keys():
    """Обрабатывает нажатия клавиш для главной сцены."""
    # global speed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            switch_scene(None)
        if event.type == pygame.MOUSEBUTTONDOWN:
            # левая клавиши мыши
            if event.button == 1:
                # сюда хочет пользователь
                return event.pos


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
    # дополнительный ход
    object.double_step = object.position in cells_double_step.positions
    # сброс пропуск хода
    if opponent.not_step:
        object.double_step = True
        opponent.not_step = False
    # пропуск хода
    object.not_step = object.position in cells_not_step.positions


def reset_old_position(
        game_object1, game_object2, cells_double_step, cells_not_step
):
    """Возврат нормального вида ячейки когда ушли."""
    # стираем старую фишку и возвращаем ячейке нужный цвет
    cell = Cell(game_object1.position)
    if game_object1.position in cells_double_step.positions:
        cell.draw(screen, CELL_DOUBLE_STEP_COLOR)
    elif game_object1.position in cells_not_step.positions:
        cell.draw(screen, CELL_NOT_STEP_COLOR)
    else:
        cell.draw(screen)
    # если фишки стояли вместе
    if game_object1.position == game_object2.position:
        # перерисовать фишку компа, чтоб не стерлась
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
    if level == 0:  # УРОВЕНЬ: дурак - выбор случайный
        return random.choice(cells_help.positions)
    best_position = []
    count_to_finish = {}
    if level == 1:  # УРОВЕНЬ: выбир ячейки с доп ходом + направление
        for position in cells_help.positions:
            if position in cells_double_step.positions:
                best_position.append(position)
                # print('двойной ход', best_position)
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
        # значит делаем выборку из позиций с пропуском хода
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

    # на все остальные случаи
    return random.choice(cells_help.positions)


def draw_in_position(image, new_position, opponent_image, opponent_position):
    """Рисуем фишку в новой ячейке или две фишки, если они в одной ячейки."""
    if new_position == opponent_position:
        # закрашиваем фон
        cell = Cell(new_position)
        cell.draw(screen)
        # рисуем фишки вместе
        x, y = new_position
        screen.blit(image, (x + 18, y))
        screen.blit(opponent_image, (x - 18, y))
    else:
        screen.blit(image, new_position)


def background_menu(image, screen, size=(ALL_WIDTH, SCREEN_HEIGHT)):
    """Фоновая картинка и кнопка меню."""
    background = pygame.transform.scale(
        pygame.image.load(image).convert(), size
    )
    screen.blit(background, (0, 0))
    menu.draw(screen)


def main_scene():
    """Главная сцена игры."""
    background_menu(
        BACKGROUND_IMAGE_MAIN, screen,
        (SCREEN_WIDTH, SCREEN_HEIGHT)
    )
    draw_field()

    # pygame.time.wait(2000) # задержка
    # ячейки пропуска хода
    cells_not_step = Cells(COUNT_NOT_STEP, CELL_NOT_STEP_COLOR)
    # дополнительный ход
    cells_double_step = Cells(COUNT_DOUBLE_STEP, CELL_DOUBLE_STEP_COLOR)
    cells_help = CellsHelp()
    cube = Cube(DEFAULT_IMAGE)
    player = Player(PLAYER_IMAGE)
    comp = Player(COMP_IMAGE)
    # рисуем ячейки с особенными полями
    cells_not_step.draw(screen)
    cells_double_step.draw(screen)
    # расстановка двух фишек на старт
    draw_in_position(player.image, player.position, comp.image, comp.position)

    end_play = False
    while not end_play:
        if not comp.double_step and not player.not_step:  # ХОД ПОЛЬЗОВАТЕЛЯ
            # получаем значение строны кубика, которое выпало
            value = cube.generate_cube_values('Ходите', screen)
            screen.blit(cube.image, cube.rect)
            cells_help.get_position(value, player.position)
            # если есть куда идти т е есть ячейки-подсказки
            if cells_help.positions != []:
                cells_help.draw(HELP_COLOR, screen)
                pygame.display.flip()

                new_position = None
                # пока кликнет в ячейке-подсказке или выход
                while not end_play and new_position is None:
                    # определяем коор нажатия
                    mouse_position = handle_keys()
                    if mouse_position is not None:
                        # кнопка меню
                        if menu.menuimagerect.collidepoint(mouse_position):
                            # switch_scene(menu_scene)
                            # пока выводятся правила, но доделать настройку
                            switch_scene(rules_game_scene)
                            end_play = True
                        else:
                            # попал ли в ячейку-подсказку
                            new_position = get_position_new_cell(
                                mouse_position, cells_help.positions
                            )
                if new_position is not None:
                    # стираем старую фишку и возвращаем ячейке нужный цвет
                    reset_old_position(
                        player, comp, cells_double_step, cells_not_step
                    )
                    # задаем новую позицию
                    player.position = new_position
                    # рисуем фишки на новом месте
                    draw_in_position(
                        player.image, player.position,
                        comp.image, comp.position
                    )
                    # скрываем подсказки
                    cells_help.draw(LINE_COLOR, screen)
                    # подсказки обнулили
                    cells_help.positions = []
                    pygame.display.flip()
                    # проверка на выигрыш:
                    if player.position == (FINISH_WIDTH, FINISH_HEIGHT):
                        switch_scene(winning_screne)
                        end_play = True
                    check_double_not_step(
                        player, comp, cells_double_step, cells_not_step
                    )
            else:
                # Если ячеек-подсказок нет - ходить не куда = пропуск хода.
                # Например: рядом граница и ходить не куда дальше.
                # ПРИДУМАТЬ В КАК СООБЩАТЬ
                print('Переход хода.')

        # если у игрока ещё один ход, то комп в пролете:
        # ХОД КОМПА
        if not player.double_step and not end_play and not comp.not_step:
            # бросок кубика Тут нам сообщение зачем?
            value = cube.generate_cube_values('', screen)
            # определяем на какие поля можем сходить
            cells_help.get_position(value, comp.position)

            level = 1
            if cells_help.positions != []:
                # А если в подсказках пусто = пропуск хода = НИчего не делаем
                reset_old_position(
                    comp, player, cells_double_step, cells_not_step
                )
                comp.position = get_comp_new_position(
                    level, cells_help, cells_double_step, cells_not_step
                )
                draw_in_position(
                    comp.image, comp.position, player.image, player.position
                )
                cells_help.positions = []  # подсказки
                # проверка на выигрыш:
                if comp.position == (FINISH_WIDTH, FINISH_HEIGHT):
                    switch_scene(loss_screne)
                    end_play = True
                # проверка ячеки на дополнительный ход
                check_double_not_step(
                    comp, player, cells_double_step, cells_not_step
                )


def handle_events(buttons, button_scenes, scene_name=True):
    """Определяем что нажато и меняем сцену."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
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
                                # доб кнопку меню
                                menu.draw(screen)
    pygame.display.flip()
    return scene_name


def menu_scene():
    """Окно меню."""
    background_menu(BACKGROUND_IMAGE_MENU, screen)
    BUTTON_TEXTS = ['Правила игры', 'Настройки', 'Выход']
    buttons = Button.create_buttons_upright(BUTTON_TEXTS, 200)
    for button in buttons:
        button.draw(screen)
    button_scenes = {
        rules_game_scene: BUTTON_TEXTS[0],
        settings_screne: BUTTON_TEXTS[1],
        main_scene: BUTTON_TEXTS[2],
    }
    menu = True
    while menu:
        menu = handle_events(buttons, button_scenes)


def print_text(texts, text_position, between_text):
    """Выводим абзац текста сцена Правила игры."""
    for text in texts:
        font_text = pygame.font.Font(FONT, 18)
        text_surface = font_text.render(text, True, FONT_COLOR)
        screen.blit(text_surface, (100, text_position))
        text_position += between_text


def rules_game_scene():
    """Правила игры."""
    background_menu(BACKGROUND_IMAGE, screen)
    head_text = font_head.render('Правила игры.', True, FONT_COLOR)
    text_width, text_height = head_text.get_size()
    screen.blit(head_text, ((ALL_WIDTH - text_width) // 2, 15 + text_height))

    game_rules = {
        'game_rules_p1': [
            'Игра начинается с «СТАРТ». Игроки по очереди бросают кубик',
            'и передвигают фишку согласно выпавшей фигуре. Выигрывает тот,',
            'кто первый приходит на «ФИНИШ». Первым ходит пользователь.'
        ],
        'game_rules_p2': [
            'Если выпала фигура:',
            '1. Пешка – ход вперед на одну клетку.',
            '(если рядом граница, то игрок пропускает ход).',
            '2. Ладья – ходит вперед или назад, вправо или влево на 1 клетку.',
            '3. Король – ходит в любом направлении на 1 клетку.',
            '4. Слон – ходит по диагонали в любую сторону на 1 клетку.',
            '5. Конь – ходит «буквой Г».',
            '6. Ферзь – ходит в любую сторону на 2 клетки.'
        ],
        'game_rules_p3': [
            'Зелёная клетка – дополнительный ход.',
            'Красная клетка - пропуск хода.'
        ]
    }
    # расстояние между строчками для вывода правил
    BETWEEN_TEXT = 20
    # начальная позиция для game_rules
    position_text = BETWEEN_TEXT * 6
    for value in game_rules.values():
        print_text(value, position_text, BETWEEN_TEXT)
        position_text += BETWEEN_TEXT * (len(value) + 2)

    # блок кнопок
    # BUTTON_TEXTS = ['В меню', 'Выход']
    # Пока не доделала настройки
    BUTTON_TEXTS = ['Выход']
    buttons = Button.create_buttons_horizontally(
        screen, BUTTON_TEXTS, position_text + 50
    )
    button_scenes = {
        # menu_scene: BUTTON_TEXTS[0],
        # main_scene: BUTTON_TEXTS[1]
        main_scene: BUTTON_TEXTS[0]
    }

    rules_game = True
    while rules_game:
        rules_game = handle_events(buttons, button_scenes)


def winning_screne():
    """Выигрыш."""
    # т к файлы названы по формату 'images\mfinish_0001.png', то
    image_sprite = [
        f'images/mfinish_{str(i).zfill(4)}.png' for i in range(1, 18)
    ]
    # Загружаем все изображения сразу
    image_sprite = [pygame.image.load(image) for image in image_sprite]
    # поздравительная анимация
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

    text = ['Ты великолепен!', 'Великолепная игра!', "Молодец!"]
    text_in_screen = font_head.render(random.choice(text), True, FONT_COLOR)
    text_position_y = 600  # по Y подбирала под рисунок
    screen.blit(
        text_in_screen,
        text_in_screen.get_rect(
            center=(screen.get_width() // 2, text_position_y)
        )
    )
    qwestion = font_head.render('Играть ещё?', True, FONT_COLOR)
    text_position_y += 30
    screen.blit(
        qwestion,
        qwestion.get_rect(center=(screen.get_width() // 2, text_position_y))
    )

    BUTTON_TEXTS = ['Да']
    buttons = Button.create_buttons_horizontally(
        screen, BUTTON_TEXTS, text_position_y + 30
    )
    button_scenes = {
        main_scene: BUTTON_TEXTS[0]
    }
    winning = True
    while winning:
        winning = handle_events(buttons, button_scenes)


def settings_screne():
    """Настройки. Статус: В работе"""
    background_menu(BACKGROUND_IMAGE, screen)

    # создаем изображение залоговка c шрифтом font цветом FONT_COLOR
    head_text = font_head.render('Настройки', True, FONT_COLOR)
    text_width, text_height = head_text.get_size()
    # выводим на экран
    screen.blit(head_text, ((ALL_WIDTH - text_width) // 2, 15 + text_height))

    head1_text = font_head_1.render('Уровень сложности', True, FONT_COLOR)
    text_width, text_height = head1_text.get_size()
    screen.blit(
        head1_text,
        ((ALL_WIDTH - text_width) // 2, BETWEEN_HEAD_HEAD_1 + text_height)
    )

    y = BETWEEN_HEAD_HEAD_1 + text_height + BEETWEEN_HEAD_1_TEXT
    BEETWEEN_RADIOBUTTON = 30
    radio_buttons = [
        RadioButton(
            ALL_WIDTH // 2 - 100, 300, 'Легкий',
            font_text, FONT_COLOR),
        RadioButton(
            ALL_WIDTH // 2 - 100,
            y + BEETWEEN_RADIOBUTTON,
            'Обычный', font_text, FONT_COLOR
        )
    ]

    # блок кнопок

    BUTTON_TEXTS = ['Сохранить', 'Сброс']
    buttons = Button.create_buttons_horizontally(screen, BUTTON_TEXTS, 300)
    # Отрисовка всех кнопок
    for button in buttons:
        button.draw(screen)

    # button_scenes = {
    #     main_scene: BUTTON_TEXTS[0],
        # main_scene: BUTTON_TEXTS[1]
    # }
    for radio_button in radio_buttons:
        radio_button.draw(screen)
    pygame.display.update()

    settings = True
    # нажатие кнопок на сцене
    while settings:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                switch_scene(None)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # left mouse button
                    mouse_pos = pygame.mouse.get_pos()
                    for radio_button in radio_buttons:
                        if radio_button.check_click(mouse_pos):
                            for rb in radio_buttons:
                                if rb != radio_button:
                                    rb.is_selected = False
        # перерисовали и обновили
        for radio_button in radio_buttons:
            radio_button.update(screen)
        pygame.display.update()

        # settings = handle_events(buttons, button_scenes, settings) # ?


def loss_screne():
    """Проигрыш."""
    background_menu(BACKGROUND_IMAGE_LOSS, screen)
    BUTTON_TEXTS = ['Играть!']
    buttons = Button.create_buttons_horizontally(screen, BUTTON_TEXTS, 350)
    button_scenes = {
        main_scene: BUTTON_TEXTS[0],
    }
    loss = True
    while loss:
        loss = handle_events(buttons, button_scenes)


if __name__ == '__main__':
    """При запуске сразу открываем игру."""
    switch_scene(main_scene)
    while current_scene is not None:
        current_scene()
