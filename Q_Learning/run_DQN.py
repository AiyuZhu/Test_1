import pandas as pd
from site_env_DQN import Site
import numpy as np
from DQN import DeepQNetwork
import matplotlib.pyplot as plt

def update():
    episode_counter = 0

    good_episode_index = []

    good_episode_steps = []

    good_episode_rewards = []

    record_state = []

    rs_ratio = []

    good_episode_states = []

    successful_counter = 0

    successful_list =[]


    def draw_plot_rs(o_len, o_list) :
        plt.plot(o_len, o_list)
        plt.ylabel('R/S ratio')
        plt.xlabel('successful episode')
        plt.show()

    def draw_plot_success(o_len, o_list) :
        plt.plot(o_len, o_list)
        plt.ylabel('successful time')
        plt.xlabel('training episode')
        plt.show()

    for episode in range(5):
        # initial environment
        step_counter = 0
        observation = env.reset()
        while True:
            # fresh env
            env.render()

            # RL choose action based on observation
            action = RL.choose_action(observation)
            # RL take action and get next observation and reward
            observation_, reward, done = env.step(action)
            # observation_, reward, done = env.step(env.sample_action())
            # RL learn from this transition
            # print(RL.get_action_value())
            RL.store_transition(observation, action, reward, observation_)
            RL.learn()
            record_state.append(observation)

            # record_step = record_step.append(RL.get_action_value())
            # swap observation
            observation = observation_
            # print(observation)
            step_counter += 1



            # break while loop when end of this episode
            if done and env.counter !=1:
                # if step_counter <= good_episode_steps[-1] and record_step >= good_episode_rewards[-1]:
                #     good_episode.append(record_step)
                # good_episode_steps.append(step_counter)
                # good_episode_rewards.append(reward)
                episode_counter += 1
                # record successful times
                successful_list.append(step_counter)
                print('it is end')
                print('it is episode: ', episode_counter)
                print('total step are: ', step_counter)
                record_state = []
                print('\n')
                break
            elif env.counter == 1:
                episode_counter += 1
                successful_counter += 1
                successful_list.append(successful_counter)
                print('it is end')
                print('it is a successful round!')
                print('it is episode: ', episode_counter)
                print('total step are: ', step_counter)
                if len(good_episode_steps)==0 and len(good_episode_rewards) == 0:
                    good_episode_states.append(record_state)
                    good_episode_steps.append(step_counter)
                    good_episode_rewards.append(reward)
                    good_episode_index.append(episode_counter)
                    rs_ratio.append(reward/step_counter)
                    print("it is the first successful episode!")
                elif step_counter <= good_episode_steps[-1]:
                    good_episode_states.append(record_state)
                    good_episode_steps.append(step_counter)
                    good_episode_rewards.append(reward)
                    good_episode_index.append(episode_counter)
                    rs_ratio.append(reward/step_counter)
                    print("it is a better round!")
                record_state = []
                print('\n')
                break
    data = {"Total rewards":good_episode_rewards,
            "Total steps":good_episode_steps,
            "Total R/S ratio":rs_ratio,
            "Total states record":good_episode_states
    }
    print(data)
    useful_result = pd.DataFrame(data,index=good_episode_index)
    writer = pd.ExcelWriter('/Users/pandzay/Desktop/result.xlsx')
    useful_result.to_excel(writer, sheet_name="No.1")
    writer.save()
    print('total successful episode is:', successful_counter)
    print(useful_result.drop(["Total states record"], axis=1))
    best_epsiode = useful_result.sort_values(["Total steps"], ascending=True)
    print("The best process is", best_epsiode.iat[0,3])
    RL.plot_cost()
    draw_plot_rs(np.arange(len(rs_ratio)),rs_ratio)
    draw_plot_success(np.arange(len(successful_list)),successful_list)





    # end of game
    print('over')
    # print(store_episode)
    # env.destroy()

if __name__ == "__main__":
    env = Site()
    RL = DeepQNetwork(4,2,e_greedy_increment=0.01)
    env.after(100,update)
    # env.update()
    env.mainloop()