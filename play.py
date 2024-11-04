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
# вывод текста на кубике (хотелось бы что-то красивое, чтоб анимация)
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

# рисуем ПОЛЕ
screen = pygame.display.set_mode((SCREEN_WIDTH + LEFT_PANEL, SCREEN_HEIGHT))
for i in range(1, COUNT_GRID+1):
    pygame.draw.line(screen, LINE_COLOR, (GRID_SIZE * i, 0), (GRID_SIZE * i, SCREEN_HEIGHT), width=1)
    pygame.draw.line(screen, LINE_COLOR, (0, GRID_SIZE * i), (SCREEN_WIDTH, GRID_SIZE * i), width=1)

pygame.display.set_caption(
    '"Шахматная головоломка". Игра-бродилка.'
)

# рисуем поле "СТАРТ"
STRAT_WIDTH, STRAT_HEIGHT = 0, SCREEN_HEIGHT - GRID_SIZE
# .convert() - переводит формат кодирования пикселей поверхности в формат 
# кодирования пикселей главной поверхности. При выполнении игры это ускоряет отрисовку поверхностей.
image = pygame.image.load('images\start.png').convert()
# картинка СТАРТ 300Х300, а должена помещаться в GRID_SIZE:
scale = pygame.transform.scale(image, (GRID_SIZE, GRID_SIZE))
# рисуем поле "ФИНИШ"
...
# отразим на экране
screen.blit(scale, (STRAT_WIDTH, STRAT_HEIGHT))



