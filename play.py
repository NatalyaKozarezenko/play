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
# вывод текста на кубике (хотелось бы что-то красивое типа анимации)
pygame.font.init()

# размер ячейки - от него и скачем
GRID_SIZE = 60
# количество ячеек - для теста, д б больше
COUNT_GRID = 8

# задаем размер экрана (пока так т к не уверена, что квадрат)
SCREEN_WIDTH, SCREEN_HEIGHT = GRID_SIZE * COUNT_GRID, GRID_SIZE * COUNT_GRID,
# ширина левой доп части чтоб разместить кубик и м б что-то ещё, типа подсказок.
LEFT_PANEL = 100

# цвет фона
BOARD_BACKGROUND_COLOR = (0, 0, 0)
# цвет сетки
LINE_COLOR = (69, 73, 78)
# цвет ячеек пропуск хода
CELL_NOT_STEP_COLOR = (255, 0, 0)
# цвет ячеек двойной хода
CELL_DOUBLE_STEP_COLOR = (0, 179, 70)
# цвет рамки для полей-подсказок, куда можно пойти
HELP_COLOR = (255, 255, 255)
# картинки фишек
PLAYER_IMAGE = 'images\green.png'
COMP_IMAGE = 'images\myred.png'
START_IMAGE = 'images\start.png'
FINISH_IMAGE = 'images\myfinish.png'
# координаты поля "СТАРТ"
STRAT_WIDTH, STRAT_HEIGHT = 0, SCREEN_HEIGHT - GRID_SIZE
# координаты поля "ФИНИШ" справа верх, но не самый угол
FINISH_WIDTH, FINISH_HEIGHT = GRID_SIZE * (COUNT_GRID - 2), GRID_SIZE * (COUNT_GRID - 6)

# Задаем экран
screen = pygame.display.set_mode((SCREEN_WIDTH + LEFT_PANEL, SCREEN_HEIGHT))
pygame.display.set_caption(
        '"Шахматная головоломка". Игра-бродилка.'
    )


def draw_cell(image, position):
    """Рисуем картинки в ячейках."""
    # .convert() - переводит формат кодирования пикселей поверхности в формат
    # кодирования это ускоряет отрисовку поверхностей.
    # картинка должна помещаться в GRID_SIZE
    scale = pygame.transform.scale(pygame.image.load(image).convert(), (GRID_SIZE, GRID_SIZE))
    screen.blit(scale, position)


def draw_field():
    """Рисуем ячейки на поле."""
    for i in range(1, COUNT_GRID+1):
        pygame.draw.line(screen, LINE_COLOR, (GRID_SIZE * i, 0), (GRID_SIZE * i, SCREEN_HEIGHT), width=1)
        pygame.draw.line(screen, LINE_COLOR, (0, GRID_SIZE * i), (SCREEN_WIDTH, GRID_SIZE * i), width=1)

    # рисуем поле "СТАРТ" ленвый нижний угол
    draw_cell(START_IMAGE, (STRAT_WIDTH, STRAT_HEIGHT))
    # рисуем поле "ФИНИШ" вправо верх, не угол
    draw_cell(FINISH_IMAGE, (FINISH_WIDTH, FINISH_HEIGHT))


class GameObject:
    """Основной класс для ячеек с доп функцией."""

    def __init__(self, color=None):
        # количество особенных полей:
        self.count = 3
        self.color = color
        self.positions = []
        self.general_position()

    def general_position(self):
        """Задаем случайное положение."""
        for i in range(0, self.count):
            list.append(self.positions, self.randomize_position())

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
        # Исключаем занятые ячейки: старт, финиш чтоб ячейки не накладывались
        used_cells = [(STRAT_WIDTH, STRAT_HEIGHT), (FINISH_WIDTH, FINISH_HEIGHT)]
        for used_cell in used_cells:
            x = randint(0, COUNT_GRID - 1) * GRID_SIZE
            y = randint(0, COUNT_GRID - 1) * GRID_SIZE
            if (x, y) != used_cell:
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
        print('начальное поле игрока', position)
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
            self.get_correct_steps(3, 1, *position)             # вправо вниз
            self.get_correct_steps(3, -1, *position)            # вправо вверх
            self.get_correct_steps(-1, -3, *position)           # вверх
            self.get_correct_steps(1, -3, *position)
            self.get_correct_steps(-1, 3, *position)            # вниз
            self.get_correct_steps( 1, 3, *position)
            self.get_correct_steps(-3, 1, *position)            # влево
            self.get_correct_steps(-3, -1, *position)
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
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, color, rect, 1)


