from OpenGL.GL import *
import numpy as np
from math import sqrt, cos, sin, acos, pi
from Cube import Cube
import WorldCommon as WC
import random


class TetrisPieces:
    Blocks = [("I", 4, "LightBlue", ((0, 0, 0), (1, 0, 0), (2, 0, 0), (3, 0, 0))),  # I
              ("O", 2, "Yellow", ((0, 0, 0), (0, 1, 0), (1, 0, 0), (1, 1, 0))),  # O
              ("T", 3, "Purple", ((0, 0, 0), (1, 0, 0), (1, 1, 0), (2, 0, 0))),  # T
              ("L", 3, "Red", ((0, 0, 0), (1, 0, 0), (2, 0, 0), (2, 1, 0))),  # L
              ("S", 3, "Green", ((0, 0, 0), (1, 0, 0), (1, 1, 0), (2, 1, 0))),  # S
              ("J", 3, "Blue", ((0, 0, 0), (1, 0, 0), (2, 0, 0), (0, 1, 0))),  # J
              ("Z", 3, "Orange", ((1, 0, 0), (2, 0, 0), (0, 1, 0), (1, 1, 0)))]  # Z

    def __init__(self, block=None):
        self.block = block if block else random.randint(0, 6)
        self.name = TetrisPieces.Blocks[self.block][0]
        self.size = TetrisPieces.Blocks[self.block][1]
        self.shape = [
            [[0]*self.size for i in range(self.size)]for j in range(self.size)]
        self.color = TetrisPieces.Blocks[self.block][2]
        self.components = []
        for x, y, z in TetrisPieces.Blocks[self.block][3]:
            component = Cube(self.color, np.asfarray([x, y, z]))
            self.shape[x][y][z] = 1
            self.components.append(component)

        self.x = WC.BorderX-self.size
        self.y = 8
        self.z = WC.BorderZ-self.size

    def point_rotation(u, v, rotation):
        if u == v == 0:
            return 0, 0
        d = sqrt(u**2+v**2)
        if v != abs(v):
            d *= -1
        angle = acos(u/d)
        return cos(angle+rotation)*d, sin(angle+rotation)*d

    def rotation(self, axis, angle=pi/2):
        tmp = self.shape
        self.shape = [
            [[0]*self.size for i in range(self.size)]for j in range(self.size)]
        for x, Lx in enumerate(tmp):
            for y, Ly in enumerate(Lx):
                for z, el in enumerate(Ly):
                    if el:
                        T = self.size/2-.5
                        nx, ny, nz = x-T, y-T, z-T
                        if axis == 0:
                            nx, ny = TetrisPieces.point_rotation(nx, ny, angle)
                        elif axis == 1:
                            nz, ny = TetrisPieces.point_rotation(nz, ny, angle)
                        else:
                            nx, nz = TetrisPieces.point_rotation(nx, nz, angle)

                        self.shape[round(nx+T)][round(ny+T)][round(nz+T)] = 1

    def Collided(self):
        for x, xL in enumerate(self.shape):
            for y, yL in enumerate(xL):
                for z, el in enumerate(yL):
                    if el:
                        # Keep block in border
                        if not (0 <= x+self.x < WC.BorderX and 0 <= round(y+self.y) <= WC.BorderY and 0 <= z+self.z < WC.BorderZ):
                            return False
                        # check collision
                        if WC.layers[x+self.x][round(y+self.y)][z+self.z] != -1:
                            return False

        return True

    def Update(self, deltaTime):
        pass

    def add(arg, mul=1):
        res = list(arg[:3])
        for i in range(3):
            res[i] += arg[3+i]
            res[i] *= mul
        return res

    def Reset(self):
        glColor(.1, .1, .05)
        glBegin(GL_QUADS)
        for surface in WC.surfaces:
            for vertex in surface:
                glVertex(TetrisPieces.add(
                    WC.verticies[vertex]+(0, 0, 0), 1000))
        glEnd()

    def Render(self):

        for x, xL in enumerate(self.shape):
            for y, yL in enumerate(xL):
                for z, el in enumerate(yL):
                    if el:
                        component = Cube(
                            self.color, (x-WC.BorderX/2+self.x, y-WC.BorderY/2+self.y, z-WC.BorderZ/2+self.z))
                        component.Render()
