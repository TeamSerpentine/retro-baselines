
from .objects.constants import DIRECTION_VALID


# Board constants
HEIGHT = 210 // 5
WIDTH = 160 // 5
CHANNELS = 3

MIN_SPAWN_WALL_DISTANCE = 2
DEFAULT_START_SNAKES = 1
DEFAULT_START_APPLES = 1
DEFAULT_START_WALLS = 0
DEFAULT_REWARD_PER_APPLE = 1

# Atari environment constants
GET_ACTION_MEANING = ["NOOP"] + DIRECTION_VALID
ACTION_SPACE = len(GET_ACTION_MEANING)
