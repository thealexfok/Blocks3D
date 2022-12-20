from OpenGL.GL import *
import numpy as np
import WorldCommon as WC
from OpenGL.arrays import vbo
from OpenGL.GL import shaders


def Init():
    global colors

    colors = {"LightBlue": np.asfarray([0.5, 1, 1]),
              "Yellow": np.asfarray([1, 1, 0]),
              "Purple": np.asfarray([1, 0, 1]),
              "Red": np.asfarray([1, 0, 0]),
              "Green": np.asfarray([0, 1, 0]),
              "Blue": np.asfarray([0, 0, 1]),
              "Orange": np.asfarray([1, 0.5, 0])}


class Cube:
    def __init__(self, color, pos):
        global colors
        self.pos = pos
        self.color = colors[color]

        # 3 positions, 3 colors, 3 normals, 2 UVs
        self.verts = np.float32([(0.5+pos[0], -0.5+pos[1], -0.5+pos[2], self.color[0], self.color[1],
                                  self.color[2], 0, 0, -0.5, 0, 0),
                                 (0.5+pos[0], 0.5+pos[1], -0.5+pos[2], self.color[0], self.color[1],
                                  self.color[2], 0, 0, -0.5, 0.5, 0),
                                 (-0.5+pos[0], 0.5+pos[1], -0.5+pos[2], self.color[0], self.color[1],
                                  self.color[2], 0, 0, -0.5, 0.5, 0.5),
                                 (-0.5+pos[0], -0.5+pos[1], -0.5+pos[2], self.color[0], self.color[1],
                                  self.color[2], 0, 0, -0.5, 0, 0.5),

                                 (-0.5+pos[0], -0.5+pos[1], -0.5+pos[2], self.color[0], self.color[1],
                                  self.color[2], -0.5, 0, 0, 0, 0),
                                 (-0.5+pos[0], 0.5+pos[1], -0.5+pos[2], self.color[0], self.color[1],
                                  self.color[2], -0.5, 0, 0, 0.5, 0),
                                 (-0.5+pos[0], 0.5+pos[1], 0.5+pos[2], self.color[0], self.color[1],
                                  self.color[2], -0.5, 0, 0, 0.5, 0.5),
                                 (-0.5+pos[0], -0.5+pos[1], 0.5+pos[2], self.color[0], self.color[1],
                                  self.color[2], -0.5, 0, 0, 0, 0.5),

                                 (-0.5+pos[0], -0.5+pos[1], 0.5+pos[2], self.color[0], self.color[1],
                                  self.color[2], 0, 0, 0.5, 0, 0),
                                 (-0.5+pos[0], 0.5+pos[1], 0.5+pos[2], self.color[0], self.color[1],
                                  self.color[2], 0, 0, 0.5, 0.5, 0),
                                 (0.5+pos[0], 0.5+pos[1], 0.5+pos[2], self.color[0], self.color[1],
                                  self.color[2], 0, 0, 0.5, 0.5, 0.5),
                                 (0.5+pos[0], -0.5+pos[1], 0.5+pos[2], self.color[0], self.color[1],
                                  self.color[2], 0, 0, 0.5, 0, 0.5),

                                 (0.5+pos[0], -0.5+pos[1], 0.5+pos[2], self.color[0], self.color[1],
                                  self.color[2], 0.5, 0, 0, 0, 0),
                                 (0.5+pos[0], 0.5+pos[1], 0.5+pos[2], self.color[0], self.color[1],
                                  self.color[2], 0.5, 0, 0, 0.5, 0),
                                 (0.5+pos[0], 0.5+pos[1], -0.5+pos[2], self.color[0], self.color[1],
                                  self.color[2], 0.5, 0, 0, 0.5, 0.5),
                                 (0.5+pos[0], -0.5+pos[1], -0.5+pos[2], self.color[0], self.color[1],
                                  self.color[2], 0.5, 0, 0, 0, 0.5),

                                 (0.5+pos[0], 0.5+pos[1], -0.5+pos[2], self.color[0], self.color[1],
                                  self.color[2], 0, 0.5, 0, 0, 0),
                                 (0.5+pos[0], 0.5+pos[1], 0.5+pos[2], self.color[0], self.color[1],
                                  self.color[2], 0, 0.5, 0, 0.5, 0),
                                 (-0.5+pos[0], 0.5+pos[1], 0.5+pos[2], self.color[0], self.color[1],
                                  self.color[2], 0, 0.5, 0, 0.5, 0.5),
                                 (-0.5+pos[0], 0.5+pos[1], -0.5+pos[2], self.color[0], self.color[1],
                                  self.color[2], 0, 0.5, 0, 0, 0.5),

                                 (0.5+pos[0], -0.5+pos[1], 0.5+pos[2], self.color[0], self.color[1],
                                  self.color[2], 0, -0.5, 0, 0, 0),
                                 (0.5+pos[0], -0.5+pos[1], -0.5+pos[2], self.color[0], self.color[1],
                                  self.color[2], 0, -0.5, 0, 0.5, 0),
                                 (-0.5+pos[0], -0.5+pos[1], -0.5+pos[2], self.color[0], self.color[1],
                                  self.color[2], 0, -0.5, 0, 0.5, 0.5),
                                 (-0.5+pos[0], -0.5+pos[1], 0.5+pos[2], self.color[0], self.color[1],
                                  self.color[2], 0, -0.5, 0, 0, 0.5)
                                 ])

    def Update(self, deltaTime):
        pass

    def add(arg, mul=1):
        res = list(arg[:3])
        for i in range(3):
            res[i] += arg[3+i]
            res[i] *= mul
        return res

    def Render(self):
        glBegin(GL_QUADS)
        glColor(self.color)
        for surface in WC.surfaces:
            for vertex in surface:
                glVertex(Cube.add(WC.verticies[vertex]+self.pos))
        glEnd()

        # block lines
        glBegin(GL_LINES)
        glColor(.5, .6, .5)
        for edge in WC.edges:
            for vertex in edge:
                glVertex(Cube.add(WC.verticies[vertex]+self.pos))
        glEnd()
