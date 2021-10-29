import numpy as np
import random
from tkinter import *
import gym



class Box:
    def __init__(self, x, y, empty, dirty=False):
        self.px = x
        self.py = y
        self.empty = empty
        self.dirty = dirty

    def isInRange(self, x, y, r):
        if (self.x - x) * (self.x - x) + (self.y - y) * (self.y - y) <= r * r:
            return True
        return False

    def isEmpty(self):
        return self.empty

    def fill(self):
        self.empty = False

    def makeDirty(self):
        self.dirty = True

    def isDirty(self):
        return self.dirty


class Grid:
    def __init__(self, x, y):
        self.dx = x
        self.dy = y
        self.tab = np.empty((x, y), dtype=Box)
        for i in range(x):
            for j in range(y):
                self.tab[i][j] = Box(i, j, True)

    def closeGrid(self):
        for i in range(self.dx):
            self.tab[i][0].fill()
            self.tab[i][self.dy - 1].fill()
        for j in range(self.dy):
            self.tab[0][j].fill()
            self.tab[self.dx - 1][j].fill()

    def addWall(self, x1, y1, x2, y2):
        for i in range(x1, x2):
            for j in range(y1, y2):
                self.tab[i][j].fill()

    def addRandomDirt(self, percentage):
        for i in range(self.dx):
            for j in range(self.dy):
                if self.tab[i][j].isEmpty():
                    if random.random()*100 < percentage:
                        self.tab[i][j].makeDirty()


class cleanerEnv(gym.Env):
    def __init__(self):
        self.sizex = 1000
        self.sizey = 500
        self.dirtpercent = 0.5

        self.grid = Grid(self.sizex, self.sizey)
        self.grid.addWall(290, 0, 300, 400)
        self.grid.addWall(690, 100, 700, 500)
        self.grid.closeGrid()
        self.grid.addRandomDirt(self.dirtpercent)

        self.viewer = None

    def render(self, mode="human"):
        screen_width = 1000
        screen_height = 500

        if self.viewer is None:
            from gym.envs.classic_control import rendering
            self.viewer = rendering.Viewer(screen_width, screen_height)

            wall1 = rendering.FilledPolygon([(290, 0), (300, 0), (300, 400), (290, 400)])
            self.wall1trans = rendering.Transform()
            wall1.add_attr(self.wall1trans)
            self.viewer.add_geom(wall1)

            wall2 = rendering.FilledPolygon([(690, 500), (700, 500), (700, 100), (690, 100)])
            self.wall2trans = rendering.Transform()
            wall2.add_attr(self.wall2trans)
            self.viewer.add_geom(wall2)

        return self.viewer.render(return_rgb_array=mode == "rgb_array")


def closeGridandDraw(grid, canvas, x, y):
    grid.closeGrid()
    canvas.create_rectangle(1, 1, x, 1, fill="black")
    canvas.create_rectangle(1, 1, 2, y, fill="black")
    canvas.create_rectangle(x - 1, 1, x, y, fill="black")
    canvas.create_rectangle(1, y - 1, x, y, fill="black")


def addWallandDraw(grid, canvas, x1, y1, x2, y2):
    grid.addWall(x1, y1, x2, y2)
    canvas.create_rectangle(x1, y1, x2, y2, fill="black")


def addDirtandDraw(grid, canvas, percentage):
    grid.addRandomDirt(percentage)
    for i in range(grid.dx):
        for j in range(grid.dy):
            if grid.tab[i][j].isDirty():
                canvas.create_rectangle(i, j, i+1, j+1, fill="red")

def main():
    x = 1000
    y = 500
    window = Tk()
    window.title("Homework 1")
    # fenetre.config(bg = "#666666")
    size = str(x + 10) + "x" + str(y + 10)
    window.geometry(size)
    canvas = Canvas(window, width=x, height=y, bg="white")
    g = Grid(x, y)
    closeGridandDraw(g, canvas, x, y)
    addWallandDraw(g, canvas, 290, 0, 300, 400)
    addWallandDraw(g, canvas, 690, 100, 700, 500)

    addDirtandDraw(g, canvas, percentage=0.5)

    canvas.pack()
    window.mainloop()


if __name__ == "__main__":
    main()
