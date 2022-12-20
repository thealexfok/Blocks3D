from OpenGL.GL import *
import WorldCommon as WC


_verts = ((4, -6, -4),
          (4, 6, -4),
          (-4, 6, -4),
          (-4, -6, -4),
          (4, -6, 4),
          (4, 6, 4),
          (-4, -6, 4),
          (-4, 6, 4))

_lines = ((0, 1, 2, 3, 0, 4, 5, 7, 6, 4),
          (5, 1),
          (6, 3),
          (7, 2))

_edges = ((0, 1),
          (0, 3),
          (0, 4),
          (1, 2),
          (1, 5),
          (2, 3),
          (2, 6),
          (3, 7),
          (4, 5),
          (4, 7),
          (5, 6),
          (6, 7)
          )


def Render():
    global _verts
    global _lines
    global _edges

    glColor(1, 1, 1)
    glBegin(GL_LINES)
    for edge in WC.edges:
        for vertex in edge:
            glVertex(WC.verticies[vertex][0]*WC.BorderX-.5,
                     WC.verticies[vertex][1]*WC.BorderY-.5, WC.verticies[vertex][2]*WC.BorderZ-.5)
    glEnd()
