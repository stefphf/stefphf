import pygame
from life import GameOfLife
from ui import UI


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        super().__init__(life)
        self.game = life
        self.cell_size = cell_size
        self.height = cell_size * life.rows
        self.width = cell_size * life.cols
        self.screen_size = cell_size * life.cols, cell_size * life.rows
        self.max_generations = life.max_generations
        self.screen = pygame.display.set_mode(self.screen_size)
        self.cell_height = life.rows
        self.cell_width = life.cols
        self.speed = speed

    def draw_lines(self) -> None:
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def draw_grid(self) -> None:
        for y in range(self.cell_height):
            for x in range(self.cell_width):
                if self.game.curr_generation[y][x] == 1:
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

    def run(self) -> None:
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))
        running = True
        paused = False
        while self.game.is_changing and self.game.is_max_generations_exceeded and running:
            if not paused:
                self.game.step()
                self.draw_grid()
                self.draw_lines()
                pygame.display.flip()
                clock.tick(self.speed)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        paused = not paused
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        pos = pygame.mouse.get_pos()
                        col = pos[0] // self.cell_size
                        row = pos[1] // self.cell_size
                        self.game.curr_generation[row][col] = 1
                        pygame.display.update()
                    self.draw_grid()
                    self.draw_lines()
                    pygame.display.flip()
                    clock.tick(self.speed)
        pygame.quit()
