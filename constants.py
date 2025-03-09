
BACKGROUND_COLOR = (0, 0, 0)           # цвет фона
LINE_COLOR = (69, 73, 78)              # цвет сетки
CELL_NOT_STEP_COLOR = (255, 0, 0)      # цвет ячеек пропуск хода
CELL_DOUBLE_STEP_COLOR = (0, 179, 70)  # цвет ячеек двойной хода
HELP_COLOR = (255, 255, 255)           # цвет рамки куда можно пойти
FOLDER = 'images/'

DEFAULT_IMAGE = FOLDER + 'black.png'
PLAYER_IMAGE = FOLDER + 'green.png'     # фишка игрока
COMP_IMAGE = FOLDER + 'myred.png'       # фишка комп
START_IMAGE = FOLDER + 'start.png'      # старт
FINISH_IMAGE = FOLDER + 'myfinish.png'  # финиш

PAWN_IMAGE = FOLDER + 'pawn.png'        # стороны кубика
KING_IMAGE = FOLDER + 'king.png'
QUEEN_IMAGE = FOLDER + 'queen.png'
BISHOP_IMAGE = FOLDER + 'mybishop.png'
KNIGHT_IMAGE = FOLDER + 'knight.png'
ROOK_IMAGE = FOLDER + 'myrook.png'
CAST = [
    FOLDER + 'myrotation1.png',
    FOLDER + 'myrotation2.png',
    FOLDER + 'myrotation3.png',
    FOLDER + 'myrotation4.png'
]
CUBE_WIDTH, CUBE_HEIGHT = 80, 120       # размер кубика


MENU = FOLDER + 'menu.png'

BACKGROUND_MAIN_SCENE = FOLDER + 'mfont.png'  
BACKGROUND_MENU_SCENE = FOLDER + 'mbackground_menu_scene.png'
BACKGROUND_SCENE = FOLDER + 'mbackground_scene.png'
NAME_RULES_SCENE = 'Правила игры.'

BACKGROUND_LOSS_SCENE = FOLDER + 'loss.png'

ICO_IMAGE = FOLDER + 'logo2.png'

GRID_SIZE = 70       # размер ячейки
COUNT_GRID = 10      # количество ячеек
LEFT_PANEL = 200     # ширина левой доп части для кубика и кнопки меню
BOARD_BORDER_Y = 95  # ширина оконтовки игрового поля
BOARD_BORDER_X_R, BOARD_BORDER_X_L = 92, 98
MENU_WIDTH = MENU_HEIGHT = 30
MENU_BORDER = 10     # расстояние от угла до кнопки меню

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

COUNT_NOT_STEP = 8                     # кол-во ячеек доп хода
COUNT_DOUBLE_STEP = 5                  # кол-во ячеек пропуск хода
TEXT_COLOR = (0, 0, 0)                 # цвет ТЕКСТА во всём проекте
FONT = 'fonts/verdana.ttf'             # шрифт ТЕКСТА
BETWEEN_HEAD_HEAD_1 = 100
BEETWEEN_HEAD_1_TEXT = 80
BETWEEN_TEXT = 20
NAME_PLAY = 'Шахматная игра-бродилка.'
HELP_MESSAGE = 'Ходите'
MESSAGE_NOT_STEP = 'Переход хода'
RULES = [
    [
        'Игра начинается с «СТАРТ». Игроки по очереди бросают кубик',
        'и передвигают фишку согласно выпавшей фигуре. Выигрывает тот,',
        'кто первый приходит на «ФИНИШ». Первым ходит пользователь.'
    ],
    [
        'Если выпала фигура:',
        '1. Пешка – ход вперед на одну клетку.',
        '(если рядом граница, то игрок пропускает ход).',
        '2. Ладья – ходит вперед или назад, вправо или влево на 1 клетку.',
        '3. Король – ходит в любом направлении на 1 клетку.',
        '4. Слон – ходит по диагонали в любую сторону на 1 клетку.',
        '5. Конь – ходит «буквой Г».',
        '6. Ферзь – ходит в любую сторону на 2 клетки.'
    ],
    [
        'Зелёная клетка – дополнительный ход.',
        'Красная клетка - пропуск хода.'
    ]
]

BUTTON_TEXTS_RULES_SCENE = ['Выход']
BUTTON_TEXTS_MENU_SCENE = ['Правила игры', 'Настройки', 'Выход']
BUTTON_TEXTS_LOSS_SCENE = ['Играть!']
BUTTON_TEXTS_WIN_SCENE = ['Да']
TEXTS_LOSS_SCENE = ['Не переживай!', 'Играй и повезёт!']
WIN_TEXTS = ['Ты великолепен!', 'Великолепная игра!', "Молодец!"]
QWESTION_TEXT = 'Играть ещё?'