class GameObject:
    """Основной класс для полей-ячеек с доп функцией."""

    def __init__(self, color=None):
        """пока так, тут руки не дошли."""
        self.body_color = color
        self.position = (
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2
        )

    def draw(self):
        """Метод должен определять, как объект будет
        отрисовываться на экране. По умолчанию — pass.
        """
        pass

    def draw_cell(self):
        """метод отрисовки единственного элемента."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, LINE_COLOR, rect, 1)

    def randomize_position(self):
        """Вычисляем случайное положение элемента."""
        # ДОБАВИТЬ список не возможные ячеек: старт, финиш
        used_cells = [(STRAT_WIDTH, STRAT_HEIGHT)]

        return (
            randint(0, COUNT_GRID - 1) * GRID_SIZE,
            randint(0, COUNT_GRID - 1) * GRID_SIZE
        )


class CellNotStep(GameObject):
    """Ячейки с пропуском хода"""

    def __init__(self):
        super().__init__(color=CELL_NOT_STEP_COLOR)
        # количество полей пропуск хода:
        self.count = 3
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


class CellDoubleStep(GameObject):
    """Ячейки с пропуском хода"""

    def __init__(self):
        super().__init__(color=CELL_DOUBLE_STEP_COLOR)
        # количество полей пропуск хода:
        self.count = 3
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


class CellHelp(GameObject):
    """Поля-подсказки, куда можно ходить"""
    def __init__(self):
        super().__init__(color=None)
        self.positions = []

    def into_playin_field(self, x, y):
        """Если такие координаты возможны, то сохраняем"""
        if 0 <= x < SCREEN_WIDTH and 0 <= y < SCREEN_HEIGHT:
            list.append(self.positions, (x, y))

    def get_up_down(self, player_position, step, direction):
        """ячейки сверху и снизу"""
        position_x, position_y = player_position
        # print('up down', position_x, position_y + GRID_SIZE * step * direction)
        self.into_playin_field(position_x, position_y + GRID_SIZE * step * direction)

    def get_left_right(self, player_position, step, direction):
        """ячейки справа и слева"""
        position_x, position_y = player_position
        # print('left right', position_x + GRID_SIZE * step * direction, position_y)
        self.into_playin_field(position_x + GRID_SIZE * step * direction, position_y)

    def get_diagonal(self, player_position, step, direction):
        """ячейки левая верхняя и правая нижняя"""
        position_x, position_y = player_position
        self.into_playin_field(position_x + GRID_SIZE * step * direction, position_y + GRID_SIZE * step * direction) 

    def get_diagonal_two(self, player_position, step, direction):
        """ячейки левая нижняя и правая верхняя"""
        position_x, position_y = player_position
        self.into_playin_field(position_x + GRID_SIZE * step * direction, position_y - GRID_SIZE * step * direction) 

    def get_position(self, value, player_position):
        """Позиции полей куда можно пойти"""
        print('get_position', player_position)
        if value == 1:
            # Пешка – ход вверх на одну клетку.
            # (если рядом граница, то есть ходить не куда дальше, то играющий пропускает ход).
            self.get_up_down(player_position, 1, -1)
        if value == 2:
            # Ладья – ходит вверх или низ, или вправо, или влево на 2 клетки.
            # вверх
            self.get_up_down(player_position, 2, -1)
            # вниз
            self.get_up_down(player_position, 2, 1)
            # вправо
            self.get_left_right(player_position, 2, 1)
            # влево
            self.get_left_right(player_position, 2, -1)
        if value == 3:
            # Король – ходит в любом направлении на 1 клетку.
            # вверх
            self.get_up_down(player_position, 1, -1)
            # вниз
            self.get_up_down(player_position, 1, 1)
            # вправо
            self.get_left_right(player_position, 1, 1)
            # влево
            self.get_left_right(player_position, 1, -1)
            # вправо по диагонали вверх
            self.get_diagonal_two(player_position, 1, 1)
            # вправо по диагонали вниз
            self.get_diagonal(player_position, 1, 1)
            # влево по диагонали вниз
            self.get_diagonal_two(player_position, 1, -1)
            # влево по диагонали вверх
            self.get_diagonal(player_position, 1, -1)
        if value == 4:
            # Слон – ходит по диагонали в любую сторону на 2 клетки.
            # вправо по диагонали вверх
            self.get_diagonal_two(player_position, 2, 1)
            # вправо по диагонали вниз
            self.get_diagonal(player_position, 2, 1)
            # влево по диагонали вниз
            self.get_diagonal_two(player_position, 2, -1)
            # влево по диагонали вверх
            self.get_diagonal(player_position, 2, -1)

        if value == 5:
            # Конь – «буквой Г».
            # вправо вниз
            position_x, position_y = player_position
            self.into_playin_field(position_x + GRID_SIZE * 3 * 1, position_y + GRID_SIZE * 1 * 1)
            # вправо вверх
            position_x, position_y = player_position
            self.into_playin_field(position_x + GRID_SIZE * 3 * 1, position_y - GRID_SIZE * 1 * 1)
            # вверх
            position_x, position_y = player_position
            self.into_playin_field(position_x - GRID_SIZE * 1 * 1, position_y - GRID_SIZE * 3 * 1)
            self.into_playin_field(position_x + GRID_SIZE * 1 * 1, position_y + GRID_SIZE * 3 * 1)
            # вниз
            # влево  
        if value == 6:
            # Ферзь – ходит в любую сторону на 2 клетки.
            # вверх
            self.get_up_down(player_position, 2, -1)
            # вниз
            self.get_up_down(player_position, 2, 1)
            # вправо
            self.get_left_right(player_position, 2, 1)
            # влево
            self.get_left_right(player_position, 2, -1)
            # вправо по диагонали вверх
            self.get_diagonal_two(player_position, 2, 1)
            # вправо по диагонали вниз
            self.get_diagonal(player_position, 2, 1)
            # влево по диагонали вниз
            self.get_diagonal_two(player_position, 2, -1)
            # влево по диагонали вверх
            self.get_diagonal(player_position, 2, -1)

    def draw(self, color):
        """Для каждой ячейки, куда может пойти пользователь вызываем отрисовку."""
        print(self.positions)
        for self.position in self.positions:
            self.draw_cell(color)

    def draw_cell(self, color):
        """Бордер для ячеки, куда может пойти пользователь."""
        # +1 - так граница "сверху", красивше
        rect = pygame.Rect(self.position, (GRID_SIZE + 1, GRID_SIZE + 1))
        pygame.draw.rect(screen, color, rect, 1)
        # print(self.position)


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
        return randint(1, 6)


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
        # player = pygame.Rect(self.position, (30, 30))
        # pygame.draw.rect(screen, (0, 50, 80), player)
        # image = pygame.Surface([40,80], pygame.SRCALPHA, 32)
        image = pygame.image.load(image_file)
        image = image.convert_alpha()

        # картинка должена помещаться в GRID_SIZE!
        scale = pygame.transform.scale(image, (GRID_SIZE, GRID_SIZE))
        # отразим на экране
        screen.blit(scale, self.position)

    def reset(self):
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


def main():
    cell_not_step = CellNotStep()
    cell_double_step = CellDoubleStep()
    cube = Cube()
    player = Player()
    comp = Player()
    cell_help = CellHelp()
    # рисуем окно для начала игры: все для первого хода пользователя
    cell_not_step.draw()
    cell_double_step.draw()
    # расстановка фишек на старт
    # СДЕЛАТЬ пользователя со смещением, чтоб виден был
    player.draw(PLAYER_IMAGE)
    # пока накладываются: или смещать или картинку менять?
    # comp.position = (
    #         STRAT_WIDTH,
    #         STRAT_HEIGHT
    #     )
    comp.draw(COMP_IMAGE)
    # бросили кубик
    value = cube.count()
    # отразили
    cube.draw(value)
    # ОТРИСОВКА НАЧАЛА ИГРЫ: фишки на старте + кубик
    pygame.display.flip()
    while True:
        # ХОД ПОЛЬЗОВАТЕЛЯ
        # подсветим поля куда можно пойти
        if cell_help.get_position(value, player.position) != []:
            cell_help.draw(HELP_COLOR)
            print('подсветка полей', value, cell_help.positions)
            # отразили красоту
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

            # стираем старую фишк на черном поле.
            player.reset()
            # стираем старую фишку с поля старт
            screen.blit(scale, (STRAT_WIDTH, STRAT_HEIGHT))
            # Туда! задаем новую позицию
            player.position = new_position
            # рисуем новую фишку
            player.draw(PLAYER_IMAGE)
            # скрываем подсказки 
            cell_help.draw(LINE_COLOR)
            # подсказки обнулили
            cell_help.positions = []
            pygame.display.flip()
        else:
            # А если пусто подсказках - то пропуск хода: ПРИДУМАТЬ В КАКОМ ВИДЕ СООБЩАТЬ
            print('Пропуск хода игрока.')
        # проверка на особенность ячейки:
        # если ячека доп ход
        ...
        # если ячека пропуск хода
        ...
        # ХОД КОМПА
        # бросили кубик для компа
        value = cube.count()
        # отразили
        cube.draw(value)
        # На Экран: новое значение кубика, нет подсказок
        pygame.display.flip()
        # ходит комп: определяем на какие поля можем сходить
        # Если есть куда ходить:
        if cell_help.get_position(value, comp.position) != []:
            # УРОВЕНЬ: дурак - выбор случайный
            print(len(cell_help.positions)-1)
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
        cube.draw(value)
        pygame.display.update()


if __name__ == '__main__':
    main()