import numpy as np
from tkinter import *

class Box:
    def __init__(self,x,y,z):
        self.px=x
        self.py=y
        self.empty=z

    def isInRange(self, x, y, r):
        if (self.x-x)*(self.x-x)+(self.y-y)*(self.y-y)<=r*r:
            return True
        return False

    def isEmpty(self):
        return self.empty

    def fill(self):
        self.empty=False

class Grid:
    def __init__(self,x,y):
        self.dx=x
        self.dy=y
        self.tab=np.empty((x,y),dtype=Box)
        for i in range(x):
            for j in range(y):
                self.tab[i][j] = Box(i,j,True)

    def closeGrid(self):
        for i in range(self.dx):
            self.tab[i][0].fill()
            self.tab[i][self.dy-1].fill()
        for j in range(self.dy):
            self.tab[0][j].fill()
            self.tab[self.dx-1][j].fill()

    def addWall(self, x1, y1, x2, y2):
        for i in range(x1,x2):
            for j in range(y1,y2):
                self.tab[i][j].fill()

def closeGridandDraw(grid,canvas,x,y):
    grid.closeGrid()
    canvas.create_rectangle(1,1,x,1,fill="black")
    canvas.create_rectangle(1,1,2,y,fill="black")
    canvas.create_rectangle(x-1,1,x,y,fill="black")
    canvas.create_rectangle(1,y-1,x,y,fill="black")

def addWallandDraw(grid, canvas, x1, y1, x2, y2):
    grid.addWall(x1,y1,x2,y2)
    canvas.create_rectangle(x1,y1,x2,y2,fill="black")

def main():
    x=1000;
    y=500;
    window = Tk()
    window.title("Homework 1")
    #fenetre.config(bg = "#666666")
    size=str(x+10)+"x"+str(y+10)
    window.geometry(size)
    canvas = Canvas(window, width=x, height=y,bg="white")
    g=Grid(x,y)
    closeGridandDraw(g,canvas,x,y)
    addWallandDraw(g,canvas,290,0,300,400)
    addWallandDraw(g,canvas,690,100,700,500)
    canvas.pack()
    window.mainloop()


if __name__ == "__main__":
    main()
