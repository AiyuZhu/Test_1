


import numpy as np
import time
from DQN import DeepQNetwork
import tkinter as tk



UNIT = 100   # pixels
SITE_H = 6  # grid height
SITE_W = 6  # grid width
RL = DeepQNetwork


class Site(tk.Tk, object):
    def __init__(self):
        super(Site, self).__init__()
        self.action_space = ['u', 'd', 'l', 'r']
        self.n_actions = len(self.action_space)
        self.title('site')
        self.geometry('{0}x{1}'.format(SITE_H * UNIT, SITE_H * UNIT))
        self._build_site()
        self.counter = 0
        self.init_counter = 0
        

    def _build_site(self):

        self.canvas = tk.Canvas(self, bg='white',
                           height=SITE_H * UNIT,
                           width=SITE_W * UNIT)

        # create grids
        for c in range(0, SITE_W * UNIT, UNIT):
            x0, y0, x1, y1 = c, 0, c, SITE_H * UNIT
            self.canvas.create_line(x0, y0, x1, y1)
        for r in range(0, SITE_H * UNIT, UNIT):
            x0, y0, x1, y1 = 0, r, SITE_W * UNIT, r
            self.canvas.create_line(x0, y0, x1, y1)

        # create origin
        origin = np.array([50, 50])
        self.reward = 0

        # forbidden area
        forbidden_center = origin + np.array([UNIT*5 , UNIT *3])
        self.forbidden = self.canvas.create_rectangle(
            forbidden_center[0] - 40, forbidden_center[1] - 40,
            forbidden_center[0] + 40, forbidden_center[1] + 40,
            fill='black')

        # create target_location
        # location_center = origin + np.array([UNIT , 0])
        # self.location = self.canvas.create_oval(
        #     location_center[0] - 40, location_center[1] - 40,
        #     location_center[0] + 40, location_center[1] + 40,
        #     fill='red')

        # create component
        comp_center = origin + np.array([UNIT * 5, UNIT * 5])
        self.comp = self.canvas.create_oval(
            comp_center[0] - 40, comp_center[1] - 40,
            comp_center[0] + 40, comp_center[1] + 40,
            fill='yellow')


        # create bot
        bot_center = origin + + np.array([UNIT * 5, 0])
        self.bot = self.canvas.create_rectangle(
            bot_center[0] - 40, bot_center[1] - 40,
            bot_center[0] + 40, bot_center[1] + 40,
            fill='white')

        # pack all
        self.canvas.pack()

    def reset(self):
        self.update()
        # time.sleep(0.5)

        self.canvas.delete(self.bot)
        # self.canvas.delete(self.location)
        self.canvas.delete(self.comp)
        self.counter = 0



        origin = np.array([50, 50])
        
        bot_center = origin + + np.array([UNIT *5, 0])
        self.bot = self.canvas.create_rectangle(
            bot_center[0] - 40, bot_center[1] - 40,
            bot_center[0] + 40, bot_center[1] + 40,
            fill='white')

        #create location
        # location_center = origin + np.array([UNIT , 0])
        # self.location = self.canvas.create_oval(
        #     location_center[0] - 40, location_center[1] - 40,
        #     location_center[0] + 40, location_center[1] + 40,
        #     fill='red')


        # create component
        comp_center = origin + np.array([UNIT * 5, UNIT * 5])
        self.comp = self.canvas.create_oval(
            comp_center[0] - 40, comp_center[1] - 40,
            comp_center[0] + 40, comp_center[1] + 40,
            fill='yellow')

        self.reward = 0
        self.done = False
        # print('the state is: ', self.canvas.coords(self.bot))
        s =self.canvas.coords(self.bot)
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
        elif self.init_counter < 50 or self.init_counter % 100 == 0:
            a_origin = RL.get_action_value(self).round(1)
            a = np.squeeze(a_origin)
            up = tk.Label(self, text=a[0])
            up.place(x=s[0] + 40, y=s[1] + 15, anchor="center")
            down = tk.Label(self, text=a[1])
            down.place(x=s[0] + 40, y=s[1] + 65, anchor="center")
            right = tk.Label(self, text=a[2])
            right.place(x=s[0] + 65, y=s[1] + 40, anchor="center")
            left = tk.Label(self, text=a[3])
            left.place(x=s[0] + 15, y=s[1] + 40, anchor="center")
            up.place_forget()
            down.place_forget()
            left.place_forget()
            right.place_forget()
            self.init_counter += 1
        else:
            self.init_counter += 1
        return np.array(self.canvas.coords(self.bot))[:2]

    def step(self, action):
        global up, down, left, right
        s = self.canvas.coords(self.bot)
        base_action = np.array([0, 0])
        if action == 0:   # up
            # if s[1] > 100:
                # self.done = True
                # self.reward -= 10
                base_action[1] -= UNIT
                # time.sleep(1)
        elif action == 1:   # down
            # if s[1] < 510:
                # self.done = True
                # self.reward -= 10
                base_action[1] += UNIT
                # time.sleep(1)
        elif action == 2:   # right
            # if s[0] > 100:
                # self.done = True
                # self.reward -= 10
                base_action[0] -= UNIT
                # time.sleep(1)
        elif action == 3:   # left
            # if s[0] < 510:
                # self.done = True
                # self.reward -= 10
                base_action[0] += UNIT
                # time.sleep(1)


        self.canvas.move(self.bot, base_action[0], base_action[1])  # move agent
        # new_s = []
        # for i in range(4):
        #     new = self.canvas.coords(self.bot)[i]-self.canvas.coords(self.location)[i]
        #     new_s.append(new)
        next_position = self.canvas.coords(self.bot)
        s_ = np.array(self.canvas.coords(self.bot))[:2]# next state
        # s = new_s

        #draw action value
        if self.init_counter < 50 or self.init_counter % 50 == 0:
            #get action value
            a_origin = RL.get_action_value(self).round(1)
            a = np.squeeze(a_origin)
            up = tk.Label(self, text=a[0])
            up.place(x=s[0] + 40, y=s[1] + 15, anchor="center")
            down = tk.Label(self, text=a[1])
            down.place(x=s[0] + 40, y=s[1] + 65, anchor="center")
            left = tk.Label(self, text=a[2])
            left.place(x=s[0] + 15, y=s[1] + 40, anchor="center")
            right = tk.Label(self, text=a[3])
            right.place(x=s[0] + 65, y=s[1] + 40, anchor="center")

        # self.reward function
        if next_position == self.canvas.coords(self.comp):
            self.reward += 10
            self.counter += 1
            self.canvas.delete(self.comp)
            print(self.reward)
        # elif next_position == self.canvas.coords(self.location):
        #     self.reward += 10
        #     self.counter += 1
        #     self.canvas.delete(self.location)
            # print(self.reward)
        elif next_position == self.canvas.coords(self.forbidden):
            self.reward -= 100
            self.done = True
            # print(self.reward)
        elif s_[0] < 10 or s_[0] > 510 or s_[1] < 10 or s_[1] > 510:
            self.reward -= 100
            self.done = True
        elif abs(next_position[2]-self.canvas.coords(self.comp)[2])+abs(next_position[3]-self.canvas.coords(self.comp)[3]) \
                < abs(s[2]-self.canvas.coords(self.comp)[2])+abs(s[3]-self.canvas.coords(self.comp)[3]): #and abs(s[0] - self.canvas.coords(self.forbidden)[0]) + abs(s[1]- self.canvas.coords(self.forbidden)[1]) != 100:
            self.reward +=1
        else:
            # self.reward += 0.0001
            self.done = False

        if self.counter == 1:
            self.done = True
            self.reward += 20
        # print(s_[0] - self.canvas.coords(self.forbidden)[0] )
        # print(s_[1] - self.canvas.coords(self.forbidden)[1] )

        # print(s[:2])
        # print(s_)
        # print(self.reward)
        # print(s_[0])
        # print(s_[1])
        return s_, self.reward, self.done

    def render(self):
        time.sleep(0.1)
        self.update()

    def sample_action(self):
        action = int(input('input action: '))
        return action

if __name__ == '__main__':
    env = Site()
    # env.after(100, update)
    env.update()
    env.mainloop()