"""План-прехват:
1. Отрисовка поля и фишек
2. Бросок кубика, отрисовка полей-подсказок, куда может ходить пользователь
3. Ход пользователя
4. Бросок кубика, ход компьютора
5. Виксация выигрыша, фанфары для пользователя (пока совсем нет)
...
7. Мобильная версия
"""
from random import randint
import pygame


# функция для подготовки модулей pygame к работе
pygame.init()
# вывод текста-подсказок
pygame.font.init()
# для вращения кубика
clock = pygame.time.Clock()
# задаем шрифт для подсказок
font = pygame.font.SysFont('couriernew', 16)

# размер ячейки - от него и скачем
GRID_SIZE = 70
# количество ячеек
COUNT_GRID = 10

# задаем размер экрана
SCREEN_WIDTH, SCREEN_HEIGHT = GRID_SIZE * COUNT_GRID, GRID_SIZE * COUNT_GRID,
# ширина левой доп части чтоб разместить кубик и подсказки
LEFT_PANEL = 200

# цвет фона
BOARD_BACKGROUND_COLOR = (0, 0, 0)
# цвет сетки
LINE_COLOR = (69, 73, 78)
# цвет ячеек пропуск хода
CELL_NOT_STEP_COLOR = (255, 0, 0)
# цвет ячеек двойной хода
CELL_DOUBLE_STEP_COLOR = (0, 179, 70)
# цвет рамки для ячеек-подсказок, куда можно пойти
HELP_COLOR = (255, 255, 255)
# картинки фишек
PLAYER_IMAGE = 'images\green.png'
COMP_IMAGE = 'images\myred.png'
# картинки ячеек старт, финиш
START_IMAGE = 'images\start.png'
FINISH_IMAGE = 'images\myfinish.png'
# картинки куба
PAWN_IMAGE = 'images\pawn.png'
KING_IMAGE = 'images\king.png'
QUEEN_IMAGE = 'images\queen.png'
BISHOP_IMAGE = 'images\mybishop.png'
KNIGHT_IMAGE = 'images\knight.png'
ROOK_IMAGE = 'images\myrook.png'
DEFAULT_IMAGE = 'images\default.png'

REWARD_IMAGE = 'images\myreward.png'

# координаты поля "СТАРТ"
STRAT_WIDTH, STRAT_HEIGHT = 0, SCREEN_HEIGHT - GRID_SIZE
# координаты поля "ФИНИШ" справа верх, но не самый угол
FINISH_WIDTH, FINISH_HEIGHT = SCREEN_WIDTH - GRID_SIZE * 3, GRID_SIZE * 2
# размер прямоугольника под кубик
CUBE_WIDTH, CUBE_HEIGHT = 80, 120
# Список занятых ячейк: старт, финиш и др. чтоб ячейки не накладывались
used_cells = [(STRAT_WIDTH, STRAT_HEIGHT), (FINISH_WIDTH, FINISH_HEIGHT)]

# Задаем экран для спрайтов
screen = pygame.display.set_mode((SCREEN_WIDTH + LEFT_PANEL, SCREEN_HEIGHT))
pygame.display.set_caption(
        '"Шахматная головоломка". Игра-бродилка.'
    )


