import curses
import time

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)
        self.game = life

    def draw_borders(self, screen) -> None:
        """Отобразить рамку."""
        screen.border("|", "|", "-", "-", "+", "+", "+", "+")

    def draw_grid(self, screen) -> None:
        """Отобразить состояние клеток."""
        grid = self.game.curr_generation
        for i in range(len(grid)):
            screen.addstr(i + 1, 1, "".join(map(str, grid[i])).replace("1", "*").replace("0", " "))

    def run(self) -> None:
        screen = curses.initscr()
        screen.nodelay(True)
        screen.resize(self.game.rows + 2, self.game.cols + 2)
        self.draw_borders(screen)
        while screen.getch() != ord("q"):
            self.draw_grid(screen)
            self.life.step()
            screen.refresh()
            time.sleep(0.1)
        curses.endwin()


game = GameOfLife((24, 32))
ui = Console(game)
ui.run()