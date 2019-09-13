

# TODO make this more dynamic
from snake.games import snake_gen, snake_v0, snake_v1, snake_v2


def make(game_name):

    names = {
        "snake": snake_v2.Snake,
        "snake-v0": snake_v0.Snake,
        "snake-v1": snake_v1.Snake,
        "snake-v2": snake_v2.Snake,
        "snake-gen": snake_gen.Snake,
    }

    if not names.get(game_name.lower().strip(), None):
        games = "\n\t".join(list(names))
        raise ValueError(f"Game unknown, pick one of the following:\n\t{games}")

    return names.get(game_name.lower().strip())()
