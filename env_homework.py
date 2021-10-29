import numpy as np
import random
from tkinter import *
import gym
import matplotlib.pyplot as plt
from matplotlib import colors


    # def isInRange(self, x, y, r):
    #     if (self.x - x) * (self.x - x) + (self.y - y) * (self.y - y) <= r * r:
    #         return True
    #     return False


class Grid:
    """
    grid representating the environnement
    0 -> unknow case
    1 -> empty case
    2 -> occupied case
    3 -> dirty case
    4 -> charging case
    """

    def __init__(self, x, y):
        self.dx = x
        self.dy = y
        self.tab = np.empty((x, y), dtype=int)
        for i in range(x):
            for j in range(y):
                self.tab[i][j] = 1

    def closeGrid(self):
        for i in range(self.dx):
            self.tab[i][0] = 2
            self.tab[i][self.dy - 1] = 2
        for j in range(self.dy):
            self.tab[0][j] = 2
            self.tab[self.dx - 1][j] = 2

    def addWall(self, x1, y1, x2, y2):
        for i in range(x1, x2):
            for j in range(y1, y2):
                self.tab[i][j] = 2

    def addRandomDirt(self, percentage):
        for i in range(self.dx):
            for j in range(self.dy):
                if self.tab[i][j] != 2:
                    if random.random()*100 < percentage:
                        self.tab[i][j] = 3
                        # print("(" + str(i) + ", " + str(j) + ")")


class cleanerEnv(gym.Env):
    def __init__(self):
        self.sizex = 50
        self.sizey = 25
        self.dirtpercent = 5

        self.grid = Grid(self.sizex, self.sizey)
        self.grid.addWall(15, 0, 16, 20)
        self.grid.addWall(35, 5, 36, 25)
        self.grid.closeGrid()
        self.grid.addRandomDirt(self.dirtpercent)

        self.viewer = None

    def render(self, mode="human"):

        # create discrete colormap
        cmap = colors.ListedColormap(['grey', 'white', 'black', 'red', 'blue'])
        bounds = [0, 1, 2, 3, 4]
        norm = colors.BoundaryNorm(bounds, cmap.N)

        fig, ax = plt.subplots()
        ax.imshow(self.grid.tab, cmap=cmap, norm=norm)

        # draw gridlines
        # ax.grid(which='major', axis='both', linestyle='-', color='k', linewidth=1)
        # ax.set_xticks(np.arange(-.5, 10, 1));
        # ax.set_yticks(np.arange(-.5, 10, 1));

        plt.show()
