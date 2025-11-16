from random import choice, randint

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE: int = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
Color = tuple[int, int, int]
Pointer = tuple[int, int]
UP: Pointer = (0, -1)
DOWN: Pointer = (0, 1)
LEFT: Pointer = (-1, 0)
RIGHT: Pointer = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR: Color = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR: Color = (93, 216, 228)

# Цвет яблока
APPLE_COLOR: Color = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR: Color = (0, 255, 0)

# Скорость движения змейки:
SPEED: int = 10

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Описание класса"""

    def __init__(self, body_color: Color = None):
        """Инициализация атрибутов класса GameObject"""
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = body_color

    def draw(self):
        """Отрисовка"""
        pass


class Apple(GameObject):
    """Описание объекта яблоко"""

    def __init__(self, occup_pos: tuple = (), body_color: Color = APPLE_COLOR):
        """Инициализация, случайное положение яблока"""
        super().__init__(body_color=body_color)
        self.randomize_position(occup_pos)

    def randomize_position(self, occup_pos: tuple) -> None:
        """Установить случайное положение яблока"""
        while True:
            new_position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
            )
            if new_position not in occup_pos:
                self.position = new_position
                break

    def draw(self):
        """Отрисовка яблока"""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Описание объекта змейка"""

    def __init__(self, body_color: Color = SNAKE_COLOR):
        """Инициализация атрибутов змейки"""
        super().__init__(body_color=body_color)
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        self.positions = [self.position]
        self.last = None

    def update_direction(self):
        """Обновление направления змейки"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Перемещение змейки"""
        self.update_direction()
        hx, hy = self.get_head_position()
        x, y = self.direction
        new = (
            (hx + x * GRID_SIZE) % SCREEN_WIDTH,
            (hy + y * GRID_SIZE) % SCREEN_HEIGHT
        )
        self.positions.insert(0, new)
        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    def get_head_position(self):
        """Вернуть координаты головы змейки"""
        return self.positions[0]

    def reset(self):
        """Сброс после столкновения"""
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = choice([UP, DOWN, RIGHT, LEFT])
        self.last = None

    def draw(self):
        """Отрисовка змейки"""
        for position in self.positions:
            rect = (pg.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pg.draw.rect(screen, self.body_color, rect)
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)


def handle_keys(game_object):
    """Взаимодействие пользователя со змейкой"""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основная логика игры"""
    pg.init()
    snake = Snake()
    apple = Apple(occup_pos=snake.positions)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.move()
        head_pos = snake.get_head_position()

        if head_pos in snake.positions[1:]:
            snake.reset()

        if head_pos == apple.position:
            snake.length += 1
            apple = Apple(occup_pos=snake.positions)
        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
