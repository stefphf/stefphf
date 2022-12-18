import typing as tp
from random import randint

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
            self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10
    ) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

    def draw_lines(self) -> None:
        """Отрисовать сетку"""
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def run(self) -> None:
        """Запустить игру"""
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        # Создание списка клеток
        self.grid = self.create_grid(randomize=True)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.draw_lines()

            # Отрисовка списка клеток
            self.draw_grid()
            # Выполнение одного шага игры (обновление состояния ячеек)
            self.get_next_generation()

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def create_grid(self, randomize: bool = False) -> Grid:
        """
        Создание списка клеток.

        Клетка считается живой, если ее значение равно 1, в противном случае клетка
        считается мертвой, то есть, ее значение равно 0.

        Parameters
        ----------
        randomize : bool
            Если значение истина, то создается матрица, где каждая клетка может
            быть равновероятно живой или мертвой, иначе все клетки создаются мертвыми.

        Returns
        ----------
        out : Grid
            Матрица клеток размером `cell_height` х `cell_width`.
        """
        divider = self.cell_width
        if randomize:
            temp_grid = []
            for i in range(self.cell_height * self.cell_width):
                temp_grid.append(randint(0, 1))
            n = self.cell_height
            grid = []
            for i in range(n):
                grid.append(temp_grid[i * divider: (i + 1) * divider])
        else:
            temp_grid = []
            for i in range(self.cell_height * self.cell_width):
                temp_grid.append(0)
            n = self.cell_height
            grid = []
            for i in range(n):
                grid.append(temp_grid[i * divider: (i + 1) * divider])
        return grid

    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        for y in range(self.cell_height):
            for x in range(self.cell_width):
                if self.grid[y][x] == 1:
                    pygame.draw.rect(
                        self.screen,
                        pygame.Color("green"),
                        (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size),
                    )
                else:
                    pygame.draw.rect(
                        self.screen,
                        pygame.Color("white"),
                        (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size),
                    )

    def get_neighbours(self, cell: Cell) -> Cells:
        """
        Вернуть список соседних клеток для клетки `cell`.

        Соседними считаются клетки по горизонтали, вертикали и диагоналям,
        то есть, во всех направлениях.

        Parameters
        ----------
        cell : Cell
            Клетка, для которой необходимо получить список соседей. Клетка
            представлена кортежем, содержащим ее координаты на игровом поле.

        Returns
        ----------
        out : Cells
            Список соседних клеток.
        """
        self.neighbours = []
        y, x = cell
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if (
                        (x + i != x or y + j != y)
                        and (0 <= x + i <= self.cell_width - 1)
                        and (0 <= y + j <= self.cell_height - 1)
                ):
                    neighbour_x = x + i
                    neighbour_y = y + j
                    self.neighbours.append(self.grid[neighbour_y][neighbour_x])
        return self.neighbours

    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток.

        Returns
        ----------
        out : Grid
            Новое поколение клеток.
        """
        self.next_gen = self.create_grid(False)
        for row in range(self.cell_height):
            for col in range(self.cell_width):
                alive_nei = sum(self.get_neighbours((row, col)))
                cell = self.grid[row][col]
                if cell == 1 and (alive_nei == 2 or alive_nei == 3):
                    self.next_gen[row][col] = 1
                if cell == 0 and alive_nei == 3:
                    self.next_gen[row][col] = 1
        return self.next_gen