class Cube():
    """Кубик"""
    def __init__(self):
        self.CUBE_X = SCREEN_WIDTH + (LEFT_PANEL - GRID_SIZE) // 2
        self.CUBE_Y = SCREEN_HEIGHT // 2

    def draw(self, value):
        cube = pygame.Rect(self.CUBE_X, self.CUBE_Y, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(screen, (255, 255, 255), cube)
        # задаем шрифт
        font = pygame.font.SysFont('couriernew', 40)
        # временное решение - д б картинки, а не числа
        text = font.render(str(value), True, (0, 0, 0))
        # выводим число с кубика
        screen.blit(text, (self.CUBE_X + 10, self.CUBE_Y + 8))

    def count(self):
        # у кубика 6 сторон
        value = randint(1, 6)
        self.draw(value)
        return value


class Player():
    """Фишки"""
    def __init__(self):
        # сначала фишка на старте
        self.position = (
            STRAT_WIDTH,
            STRAT_HEIGHT
        )

    def draw(self, image_file):
        image_file = image_file
        image = pygame.image.load(image_file)
        image = image.convert_alpha()

        # картинка должена помещаться в GRID_SIZE!
        scale = pygame.transform.scale(image, (GRID_SIZE, GRID_SIZE))
        # отразим на экране
        screen.blit(scale, self.position)

    def reset(self):
        if self.position == (STRAT_WIDTH, STRAT_HEIGHT):
            # если ушли с поля "СТАРТ"
            draw_cell(START_IMAGE, (STRAT_WIDTH, STRAT_HEIGHT))
        else:
            player = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, (0, 0, 0), player)
            pygame.draw.rect(screen, LINE_COLOR, player, 1)


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
    """Проверяем может ли пользователь ходить на то поле, накоторое он нажал"""
    mouse_x, mouse_y = mouse_position
    print('курсор', mouse_x, mouse_y)
    for position in good_positions:
        good_x, good_y = position
        if good_x <= mouse_x <= good_x + GRID_SIZE and good_y <= mouse_y <= good_y + GRID_SIZE:
            return (good_x, good_y)
    # кликнул туда, куда ходить не может
    return (1000, 1000)


def draw_together(self, direction, images):
    x, y = self.position
    # делаем смещение
    self.position = (x + direction, y)
    self.draw(images)
    # возвращаем как было
    self.position = (x, y)


def main():
    draw_field()
    cell_not_step = CellNotStep()
    cell_double_step = CellDoubleStep()
    cube = Cube()
    player = Player()
    comp = Player()
    cell_help = CellHelp()
    # создаем ячейки с особенными полями
    cell_not_step.draw()
    cell_double_step.draw()
    # расстановка двух фишек на старт
    together = True
    if together:
        draw_together(player, 10, PLAYER_IMAGE)
        draw_together(comp, -10, COMP_IMAGE)
    else:
        player.draw(PLAYER_IMAGE)
        comp.draw(COMP_IMAGE)
    # бросили кубик
    value = cube.count()
    # ОТРИСОВКА НАЧАЛА ИГРЫ: фишки на старте + кубик
    pygame.display.flip()
    while True:
        # ХОД ПОЛЬЗОВАТЕЛЯ
        # находим поля куда можно пойти
        if cell_help.get_position(value, player.position) != []:
            cell_help.draw(HELP_COLOR)
            print('подсветка полей', cell_help.positions, 'кубик', value)
            # показали поля куда можно пойти
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
            # стираем старую фишку
            player.reset()
            # Туда! задаем новую позицию
            player.position = new_position
            # рисуем новую фишку
            player.draw(PLAYER_IMAGE)
            # скрываем подсказки
            cell_help.draw(LINE_COLOR)
            # подсказки обнулили
            cell_help.positions = []
            pygame.display.flip()
            # проверка на особенность ячейки:
            # если ячека доп ход
            if player.position in cell_double_step.positions:
                print('Ещё один ход.')
            # если ячека пропуск хода
            if player.position in cell_not_step.positions:
                print('Пропуск хода игрока.')
        else:
            # А если пусто подсказках - то пропуск хода: ПРИДУМАТЬ В КАКОМ ВИДЕ СООБЩАТЬ
            # Например: если рядом граница, то есть ходить не куда дальше
            print('Пропуск хода игрока.')

        # ХОД КОМПА
        # бросили кубик для компа
        value = cube.count()
        # отразили
        # cube.draw(value)
        # На Экран: новое значение кубика, нет подсказок
        pygame.display.flip()
        # ходит комп: определяем на какие поля можем сходить
        # Если есть куда ходить:
        if cell_help.get_position(value, comp.position) != []:
            # УРОВЕНЬ: дурак - выбор случайный
            print('кол-во ячеек-подсказок у компа', len(cell_help.positions)-1, 'кубик', value)
            select_position = randint(0, len(cell_help.positions)-1)
            # стираем фишку
            comp.reset()
            comp.position = cell_help.positions[select_position]
            # перерисовываем фишку компа
            comp.draw(COMP_IMAGE)
            # подсказки обнулили
            cell_help.positions = []
        else:
            # А если пусто подсказках - то пропуск хода
            print('Пропуск хода компа.')
        # НАЧАЛО СЛЕДУЮЩЕГО ХОДА ПОЛЬЗОВАТЕЛЯ
        # бросили кубик для пользователя и отразили
        value = cube.count()
        # cube.draw(value)
        pygame.display.update()


if __name__ == '__main__':
    main()