class GameObject:
    """Основной класс для ячеек с доп функцией."""

    def __init__(self, color=None):
        # количество особенных полей:
        self.count = 0
        self.color = color
        self.positions = []
        self.general_position()

    def general_position(self):
        """Задаем случайное положение."""
        while len(self.positions) < self.count:
            position = self.randomize_position()
            if position not in used_cells:
                # чтоб ячейки не накладвались друг на друга, сразу добавим к занятым
                list.append(used_cells, position)
                list.append(self.positions, position)

    def draw(self):
        """Рисуем на экране."""
        for self.position in self.positions:
            self.draw_cell()

    def draw_cell(self):
        """Закрашиваем ячейку."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.color, rect)
        pygame.draw.rect(screen, LINE_COLOR, rect, 1)

    def randomize_position(self):
        """Вычисляем случайное положение ячейки."""
        x = randint(0, COUNT_GRID - 1) * GRID_SIZE
        y = randint(0, COUNT_GRID - 1) * GRID_SIZE
        return (x, y)


class CellNotStep(GameObject):
    """Ячейки пропуск хода."""

    def __init__(self):
        super().__init__()
        # количество полей пропуск хода:
        self.count = 3
        self.color = CELL_NOT_STEP_COLOR
        self.positions = []
        self.general_position()


class CellDoubleStep(GameObject):
    """Ячейки дополнительный ход."""

    def __init__(self):
        super().__init__()
        # количество полей дополнительного хода:
        self.count = 3
        self.color = CELL_DOUBLE_STEP_COLOR
        self.positions = []
        self.general_position()


class CellHelp():
    """Поля-подсказки, куда можно ходить."""
    def __init__(self):
        self.positions = []

    def into_field(self, x, y):
        """Если координаты внутри поля, то сохраняем."""
        if 0 <= x < SCREEN_WIDTH and 0 <= y < SCREEN_HEIGHT:
            list.append(self.positions, (x, y))

    def get_correct_steps(self, step_x, step_y, *player_position):
        self.into_field(
            player_position[0] + GRID_SIZE * step_x,
            player_position[1] + GRID_SIZE * step_y
        )

    def get_position(self, value, position):
        """Позиции полей куда можно пойти от значения кубика."""
        # print('начальное поле игрока', position)
        if value == 1:
            # Пешка – ход вверх на одну клетку.
            self.get_correct_steps(0, -1, *position)
        elif value == 2:
            # Ладья – ходит вверх или низ, или вправо, или влево на 2 клетки.
            self.get_correct_steps(0, -2, *position)            # вверх
            self.get_correct_steps(0, 2, *position)             # вниз
            self.get_correct_steps(2, 0, *position)             # вправо
            self.get_correct_steps(-2, 0, *position)            # влево
        elif value == 3:
            # Король – ходит в любом направлении на 1 клетку.
            self.get_correct_steps(0, -1, *position)            # вверх
            self.get_correct_steps(0, 1, *position)             # вниз
            self.get_correct_steps(1, 0, *position)             # вправо
            self.get_correct_steps(-1, 0, *position)            # влево
            self.get_correct_steps(1, -1, *position)            # вправо по диагонали вверх
            self.get_correct_steps(1, 1, *position)             # вправо по диагонали вниз
            self.get_correct_steps(-1, 1, *position)            # влево по диагонали вниз
            self.get_correct_steps(-1, -1, *position)           # влево по диагонали вверх
        elif value == 4:
            # Слон – ходит по диагонали в любую сторону на 2 клетки.
            self.get_correct_steps(2, -2, *position)            # вправо по диагонали вверх
            self.get_correct_steps(2, 2, *position)             # вправо по диагонали вниз
            self.get_correct_steps(-2, 2, *position)            # влево по диагонали вниз
            self.get_correct_steps(-2, -2, *position)            # влево по диагонали вверх
        elif value == 5:
            # Конь – «буквой Г».
            self.get_correct_steps(2, 1, *position)             # вправо вниз
            self.get_correct_steps(2, -1, *position)            # вправо вверх
            self.get_correct_steps(-1, -2, *position)           # вверх
            self.get_correct_steps(1, -2, *position)
            self.get_correct_steps(-1, 2, *position)            # вниз
            self.get_correct_steps(1, 2, *position)
            self.get_correct_steps(-2, 1, *position)            # влево
            self.get_correct_steps(-2, -1, *position)
        else:
            # value == 6: Ферзь – ходит в любую сторону на 2 клетки.
            self.get_correct_steps(0, -2, *position)            # вверх
            self.get_correct_steps(0, 2, *position)             # вниз
            self.get_correct_steps(2, 0, *position)             # вправо
            self.get_correct_steps(-2, 0, *position)            # влево
            self.get_correct_steps(2, -2, *position)            # вправо по диагонали вверх
            self.get_correct_steps(2, 2, *position)             # вправо по диагонали вниз
            self.get_correct_steps(-2, 2, *position)            # влево по диагонали вниз
            self.get_correct_steps(-2, -2, *position)           # влево по диагонали вверх

    def draw(self, color):
        """Для каждой ячейки, куда может пойти пользователь вызываем отрисовку."""
        for self.position in self.positions:
            self.draw_cell(color)

    def draw_cell(self, color):
        """Бордер для ячеки, куда может пойти пользователь."""
        rect = pygame.Rect(self.position, (GRID_SIZE+1, GRID_SIZE+1))
        pygame.draw.rect(screen, color, rect, 1)


class Cube(pygame.sprite.Sprite):
    """Кубик"""
    def __init__(self, filename=DEFAULT_IMAGE):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert_alpha()
        self.image = pygame.transform.scale(self.image, (CUBE_WIDTH, CUBE_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH + (LEFT_PANEL - CUBE_WIDTH) // 2
        self.rect.y = (SCREEN_HEIGHT - CUBE_HEIGHT) // 2

    def cast(self):
        image_sprite = [pygame.image.load('images\myrotation1.png'),
                        pygame.image.load('images\myrotation2.png'),
                        pygame.image.load('images\myrotation3.png'),
                        pygame.image.load('images\myrotation4.png'),
                        pygame.image.load('images\myrotation1.png'),
                        pygame.image.load('images\myrotation2.png'),
                        pygame.image.load('images\myrotation3.png'),
                        pygame.image.load('images\myrotation4.png'),
                        pygame.image.load('images\myrotation1.png')
                        ]
        y_step = [-20, -40, -60, -80, -100, -80, -60, -40, -20]

        i = 0
        count_images = len(image_sprite)
        # крутим куб
        while i < count_images:
            # очистили
            self.reset()
            # выводим текст-подсказку ЛИШНЯЯ
            # text = font.render('Бросаем кубик...', True, (255, 255, 255))
            # screen.blit(text, (self.rect.x - 40, self.rect.y - 25))
            image = image_sprite[i]
            image = pygame.transform.scale(image, (CUBE_WIDTH, CUBE_HEIGHT))
            screen.blit(image, (self.rect.x, self.rect.y+y_step[i]))
            pygame.display.update()
            clock.tick(15)
            i += 1

    def draw(self, filename, message):
        # закрасили
        player = pygame.Rect((self.rect.x - 40, self.rect.y - 25), (CUBE_WIDTH + 100, CUBE_HEIGHT + 25))
        pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, player)

        text = font.render(message, True, (255, 255, 255))
        # выводим текст-подсказку
        screen.blit(text, (self.rect.x - 40, self.rect.y - 25))
        # отрисовали нужное
        self.__init__(filename)

    def count(self, message):
        # 6 сторон
        values = {1: PAWN_IMAGE,     # Пешка
                  2: ROOK_IMAGE,     # Ладья
                  3: KING_IMAGE,     # Король
                  4: BISHOP_IMAGE,   # Слон
                  5: KNIGHT_IMAGE,   # Конь
                  6: QUEEN_IMAGE,    # Ферзь
                  }
        key = randint(1, 6)
        self.cast()
        self.draw(values[key], message)
        return key

    def reset(self):
        # закрасили всю левую часть
        player = pygame.Rect((SCREEN_WIDTH + 1, 0), (LEFT_PANEL, SCREEN_HEIGHT))
        pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, player)


class Player(pygame.sprite.Sprite):
    """Фишки"""
    def __init__(self, filename=DEFAULT_IMAGE):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert_alpha()
        self.image = pygame.transform.scale(self.image, (GRID_SIZE, GRID_SIZE))
        # Команда get_rect() оценивает изображение image и высчитывает прямоугольник, 
        # способный окружить его. Этот прямоугольник можно использовать для размещения спрайта в любом месте.
        self.rect = self.image.get_rect()
        self.rect.x = STRAT_WIDTH
        self.rect.y = STRAT_HEIGHT
        self.position = (self.rect.x, self.rect.y)
        self.double_step = False


# class Reward(pygame.sprite.Sprite):
#     """Кубок"""
#     def __init__(self, filename=REWARD_IMAGE):
#         pygame.sprite.Sprite.__init__(self)
#         self.image = pygame.image.load(filename).convert_alpha()
#         # self.image = pygame.transform.scale(self.image, (GRID_SIZE, GRID_SIZE))
#         # Команда get_rect() оценивает изображение image и высчитывает прямоугольник, 
#         # способный окружить его. Этот прямоугольник можно использовать для размещения спрайта в любом месте.
#         self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT))


def finish_window():
    bg = pygame.image.load('images\pozdrav.png')
    bg = pygame.transform.scale(bg, (SCREEN_WIDTH + LEFT_PANEL, SCREEN_HEIGHT))
    screen.blit(bg, (0, 0))
    # clock.tick(1)


def draw_cell(image, position):
    """картинки СТАРТ и ФИНИШ"""
    # .convert() - переводит формат кодирования пикселей поверхности в формат
    # кодирования это ускоряет отрисовку поверхностей.
    # картинка должна помещаться в GRID_SIZE - 2, чтоб сетка была видна хорошо
    scale = pygame.transform.scale(pygame.image.load(image).convert(), (GRID_SIZE-2, GRID_SIZE-2))
    screen.blit(scale, position)


def draw_field():
    """Игровое поле: ячейки, СТАРТ, ФИНИШ"""
    for i in range(0, COUNT_GRID+1):
        pygame.draw.line(screen, LINE_COLOR, (GRID_SIZE * i, 0), (GRID_SIZE * i, SCREEN_HEIGHT), width=1)
        pygame.draw.line(screen, LINE_COLOR, (0, GRID_SIZE * i), (SCREEN_WIDTH, GRID_SIZE * i), width=1)

    # рисуем поле "СТАРТ" левый нижний угол
    draw_cell(START_IMAGE, (STRAT_WIDTH, STRAT_HEIGHT))
    # рисуем поле "ФИНИШ" вправо верх, не угол
    # +2 - чтоб сетка была видна хорошо
    draw_cell(FINISH_IMAGE, (FINISH_WIDTH + 2, FINISH_HEIGHT + 2))


def handle_keys(game_object):
    """Обрабатывает нажатия клавиш."""
    global speed
    # pygame.event.get(). Этот вызов очищает очередь событий. 
    # Если вы не вызовете его, сообщения от операционной системы начнут накапливаться, и ваша игра станет неотзывчивой.
    for event in pygame.event.get():
        # если закрыли окно - выходим
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            # левая клавиши мыши
            if event.button == 1:
                # сюда хочет пользоваьель
                return event.pos


def can_step(mouse_position, good_positions):
    """Проверяем может ли пользователь ходить на то поле, накоторое он нажал."""
    mouse_x, mouse_y = mouse_position
    # print('курсор', mouse_x, mouse_y)
    for position in good_positions:
        good_x, good_y = position
        if good_x <= mouse_x <= good_x + GRID_SIZE and good_y <= mouse_y <= good_y + GRID_SIZE:
            return (good_x, good_y)
    # кликнул туда, куда ходить не может
    return (1000, 1000)


def double_step(game_object, cell_double_step):
    """Проверка на дополнительный ход."""
    if game_object.position in cell_double_step.positions:
        print('Ещё один ход.')
        game_object.double_step = True
    else:
        game_object.double_step = False


def reset(position, color=BOARD_BACKGROUND_COLOR):
    """Окрашиваем ячейку с которой уходим в её цвет."""
    cell = pygame.Rect(position, (GRID_SIZE+1, GRID_SIZE+1))
    pygame.draw.rect(screen, color, cell)
    pygame.draw.rect(screen, LINE_COLOR, cell, 1)


def get_reset(game_object1, game_object2, cell_double_steps, cell_not_steps):
    # стираем старую фишку и возвращаем ячейке нужный цвет
    if game_object1.position == (STRAT_WIDTH, STRAT_HEIGHT):
        # если ушли с поля "СТАРТ"
        draw_cell(START_IMAGE, (STRAT_WIDTH, STRAT_HEIGHT))
    elif game_object1.position in cell_double_steps:
        reset(game_object1.position, CELL_DOUBLE_STEP_COLOR)
    elif game_object1.position in cell_not_steps:
        reset(game_object1.position, CELL_NOT_STEP_COLOR)
    else:
        reset(game_object1.position)
    # если фишки стояли вместе
    if game_object1.position == game_object2.position:
        # перерисовать фишку компа, чтоб не стерлась
        screen.blit(game_object2.image, game_object2.position)


def draw_together(game_object, distance):
    x, y = game_object.position
    screen.blit(game_object.image, (x + distance, y))


def main():
    draw_field()
    cell_not_step = CellNotStep()
    cell_double_step = CellDoubleStep()
    cube = Cube(DEFAULT_IMAGE)
    player = Player(PLAYER_IMAGE)
    comp = Player(COMP_IMAGE)
    cell_help = CellHelp()
    # создаем ячейки с особенными полями
    cell_not_step.draw()
    cell_double_step.draw()
    # расстановка двух фишек на старт
    draw_together(player, 18)
    draw_together(comp, -18)

    end_play = False
    while not end_play:
        if not comp.double_step:
            # ХОД ПОЛЬЗОВАТЕЛЯ
            # бросили кубик
            value = cube.count('Ходите')
            # отразили на экране
            screen.blit(cube.image, cube.rect)
            # ОТРИСОВКА НАЧАЛА ИГРЫ: фишки на старте + кубик
            pygame.display.flip()
            # находим поля куда можно пойти
            cell_help.get_position(value, player.position)
            # если есть куда идти
            if cell_help.positions != []:
                # рамками - ячейки куда можно пойти
                cell_help.draw(HELP_COLOR)
                # print('подсветка полей пользователя', cell_help.positions)
                # отрисовали на экране
                pygame.display.flip()

                mouse_position = None
                # заведомо ложные координаты
                new_position = (1000, 1000)
                # ждем пока пользователь кликнет мышью в правильной ячейке
                while mouse_position is None or new_position == (1000, 1000):
                    mouse_position = handle_keys(player)
                    # проверяем а туда ли нажал?
                    if mouse_position is not None:
                        new_position = can_step(mouse_position, cell_help.positions)

                # стираем старую фишку и возвращаем ячейке нужный цвет
                get_reset(player, comp, cell_double_step.positions, cell_not_step.positions)
                # задаем новую позицию
                player.position = new_position
                # рисуем фишки на новом месте
                if player.position == comp.position:
                    # убираем фишку, что там была
                    reset(player.position)
                    # рисуем фишки вместе
                    draw_together(player, 18)
                    draw_together(comp, -18)
                else:
                    # рисуем фишку на новом месте
                    screen.blit(player.image, new_position)
                # скрываем подсказки
                cell_help.draw(LINE_COLOR)
                # подсказки обнулили
                cell_help.positions = []
                pygame.display.flip()
                # проверка на выигрыш:
                if player.position == (FINISH_WIDTH, FINISH_HEIGHT):
                    print('Выигрыш. Фанфары и фейерверки!')
                    end_play = True
                    
                # проверка ячеки на дополнительный ход
                double_step(player, cell_double_step)

                # если ячека пропуск хода  !!!!!!!!!!!!!СДЕЛАТЬ
            else:
                # Если пусто подсказках - то никуда не ходит. Например: рядом граница и ходить не куда дальше.
                # ПРИДУМАТЬ В КАК СООБЩАТЬ
                print('Переход хода.')
     
        # если у игрока ещё один ход, то комп в пролете:
        if not player.double_step and not end_play:
            # ХОД КОМПА       
            # бросили кубик для компа
            value = cube.count('Ход компа')
            # отразили на экране
            screen.blit(cube.image, cube.rect)
            # На Экран: новое значение кубика, нет подсказок
            pygame.display.flip()
            # определяем на какие поля можем сходить
            cell_help.get_position(value, comp.position)
            if cell_help.positions != []:
                # УРОВЕНЬ: дурак - выбор случайный
                select_position = randint(0, len(cell_help.positions)-1)
                # стираем старую фишку и возвращаем ячейке нужный цвет
                # print('позиции компа', cell_help.positions)
                get_reset(comp, player, cell_double_step.positions, cell_not_step.positions)
                # задаем новое положение
                comp.position = cell_help.positions[select_position]
                if player.position == comp.position:
                    # убираем фишку, что там была
                    reset(player.position)
                    # рисуем фишки вместе
                    draw_together(player, 18)
                    draw_together(comp, -18)
                else:
                    # перерисовываем фишку компа
                    screen.blit(comp.image, comp.position)
                # подсказки обнулили
                cell_help.positions = []
            else:
                # А если пусто подсказках - то пропуск хода
                print('Пропуск хода компа.')
            # проверка на выигрыш:
            if comp.position == (FINISH_WIDTH, FINISH_HEIGHT):
                # должно быть типа этого
                print('Вы проиграли. Хотите сыграть еще раз?')
                # но пока конец игры
                end_play = True
            # проверка ячеки на дополнительный ход
            double_step(comp, cell_double_step)

        # НАЧАЛО СЛЕДУЮЩЕГО ХОДА ПОЛЬЗОВАТЕЛЯ


if __name__ == '__main__':
    main()