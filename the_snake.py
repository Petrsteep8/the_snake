"""Модуль, который рандомизирует события."""
from random import choice, randint

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Базовый класс, от которого наследуются другие игровые объекты."""

    def __init__(self):
        """Инициализатор класса GameObject."""
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = None

    def draw(self):
        """Пустой метод."""
        raise NotImplementedError


class Apple(GameObject):
    """Класс, описывающий яблоко и действия с ним."""

    def __init__(self) -> None:
        """Инициализатор класса Apple."""
        super().__init__()
        self.body_color = APPLE_COLOR

    def randomize_position(self, *args):
        """Устанавливает случайное положение яблока на игровом поле."""
        while True:
            new_position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                            randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
            if new_position not in args:
                self.position = new_position
                break

    def draw(self):
        """Отрисовывает яблоко на игровой поверхности."""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс, описывающий змейку и её поведение."""

    def __init__(self) -> None:
        """Инициализатор класса Snake."""
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def get_head_position(self):
        """Метод, который возвращает позицию головы змейки."""
        return self.positions[0]

    def update_direction(self):
        """Метод, который обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Метод, который обновляет позицию змейки."""
        first_coordinate, second_coordinate = self.get_head_position()
        dx, dy = self.direction
        dx *= GRID_SIZE
        dy *= GRID_SIZE
        new_x = (first_coordinate + dx) % SCREEN_WIDTH
        new_y = (second_coordinate + dy) % SCREEN_HEIGHT
        new_coordinates = (new_x, new_y)
        self.positions.insert(0, new_coordinates)
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def self_collided(self):
        """Метод, который проверяет змейку на самоукус."""
        head_position = self.get_head_position()
        for pos in self.positions[1:]:
            if head_position == pos:
                return True
        return False

    def reset(self):
        """Метод, который сбрасывает змейку в начальное состояние."""
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.length = 1
        self.direction = choice([LEFT, RIGHT, DOWN, UP])
        self.next_direction = None
        self.last = None

    def draw(self):
        """Метод, который отрисовывает змейку на экране, затирая след."""
        # Отрисовка головы змейки
        head_rect = pg.Rect(self.get_head_position(), (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, head_rect)
        pg.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


def handle_keys(game_object):
    """Функция, которая обрабатывает события клавиш."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if ((event.key == pg.K_UP or event.key == pg.K_w)
                    and game_object.direction != DOWN):
                game_object.next_direction = UP
            elif ((event.key == pg.K_DOWN or event.key == pg.K_s)
                  and game_object.direction != UP):
                game_object.next_direction = DOWN
            elif ((event.key == pg.K_LEFT or event.key == pg.K_a)
                  and game_object.direction != RIGHT):
                game_object.next_direction = LEFT
            elif ((event.key == pg.K_RIGHT or event.key == pg.K_d)
                  and game_object.direction != LEFT):
                game_object.next_direction = RIGHT


def main():
    """Основной цикл игры."""
    # Инициализация PyGame:
    pg.init()
    apple = Apple()
    snake = Snake()
    apple.randomize_position(snake.positions)
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.self_collided():
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
            apple.randomize_position(snake.positions)

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)

        apple.draw()
        snake.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
