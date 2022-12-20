import pygame
from OpenGL.GL import *
import numpy as np
import math
from math import pi

import UI.UI as UI
import UI.UICommon as UICommon

from TetrisPieces import *
import WorldCommon as WC
from Cube import Cube as Cube


def Init():
    global _block
    global _nextBlock

    _block = TetrisPieces()
    _nextBlock = TetrisPieces()
    WC.layers = [
        [[-1]*WC.BorderZ for i in range(WC.BorderY)]for j in range(WC.BorderX)]
    # UICommon.Blocks[_nextBlock.name].visible = True
    # global _curBlock
    global _fallingSpeed
    global _pos
    global score
    score = 0
    print("Next:" + _nextBlock.name)
    Nextblock = UI.GetElementByName("nextblock")
    Nextblock.text = _nextBlock.name
    # UICommon.Blocks[_order[-1]].visible = True
    _pos = np.asfarray([0, 0, 0])

    _fallingSpeed = 3


def ProcessEvent(event):
    global _block
    global _collectedcube
    global _rotationX
    global _rotationY
    global _rotationZ

    if event.type == pygame.KEYDOWN:
        if event.key in UICommon.keypressed:
            UICommon.keypressed[event.key] = True
            if UICommon.keypressed[pygame.K_ESCAPE]:
                UICommon.TogglePause = True
            # Only rotate when not pause
            if not UICommon.Paused:
                if UICommon.keypressed[pygame.K_UP]:
                    _block.z -= 1
                    if not _block.Collided():
                        _block.Reset()
                        _block.z += 1

                if UICommon.keypressed[pygame.K_DOWN]:
                    _block.z += 1
                    if not _block.Collided():
                        _block.Reset()
                        _block.z -= 1
                if UICommon.keypressed[pygame.K_LEFT]:
                    _block.x -= 1
                    if not _block.Collided():
                        _block.Reset()
                        _block.x += 1
                if UICommon.keypressed[pygame.K_RIGHT]:
                    _block.x += 1
                    if not _block.Collided():
                        _block.Reset()
                        _block.x -= 1
                if UICommon.keypressed[pygame.K_a]:
                    _block.rotation(0)
                    if not _block.Collided():
                        _block.Reset()
                        _block.rotation(0, -pi/2)
                if UICommon.keypressed[pygame.K_s]:
                    _block.rotation(1)
                    if not _block.Collided():
                        _block.Reset()
                        _block.rotation(1, -pi/2)
                if UICommon.keypressed[pygame.K_d]:
                    _block.rotation(2)
                    if not _block.Collided():
                        _block.Reset()
                        _block.rotation(2, -pi/2)
            return True
    elif event.type == pygame.KEYUP:
        if event.key in UICommon.keypressed:
            UICommon.keypressed[event.key] = False
            return True
    return False


