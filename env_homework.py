import numpy as np
import random
import gym
import matplotlib.pyplot as plt
from matplotlib import colors


class Grid:
    """
    grid representating the environnement
    0 -> unknow case
    1 -> empty case
    2 -> occupied case
    3 -> dirty case
    4 -> charging case
    """

    def __init__(self, x, y, unknown=False):
        self.dx = x
        self.dy = y
        self.tab = np.empty((x, y), dtype=int)
        for i in range(x):
            for j in range(y):
                if unknown:
                    self.tab[i][j] = 0
                else:
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
                    if random.random() * 100 < percentage:
                        self.tab[i][j] = 3

    def addChargingCase(self, x, y):
        self.tab[x][y] = 4


class cleanerEnv(gym.Env):
    def __init__(self):
        self.sizex = 50
        self.sizey = 25
        self.dirtpercent = 5
        self.r_detection = 5

        self.pos = (1, 10)
        self.battery = 50

        self.grid = Grid(self.sizex, self.sizey)
        self.grid.addWall(15, 0, 16, 20)
        self.grid.addWall(35, 5, 36, 25)
        self.grid.closeGrid()
        self.grid.addRandomDirt(self.dirtpercent)
        self.grid.addChargingCase(1, 10)

        self.observation_grid = Grid(self.sizex, self.sizey, unknown=True)
        self.updateObservationGrid()

        self.state = None

    def step(self, action):
        """
        actions:
        0 -> aller à droite
        1 -> aller à gauche
        2 -> avancer
        3 -> reculer

        rewards:
        si sale -> 1
        si occupé ou batterie vide -> -1000 et done
        sinon 0
        """

        if action == 0:
            self.pos = (self.pos[0] + 1, self.pos[1])
        if action == 1:
            self.pos = (self.pos[0] - 1, self.pos[1])
        if action == 2:
            self.pos = (self.pos[0], self.pos[1] + 1)
        if action == 3:
            self.pos = (self.pos[0], self.pos[1] - 1)

        done = False
        if self.grid.tab[self.pos[0]][self.pos[1]] == 3:
            reward = 1
            self.grid.tab[self.pos[0]][self.pos[1]] = 1
        elif self.grid.tab[self.pos[0]][self.pos[1]] == 2:
            reward = - 1000
            done = True
        else:
            reward = 0

        self.updateObservationGrid()

        self.battery -= 1
        if self.battery <= 0:
            done = True

        self.state = (self.pos, self.battery, self.observation_grid)
        return self.state, reward, done, {}

    def updateObservationGrid(self):
        for x in range(self.sizex):
            for y in range(self.sizey):
                if (self.pos[0] - x) * (self.pos[0] - x) + (self.pos[1] - y) * (self.pos[1] - y) <= self.r_detection * self.r_detection:
                    self.observation_grid.tab[x][y] = self.grid.tab[x][y]

    def render(self, mode="human"):
        cmap = colors.ListedColormap(['grey', 'white', 'black', 'red', 'blue'])
        bounds = [-0.5, 0.5, 1.5, 2.5, 3.5, 4.5]
        norm = colors.BoundaryNorm(bounds, cmap.N)

        fig, (ax1, ax2) = plt.subplots(1, 2)
        ax1.imshow(self.observation_grid.tab, cmap=cmap, norm=norm)
        ax2.imshow(self.grid.tab, cmap=cmap, norm=norm)

        plt.show()
