import pandas as pd
from site_env import Site
from RL_brain import QLearningTable
import numpy as np



def update():
    episode_counter = 0

    store_episode = []

    store_step = [0]

    store_rewards = [0]

    good_episode = []

    for episode in range(2):
    # while env.counter != 2:
        # initial observation
        record_step = pd.DataFrame(columns= [0,1,2,3], dtype=np.float64)
        step_counter = 0
        successful_counter = 0
        observation = env.reset()
        while True:
            # fresh env
            env.render()
            record_step = record_step.append(
                pd.Series(
                    [0] * 4,
                    index=[0, 1, 2, 3],
                    name=str(observation),
                ))

            # RL choose action based on observation
            action = RL.choose_action(str(observation))
            # RL take action and get next observation and reward
            observation_, reward, done = env.step(action)
            # observation_, reward, done = env.step(env.sample_action())
            # RL learn from this transition
            # print(RL.get_action_value())
            RL.learn(str(observation), action, reward, str(observation_))
            # RL.learn()

            record_step = record_step.append(RL.get_action_value())
            # swap observation
            observation = observation_
            # print(observation)
            step_counter += 1



            # break while loop when end of this episode
            if done:
                # if step_counter <= store_step[-1] and record_step >= store_rewards[-1]:
                #     good_episode.append(record_step)
                store_step.append(step_counter)
                store_rewards.append(reward)
                print('it is end')
                store_episode.append(record_step)
                episode_counter += 1
                print('it is episode: ', episode_counter)
                print('total step are: ', step_counter)
                print('\n')
                break
            if env.counter == 2:
                print('it is end')
                if step_counter <= store_step[-1] and record_step >= store_rewards[-1]:
                    good_episode.append(record_step)
                store_step.append(step_counter)
                store_rewards.append(reward)
                store_episode.append(record_step)
                print('it is a successful round')
                episode_counter += 1
                print('it is episode: ', episode_counter)
                print('total step are: ', step_counter)
                successful_counter += 1
                print('\n')
                break
    print('total success is:', successful_counter)
    print('the good episode',good_episode)
    # end of game
    print('over')
    # print(store_episode)
    env.destroy()

if __name__ == "__main__":
    env = Site()
    RL = QLearningTable(actions=list(range(env.n_actions)))


    env.after(100, update)
    # env.update()
    env.mainloop()