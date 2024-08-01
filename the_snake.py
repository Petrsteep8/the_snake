from random import choice, randint

import pygame

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
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Базовый класс, от которого наследуются другие игровые объекты."""

    def __init__(self):
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = None

    def draw(self):
        """Пустой метод"""
        pass


class Apple(GameObject):
    """Класс, унаследованный от GameObject,
    описывающий яблоко и действия с ним.
    """

    def __init__(self) -> None:
        super().__init__()
        self.body_color = APPLE_COLOR

    def randomize_position(self, snake_positions):
        """Метод, который устанавливает случайное положение яблока на игровом
        поле
        """
        while True:
            new_position = (randint(0, GRID_WIDTH) * GRID_SIZE,
                            randint(0, GRID_HEIGHT) * GRID_SIZE)
            if new_position not in snake_positions:
                self.position = new_position
                break

    def draw(self):
        """Отрисовывает яблоко на игровой поверхности"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс, унаследованный от GameObject, описывающий змейку и её
    поведение.
    """

    def __init__(self) -> None:
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def get_head_position(self):
        """Метод, который возвращает позицию головы змейки"""
        return self.positions[0]

    def update_direction(self):
        """Метод, который обновляет направление движения змейки"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Метод, который обновляет позицию змейки"""
        first_coordinate, second_coordinate = self.get_head_position()
        new_coordinates = (
            (first_coordinate + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH,
            (second_coordinate + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT
        )
        if new_coordinates in self.positions:
            return False
        self.positions.insert(0, new_coordinates)
        if len(self.positions) > self.length:
            self.last = self.positions[-1]
            self.positions.pop()
        return True

    @property
    def reset(self):
        """Метод, который сбрасывает змейку в начальное состояние"""
        self.positions = [(self.position[0], self.position[1])]
        self.length = 1
        self.direction = choice([LEFT, RIGHT, DOWN, UP])
        self.next_direction = None
        self.last = None
        return screen.fill(BOARD_BACKGROUND_COLOR)

    def draw(self):
        """Метод, который отрисовывает змейку на экране, затирая след"""
        for position in self.positions[:-1]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


def handle_keys(game_object):
    """Функция, которая обрабатывает события клавиш."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if ((event.key == pygame.K_UP or event.key == pygame.K_w)
                    and game_object.direction != DOWN):
                game_object.next_direction = UP
            elif ((event.key == pygame.K_DOWN or event.key == pygame.K_s)
                  and game_object.direction != UP):
                game_object.next_direction = DOWN
            elif ((event.key == pygame.K_LEFT or event.key == pygame.K_a)
                  and game_object.direction != RIGHT):
                game_object.next_direction = LEFT
            elif ((event.key == pygame.K_RIGHT or event.key == pygame.K_d)
                  and game_object.direction != LEFT):
                game_object.next_direction = RIGHT


def main():
    """Основной цикл игры."""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    apple = Apple()
    snake = Snake()
    apple.randomize_position(snake.positions)
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        if not snake.move():
            snake.reset
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)
        apple.draw()
        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
