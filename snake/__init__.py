from gym.envs.registration import register

register(
    id='Snake-v0',
    entry_point='snake.env:SnakeEnv',
    kwargs=dict(game=id, mode='human', width=32, height=42, scale=5),
    max_episode_steps=100000
)

register(
    id='Snake-v1',
    entry_point='snake.env:SnakeEnv',
    kwargs=dict(game=id, mode='ansi', obs_type='text', width=32, height=42, scale=5),
    max_episode_steps=100000
)

register(
    id='Snake-v2',
    entry_point='snake.env:SnakeEnv',
    kwargs=dict(game=id, mode='ansi_fancy', obs_type='text', width=32, height=42, scale=5),
    max_episode_steps=100000
)

register(
    id='SnakeGen-v0',
    entry_point='snake.env:SnakeEnv',
    kwargs=dict(game=id, mode='gen', obs_type='gen', width=32, height=42, scale=5),
    max_episode_steps=100000
)

register(
    id='SnakeGen-v1',
    entry_point='snake.env:SnakeEnv',
    kwargs=dict(game=id, mode='gen', obs_type='gen', width=16, height=21, scale=10),
    max_episode_steps=100000
)
