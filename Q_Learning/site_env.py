


import numpy as np
import time
import sys
from RL_brain import QLearningTable
# from DQN_modified import DeepQNetwork
import tkinter as tk


UNIT = 100   # pixels
MAZE_H = 6  # grid height
MAZE_W = 6  # grid width
RL = QLearningTable
# RL = DeepQNetwork


class Site(tk.Tk, object):
    def __init__(self):
        super(Site, self).__init__()
        self.action_space = ['u', 'd', 'l', 'r']
        self.n_actions = len(self.action_space)
        self.title('site')
        self.geometry('{0}x{1}'.format(MAZE_H * UNIT, MAZE_H * UNIT))
        self._build_maze()
        self.counter = 0
        self.init_counter = 0
        

    def _build_maze(self):

        self.canvas = tk.Canvas(self, bg='white',
                           height=MAZE_H * UNIT,
                           width=MAZE_W * UNIT)

        # create grids
        for c in range(0, MAZE_W * UNIT, UNIT):
            x0, y0, x1, y1 = c, 0, c, MAZE_H * UNIT
            self.canvas.create_line(x0, y0, x1, y1)
        for r in range(0, MAZE_H * UNIT, UNIT):
            x0, y0, x1, y1 = 0, r, MAZE_W * UNIT, r
            self.canvas.create_line(x0, y0, x1, y1)

        # create origin
        origin = np.array([50, 50])
        self.reward = 0

        # forbidden area
        hell0_center = origin + np.array([UNIT*5 , UNIT *3])
        self.hell0 = self.canvas.create_rectangle(
            hell0_center[0] - 40, hell0_center[1] - 40,
            hell0_center[0] + 40, hell0_center[1] + 40,
            fill='black')

        # create target
        location_center = origin + np.array([UNIT , 0])
        self.location = self.canvas.create_oval(
            location_center[0] - 40, location_center[1] - 40,
            location_center[0] + 40, location_center[1] + 40,
            fill='yellow')

        # create component
        comp_center = origin + np.array([UNIT * 5, UNIT * 5])
        self.comp = self.canvas.create_oval(
            comp_center[0] - 40, comp_center[1] - 40,
            comp_center[0] + 40, comp_center[1] + 40,
            fill='yellow')


        # create bot
        rect_center = origin + + np.array([UNIT * 5, 0])
        self.rect = self.canvas.create_rectangle(
            rect_center[0] - 40, rect_center[1] - 40,
            rect_center[0] + 40, rect_center[1] + 40,
            fill='white')

        # pack all
        self.canvas.pack()

    def reset(self):
        self.update()
        # time.sleep(0.5)

        self.canvas.delete(self.rect)
        self.canvas.delete(self.location)
        self.canvas.delete(self.comp)
        self.counter = 0



        origin = np.array([50, 50])
        
        rect_center = origin + + np.array([UNIT *5, 0])
        self.rect = self.canvas.create_rectangle(
            rect_center[0] - 40, rect_center[1] - 40,
            rect_center[0] + 40, rect_center[1] + 40,
            fill='white')

        # create component
        location_center = origin + np.array([UNIT , 0])
        self.location = self.canvas.create_oval(
            location_center[0] - 40, location_center[1] - 40,
            location_center[0] + 40, location_center[1] + 40,
            fill='yellow')


        # create component
        comp_center = origin + np.array([UNIT * 5, UNIT * 5])
        self.comp = self.canvas.create_oval(
            comp_center[0] - 40, comp_center[1] - 40,
            comp_center[0] + 40, comp_center[1] + 40,
            fill='yellow')

        self.reward = 0
        self.done = False
        # print('the state is: ', self.canvas.coords(self.rect))
        s =self.canvas.coords(self.rect)
        # action_value = RL.get_action_value(self)
        if self.init_counter == 0:
            up = tk.Label(self, text=0.0)
            up.place(x=s[0] + 40, y=s[1] + 20, anchor="center")
            down = tk.Label(self, text=0.0)
            down.place(x=s[0] + 40, y=s[1] + 60, anchor="center")
            right = tk.Label(self, text=0.0)
            right.place(x=s[0] + 60, y=s[1] + 40, anchor="center")
            left = tk.Label(self, text=0.0)
            left.place(x=s[0] + 20, y=s[1] + 40, anchor="center")
            self.init_counter += 1
        else:
            a = RL.get_action_value(self).round(2)
            up = tk.Label(self, text=a[0])
            up.place(x=s[0] + 40, y=s[1] + 20, anchor="center")
            down = tk.Label(self, text=a[1])
            down.place(x=s[0] + 40, y=s[1] + 60, anchor="center")
            right = tk.Label(self, text=a[2])
            right.place(x=s[0] + 60, y=s[1] + 40, anchor="center")
            left = tk.Label(self, text=a[3])
            left.place(x=s[0] + 20, y=s[1] + 40, anchor="center")
            up.place_forget()
            down.place_forget()
            left.place_forget()
            right.place_forget()


        return self.canvas.coords(self.rect)

    def step(self, action):
        global up, down, left, right
        s = self.canvas.coords(self.rect)
        base_action = np.array([0, 0])
        if action == 0:   # up
            if s[1] > UNIT:
                # self.done = True
                # self.reward -= 10
                base_action[1] -= UNIT
                # time.sleep(1)
        elif action == 1:   # down
            if s[1] < (MAZE_H - 1) * UNIT:
                # self.done = True
                # self.reward -= 10
                base_action[1] += UNIT
                # time.sleep(1)
        elif action == 2:   # right
            if s[0] < (MAZE_W - 1) * UNIT:
                # self.done = True
                # self.reward -= 10
                base_action[0] += UNIT
                # time.sleep(1)
        elif action == 3:   # left
            if s[0] > UNIT:
                # self.done = True
                # self.reward -= 10
                base_action[0] -= UNIT
                # time.sleep(1)


        self.canvas.move(self.rect, base_action[0], base_action[1])  # move agent
        s_ = self.canvas.coords(self.rect)  # next state

        # if s_[0] <= 50 or s_[0] >= 550 or s_[1] <= 50 or s_[1] >= 550:
        #     self.done = True
        #     self.reward -= 10
        # print(s)
        # print(s_)
        # if self.init_counter % 10 == 0:
        a = RL.get_action_value(self).round(2)
        up=tk.Label(self, text=a[0])
        up.place(x=s[0] + 40, y=s[1] + 20, anchor="center")
        down=tk.Label(self, text=a[1])
        down.place(x=s[0] + 40, y=s[1] + 60, anchor="center")
        right=tk.Label(self, text=a[2])
        right.place(x=s[0] + 60, y=s[1] + 40, anchor="center")
        left=tk.Label(self, text=a[3])
        left.place(x=s[0] + 20, y=s[1] + 40, anchor="center")

        # self.reward function
        if s_ == self.canvas.coords(self.location):
            self.reward += 100
            self.counter += 1
            self.canvas.delete(self.location)
        elif s_ == self.canvas.coords(self.comp):
            self.reward += 100
            self.counter += 1
            self.canvas.delete(self.comp)
        elif self.counter == 2:
            self.done = True
        elif s_ in [self.canvas.coords(self.hell0)]:
            self.reward = -10
            self.done = True
            s_ = 'terminal'
        else:
            self.reward = 0
            self.done = False

        return s_, self.reward, self.done

    def render(self):
        time.sleep(0.1)
        self.update()

    def sample_action(self):
        action = int(input('input action: '))
        return action


def update():
    for t in range(10):
        s = env.reset()
        while True:
            env.render()
            a = 1
            s, r, done = env.step(a)
            if done:
                break




if __name__ == '__main__':
    env = Site()
    # env.after(100, update)
    env.update()
    env.mainloop()