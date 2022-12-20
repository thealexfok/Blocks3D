from OpenGL.GL import *
from OpenGL.GLU import *

import UI.UICommon as UICommon
# Text
from UI.UIText import UIText
# Image
from UI.UIImage import UIImage


def init():
    global _uiObjects
    global _uiIds
    global _uiNames
    global _tetris
    global _paused
    _uiObjects = []
    _uiIds = {}
    _uiNames = {}

    helloworld = UIText("Blocks 3D", align="center")
    scoretag = UIText("Score", size=16, align="right",
                      xoffset=-20, yoffset=-30)
    score = UIText("0", align="right", xoffset=-20, yoffset=-50)
    preview = UIText("Next", size=16, align="right",
                     valign="center", xoffset=-30, yoffset=-30)
    _tetris = UIText("TETRIS", size=64, align="center",
                     valign="center", visible=False)
    _uiNames["tetris"] = _tetris
    _paused = UIText("Game Paused", align="center",
                     valign="center", visible=False)
    I = UIImage("UI/Data/I.png", align="right", valign="center",
                xoffset=-30, yoffset=-55, visible=False)
    O = UIImage("UI/Data/O.png", align="right", valign="center",
                xoffset=-30, yoffset=-55, visible=False)
    T = UIImage("UI/Data/T.png", align="right", valign="center",
                xoffset=-30, yoffset=-55, visible=False)
    S = UIImage("UI/Data/S.png", align="right", valign="center",
                xoffset=-30, yoffset=-55, visible=False)
    Z = UIImage("UI/Data/Z.png", align="right", valign="center",
                xoffset=-30, yoffset=-55, visible=False)
    J = UIImage("UI/Data/J.png", align="right", valign="center",
                xoffset=-30, yoffset=-55, visible=False)
    L = UIImage("UI/Data/L.png", align="right", valign="center",
                xoffset=-30, yoffset=-55, visible=False)
    nextblock = UIText("", size=32, align="right",
                       valign="center", xoffset=-30, yoffset=-60, visible=True)
    _uiNames["nextblock"] = nextblock
    _uiObjects.append(nextblock)

    _uiObjects.append(helloworld)
    _uiObjects.append(scoretag)
    _uiObjects.append(score)
    _uiNames["score"] = score
    _uiObjects.append(preview)
    _uiObjects.append(_paused)
    # _uiObjects.append(I)
    # _uiObjects.append(O)
    # _uiObjects.append(T)
    # _uiObjects.append(S)
    # _uiObjects.append(Z)
    # _uiObjects.append(J)
    # _uiObjects.append(L)

    UICommon.Blocks = {"I": I,
                       "O": O,
                       "T": T,
                       "L": L,
                       "S": S,
                       "J": J,
                       "Z": Z}


def Update(deltaTime):
    global _uiObjects
    global _tetris
    global _paused

    for i in _uiObjects:
        i.Update(deltaTime)
        if UICommon.Paused:
            i.visible = False
        else:
            i.visible = True
    for i in UICommon.Blocks.values():
        i.Update(deltaTime)
        # print(i.path + str(i.visible))


def Render():
    global _uiObjects
    global _tetris

    # glPushMatrix()
    for i in _uiObjects:
        i.Render()
    for i in UICommon.Blocks.values():
        i.Render()

    _tetris.Render()
    # glPopMatrix()


def Cleanup():
    pass


def GetElementByID(id):
    global _uiIds
    return _uiIds[id]


def GetElementByName(name):
    global _uiNames
    return _uiNames[name]