def Update(deltaTime):
    global _block
    global _nextBlock
    global _fallingSpeed
    global score

    if not UICommon.Paused:
        # UICommon.Blocks[_order[-1]].visible = False
        _block.y -= _fallingSpeed * deltaTime

        if not _block.Collided():
            # collect block
            for x, xL in enumerate(_block.shape):
                for y, yL in enumerate(xL):
                    for z, el in enumerate(yL):
                        if el:
                            # round
                            WC.layers[x+_block.x][math.ceil(
                                y+_block.y)][z+_block.z] = _block.color

            cubetodestroy = []
            for y in range(WC.BorderY):
                # check from x acros z axis
                tmp = []
                for x in range(WC.BorderX):
                    for z in range(WC.BorderZ):
                        if WC.layers[x][y][z] == -1:
                            break
                    # this column is filled
                    else:
                        tmp += [(x, y, z) for z in range(WC.BorderZ)]

                # check from z acros x axis
                for z in range(WC.BorderZ):
                    for x in range(WC.BorderX):
                        if WC.layers[x][y][z] == -1:
                            break
                    # this row is filled
                    else:
                        tmp += [(x, y, z) for x in range(WC.BorderX)]
                tmp2 = []
                # check if whole layer is filled
                for x in range(WC.BorderX):
                    for z in range(WC.BorderZ):
                        if (x, y, z) not in tmp:
                            break
                    # this column is filled
                    else:
                        tmp2 += [(x, y, z) for z in range(WC.BorderZ)]
                for z in range(WC.BorderZ):
                    for x in range(WC.BorderX):
                        if (x, y, z) not in tmp:
                            break
                    else:
                        tmp2 += [(x, y, z) for x in range(WC.BorderX)]
                print(tmp2)
                if tmp2 != [] and len(tmp2) == WC.BorderX * WC.BorderZ * 2:
                    cubetodestroy += [cube for cube in tmp2]
                # tmp2 = []
                # for x in range(WC.BorderX):
                #     for z in range(WC.BorderZ):
                #         if (x,y,z) not in tmp:
                #             break
                #     ##this column is filled
                #     else:
                #         tmp2+=[(x,y,z) for z in range(WC.BorderZ)]
                # for z in range(WC.BorderZ):
                #     for x in range(WC.BorderX):
                #         if (x,y,z) not in tmp:
                #             break
                #     else:
                #         tmp2+=[(x,y,z) for x in range(WC.BorderX)]
                # print(tmp2)
                # if tmp2 != []:
                #     cubetodestroy+=[tmp2]
            # print(cubetodestroy)

            if len(cubetodestroy):
                UICommon.Score += 1200

                previous = (-1, -1, -1)
                # cubetodestroy.sort(reverse=True)
                cubetodestroy.sort()
                # move layer down after bottom one destroyed
                for x, y, z in cubetodestroy:
                    WC.layers[x][y][z] = WC.layers[x][y+1][z]
                    # UICommon.Tetris = True
                    # WC.layers[x][y+1][z]=-1
                # for x,y,z in cubetodestroy:
                #     if (x,y,z)==previous:continue
                #     previous=(x,y,z)
                #     for y in range(y-1):
                #         WC.layers[x][y][z]=WC.layers[x][y+1][z]
                #         # UICommon.Tetris = True
                #     WC.layers[x][y][z]=-1

            if UICommon.Tetris:
                Tetris = UI.GetElementByName("tetris")
                Tetris.displaytime = 0.5
                UICommon.Tetris = False

            _block = _nextBlock
            if not _block.Collided():
                # game end
                print("Gameover")
                # UI gameover
                _block.Render()
                pygame.display.flip()

                return "Gameover"
            # UICommon.Blocks[_block.name].visible = False
            _nextBlock = TetrisPieces()
            print("Next:" + _nextBlock.name)
            Nextblock = UI.GetElementByName("nextblock")
            Nextblock.text = _nextBlock.name
            # UICommon.Blocks[_nextBlock.name].visible = True
            # 2 lines 100, 3lines 300
            # a single line clear is worth 40 points, clearing four lines at once (known as a Tetris) is worth 1200 4*4 lines 36000
            # Score update
            Score = UI.GetElementByName("score")
            Score.text = str(UICommon.Score)


def Render():
    global _block
    global _pos

    # m = glGetDouble(GL_MODELVIEW_MATRIX)
    for x, xL in enumerate(WC.layers):
        for y, yL in enumerate(xL):
            for z, el in enumerate(yL):
                if el != -1:
                    # print(x,xL,y,yL,z,el)
                    component = Cube(
                        el, (x-WC.BorderX/2, y-WC.BorderY/2, z-WC.BorderZ/2))
                    component.Render()
    _block.Render()
    # glLoadMatrixf(m)
    # for cube in _collectedcube:
    #     cube.Render()
    #     # print(block.max)
    # m = glGetDouble(GL_MODELVIEW_MATRIX)
    # glTranslatef(*_pos)
    # _curBlock.Render()
    # glLoadMatrixf(m)
