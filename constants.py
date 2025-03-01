FONT_COLOR = (0, 0, 0)      # цвет ТЕКСТА во всём проекте
FONT = 'fonts/verdana.ttf'  # шрифт текста


# цвет фона
BOARD_BACKGROUND_COLOR = (0, 0, 0)   # цвет фона


LINE_COLOR = (69, 73, 78)    # цвет сетки

CELL_NOT_STEP_COLOR = (255, 0, 0)  # цвет ячеек пропуск хода

CELL_DOUBLE_STEP_COLOR = (0, 179, 70)  # цвет ячеек двойной хода

# цвет рамки для ячеек-подсказок, куда можно пойти
HELP_COLOR = (255, 255, 255)

# ИЗОБРАЖЕНИЯ
PLAYER_IMAGE = 'images/green.png'     # игрока
COMP_IMAGE = 'images/myred.png'       # комп
START_IMAGE = 'images/start.png'      # старт
FINISH_IMAGE = 'images/myfinish.png'  # финиш
# стороны кубика
PAWN_IMAGE = 'images/pawn.png'
KING_IMAGE = 'images/king.png'
QUEEN_IMAGE = 'images/queen.png'
BISHOP_IMAGE = 'images/mybishop.png'
KNIGHT_IMAGE = 'images/knight.png'
ROOK_IMAGE = 'images/myrook.png'

DEFAULT_IMAGE = 'images/default.png'

MENU = 'images/menu.png'
# ФОНЫ
BACKGROUND_IMAGE_MAIN = 'images/mfont.png'
BACKGROUND_IMAGE_MENU = 'images/mbackground_image.png'  # фон для окон Меню
# фон для окон Правила игры, настройки
BACKGROUND_IMAGE = 'images/mbackground_image1.png'
BACKGROUND_IMAGE_LOSS = 'images/loss_2.png'  # фон для проигрыша


GRID_SIZE = 70     # размер ячейки - от него и скачем
COUNT_GRID = 10    # количество ячеек
# ширина левой доп части чтоб разместить кубик, текст и "кнопку" меню
LEFT_PANEL = 200
# размер прямоугольника под анимацию кубика
CUBE_WIDTH, CUBE_HEIGHT = 80, 120

BOARD_BORDER_Y = 95  # ширина оконтовки игрового поля
BOARD_BORDER_X_R, BOARD_BORDER_X_L = 92, 98
MENU_WIDTH = MENU_HEIGHT = 30
MENU_BORDER = 10

# игровое поле
BOARD_WIDTH = BOARD_HEIGHT = GRID_SIZE * COUNT_GRID
# размер доски с оконтовкой
SCREEN_WIDTH = BOARD_WIDTH + BOARD_BORDER_X_R + BOARD_BORDER_X_L
SCREEN_HEIGHT = BOARD_HEIGHT + BOARD_BORDER_Y * 2

# координаты "СТАРТ"
STRAT_WIDTH = BOARD_BORDER_X_R
STRAT_HEIGHT = SCREEN_HEIGHT - BOARD_BORDER_Y - GRID_SIZE
# координаты "ФИНИШ"
FINISH_WIDTH = BOARD_WIDTH + BOARD_BORDER_X_R - GRID_SIZE * 3
FINISH_HEIGHT = BOARD_BORDER_Y + GRID_SIZE * 2

ALL_WIDTH = SCREEN_WIDTH + LEFT_PANEL

BETWEEN_HEAD_HEAD_1 = 100
BEETWEEN_HEAD_1_TEXT = 80
COUNT_NOT_STEP = 8
COUNT_DOUBLE_STEP = 3
NAME_PLAY = 'Шахматная игра-бродилка.'

MESSAGE = 'Ходите'
MESSAGE_NOT_STEP = 'Переход хода.'