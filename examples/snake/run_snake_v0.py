
import time
import snake


def clean_list_repr(iterable):
    return "\n".join(['| %3i' % each for each in iterable])


if __name__ == "__main__":

    env = snake.make("Snake-v0")

    games = 1
    results = dict()

    start = time.time()
    for _ in range(games):
        env.reset()
        done = False
        steps = 0
        total_reward = 0
        while not done:
            env.render()
            obs, reward, done, info = env.step(env.action_space.sample())
            steps += 1
            total_reward += reward

        results[steps] = total_reward
        print("\n\n GAME OVER \n\n")

    result_steps = sorted(results.keys(), reverse=True)[:10]
    result_points = sorted(results.values(), reverse=True)[:10]

    print(f"Run {games} games in {round(time.time() - start, 2)}s\n"
          f"Steps: {'%3i' % sum(list(results.keys()))}\n"
          f"Points: {'%3i' % sum(list(results.values()))}\n\n"
          f"Top 10 steps:\n{clean_list_repr(result_steps)}\n\n"
          f"Top 10 points:\n{clean_list_repr(result_points)}")
