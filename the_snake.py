"""Игра «Изгиб Питона»."""

from random import choice

import pygame

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
ALL_CELLS = {
    (x * GRID_SIZE, y * GRID_SIZE)
    for x in range(GRID_WIDTH)
    for y in range(GRID_HEIGHT)
}

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
KEY_DIRECTIONS = {
    pygame.K_UP: UP, pygame.K_DOWN: DOWN,
    pygame.K_LEFT: LEFT, pygame.K_RIGHT: RIGHT,
}

BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)
SPEED = 20

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Змейка')
clock = pygame.time.Clock()


class GameObject:
    """Базовый объект игрового поля."""

    def __init__(self, body_color=None):
        """Задаёт цвет объекта и помещает его в центр поля."""
        self.position = CENTER
        self.body_color = body_color

    def draw(self):
        """Отрисовывает объект на игровом поле."""
        pass

    def draw_cell(self, position):
        """Закрашивает одну клетку и рисует её границу."""
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Яблоко, которое появляется в свободной клетке."""

    def __init__(self, occupied=()):
        """Выбирает начальное положение яблока."""
        super().__init__(APPLE_COLOR)
        self.randomize_position(occupied)

    def randomize_position(self, occupied=()):
        """Переносит яблоко в случайную свободную клетку."""
        self.position = choice(tuple(ALL_CELLS.difference(occupied)))

    def draw(self):
        """Рисует яблоко."""
        self.draw_cell(self.position)


class Snake(GameObject):
    """Змейка с головой в начале списка сегментов."""

    def __init__(self):
        """Создаёт змейку, ползущую вправо."""
        super().__init__(SNAKE_COLOR)
        self.reset(RIGHT)

    def reset(self, direction=None):
        """Возвращает змейку в центр и задаёт направление движения."""
        self.length = 1
        self.positions = [CENTER]
        self.direction = direction or choice((UP, DOWN, LEFT, RIGHT))
        self.next_direction = None
        self.last = None

    def get_head_position(self):
        """Возвращает координаты головы."""
        return self.positions[0]

    def update_direction(self):
        """Применяет поворот перед следующим шагом."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self, apple_position=None):
        """Передвигает голову и сохраняет хвост при поедании яблока."""
        x, y = self.get_head_position()
        dx, dy = self.direction
        head = ((x + dx * GRID_SIZE) % SCREEN_WIDTH,
                (y + dy * GRID_SIZE) % SCREEN_HEIGHT)
        self.positions.insert(0, head)
        if head == apple_position:
            self.length += 1
        self.last = None
        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    def draw(self):
        """Стирает освободившуюся клетку и рисует голову."""
        if self.last is not None:
            screen.fill(BOARD_BACKGROUND_COLOR,
                        pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE)))
        self.draw_cell(self.get_head_position())


def handle_keys(game_object):
    """Обрабатывает стрелки, Escape и закрытие окна."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (
            event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
        ):
            pygame.quit()
            raise SystemExit
        if event.type == pygame.KEYDOWN:
            direction = KEY_DIRECTIONS.get(event.key)
            dx, dy = game_object.direction
            if direction and direction != (-dx, -dy):
                game_object.next_direction = direction


def main():
    """Запускает игру и обновляет поле после каждого шага."""
    pygame.init()
    snake = Snake()
    apple = Apple(snake.positions)
    screen.fill(BOARD_BACKGROUND_COLOR)
    snake.draw()
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move(apple.position)
        head = snake.get_head_position()
        if head in snake.positions[1:] or snake.length == len(ALL_CELLS):
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
            apple.randomize_position(snake.positions)
        elif head == apple.position:
            apple.randomize_position(snake.positions)
        snake.draw()
        apple.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
