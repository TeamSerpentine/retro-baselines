

from snake.games.base_game import SnakeGame
from snake.boards.classic import Board
from snake.displays.console import Console


class Snake(SnakeGame):
    """
        Classic snake game with only console output. But the console output
        is created using unicode. (this leads to a slightly more fancy
        game layout.
    """
    def __init__(self):
        board = Board()
        render = Console()
        super().__init__(board, render)

    def obs(self):
        obs = self.board._get_obs(attribute="text_fancy")
        return "\n".join(map(str, ["".join(row.tolist() )for row in obs]))
