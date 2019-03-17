from OpenGL.GL import *
from OpenGL.GLUT import *
import numpy as np
from math import *


# each curve is represented as an arc defined by its center
# and angles between which the arc is

# processes given curves' outline (0), interior (1)
def drawAllCurves(curves):
    drawCurves(curves, 0)
    drawCurves(curves, 1)
    return


# draws given sequence of curves
def drawCurves(curves, interior):
    glBegin(GL_POLYGON) if interior else glBegin(GL_LINE_LOOP)
    for i in range(len(curves)):
        curve = curves[i]
        cirCx = curve[0]
        cirCy = curve[1]
        r = curve[2]
        st = curve[3]
        en = curve[4]
        if st - en > 180:
            st -= 360
        if en - st > 180:
            en -= 360
        nxtCurve = curves[(i + 1) % len(curves)]
        nxtCirCx = nxtCurve[0]
        nxtCirCy = nxtCurve[1]
        nxtR = nxtCurve[2]
        nxtSt = nxtCurve[3]
        nxtEn = nxtCurve[4]
        p1x, p1y = getPnt(cirCx, cirCy, r, st)
        nxtP1x, nxtP1y = getPnt(nxtCirCx, nxtCirCy, nxtR, st)
        nxtP2x, nxtP2y = getPnt(nxtCirCx, nxtCirCy, nxtR, en)
        if (abs(p1x - nxtP1x) < 1e-9 and abs(p1y - nxtP1y) < 1e-9) or (
                abs(p1x - nxtP2x) < 1e-9 and abs(p1y - nxtP2y) < 1e-9):
            st, en = en, st
        clr = curve[5] if interior else curve[6]
        nxtClr = curves[(i + 1) % len(curves)][5] if interior else curves[(i + 1) % len(curves)][6]
        step = ((en - st) / abs(en - st)) / 3
        for theta in np.arange(st, en, step):
            done = abs((theta - st) / (en - st))
            curClr = []
            [curClr.append(clr[j] * (1 - done ** 2) + nxtClr[j] * done ** 2) for j in range(4)]
            glColor(curClr[0], curClr[1], curClr[2], curClr[3])
            glVertex(cirCx + r * cos(theta * pi / 180), cirCy + r * sin(theta * pi / 180))

    glEnd()


# returns the point on the given circle that makes the given angle with its center
def getPnt(cx, cy, r, angle):
    return cx + r * cos(angle * pi / 180), cy + r * sin(angle * pi / 180)


# creates a curve that goes from p1 to p2, and has radius r
def getCircle(x1, y1, x2, y2, r, intClr=[1, 1, 1, 1], outClr=[0, 0, 0, 1]):
    r = max(r, sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) / 2)
    x3 = x2 - x1
    y3 = y2 - y1
    x3, y3 = -y3, x3
    l = sqrt(x3 ** 2 + y3 ** 2)
    x3, y3 = x3 / l, y3 / l
    distToCtr = sqrt(r ** 2 - (l / 2) ** 2)
    x4 = (x1 + x2) / 2 + distToCtr * x3
    y4 = (y1 + y2) / 2 + distToCtr * y3
    return [x4, y4, r, atan2(y1 - y4, x1 - x4) * 180 / pi, atan2(y2 - y4, x2 - x4) * 180 / pi, intClr, outClr]


# draws a circle given it's center and radius
def drawCircle(cx, cy, r, clr=[0, 0, 0, 1]):
    glColor(clr[0], clr[1], clr[2], clr[3])
    glBegin(GL_POLYGON)
    [glVertex(cx + r * cos(theta * pi / 180), cy + r * sin(theta * pi / 180)) for theta in range(1, 360)]
    glEnd()


def draw():
    glClearColor(1, 1, 1, 1)
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(1, 0, 0.3)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glLineWidth(4)
    glBegin(GL_QUADS)
    # background
    for theta in range(0, 360, 10):
        glColor(.7, .3, 0) if theta % 20 == 0 else glColor(1, .8, .2)
        glVertex(0, 0)
        glVertex(2 * cos(theta * pi / 180), 2 * sin(theta * pi / 180))
        glVertex(2 * cos((theta + 10) * pi / 180), 2 * sin((theta + 10) * pi / 180))
        glVertex(0, 0)
    glEnd()
    yellow = [[.9, .70, .15, 1], [1, .862, .278, 1], [1, .962, .378, 1]]
    brown = [.75, .2, .05, 1]
    black = [0, 0, 0, 1]
    red = [.9, .1, .1, 1]
    lightRed = [.9, .5, .5, 1]
    # tail
    curves = []
    curves.append(getCircle(-.295, .317, -.866, .712, 2.5, yellow[1], black))
    curves.append(getCircle(-.866, .712, -.887, .206, 2, yellow[2], black))
    curves.append(getCircle(-.887, .206, -.361, .024, 2.7, yellow[1], black))
    curves.append(getCircle(-.361, .024, -.295, .317, 2.7, yellow[1], black))
    drawAllCurves(curves)
    curves = []
    curves.append(getCircle(-.361, .024, -.64, -.282, 2.5, yellow[1], black))
    curves.append(getCircle(-.64, -.282, -.5, -.33, 2, yellow[1], black))
    curves.append(getCircle(-.5, -.33, -.548, -.47, 2.7, yellow[1], black))
    curves.append(getCircle(-.548, -.47, -.42, -.505, 2.7, yellow[1], black))
    curves.append(getCircle(-.42, -.505, -.361, .024, 2.7, yellow[0], black))
    drawAllCurves(curves)
    curves = []
    curves.append(getCircle(-.512, -.3666, -.548, -.47, 2.5, brown, black))
    curves.append(getCircle(-.548, -.47, -.41, -.506, 2, brown, black))
    curves.append(getCircle(-.41, -.506, -.407, -.403, 2.7, brown, black))
    curves.append(getCircle(-.407, -.403, -.458, -.335, 2.7, brown, black))
    curves.append(getCircle(-.458, -.335, -.512, -.3666, 2.7, brown, black))
    drawAllCurves(curves)
    # ears
    curves = []
    curves.append(getCircle(-.735, .96, -.237, .434, 1.1, yellow[2], black))
    curves.append(getCircle(-.237, .434, -.735, .96, .6, yellow[1], black))
    drawAllCurves(curves)
    curves = []
    curves.append(getCircle(-.738, .965, -.48, .60, 1.1, [0, 0, 0, .95], [0, 0, 0, 0]))
    curves.append(getCircle(-.48, .60, -.583, .92, .8, [0, 0, 0, .5], [0, 0, 0, 0]))
    curves.append(getCircle(-.583, .92, -.738, .965, .9, [0, 0, 0, .95], [0, 0, 0, 0]))
    drawAllCurves(curves)
    curves = []
    curves.append(getCircle(.492, 1.12, .25, .383, .8, yellow[2], black))
    curves.append(getCircle(.25, .383, .492, 1.12, .7, yellow[1], black))
    drawAllCurves(curves)
    curves = []
    curves.append(getCircle(.492, 1.12, .3465, .939, .7, [0, 0, 0, .95], [0, 0, 0, 0]))
    curves.append(getCircle(.3465, .939, .454, .642, .8, [0, 0, 0, .95], [0, 0, 0, 0]))
    curves.append(getCircle(.454, .642, .492, 1.12, .7, [0, 0, 0, .5], [0, 0, 0, 0]))
    drawAllCurves(curves)
    # head
    curves = []
    curves.append(getCircle(.28, .567, -.32, .565, .45, yellow[2], black))
    curves.append(getCircle(-.32, .565, -.262, -.054, .4, yellow[2], black))
    curves.append(getCircle(-.262, -.054, .21, -.064, .7, yellow[1], [0, 0, 0, 0]))
    curves.append(getCircle(.21, -.064, .28, .567, .4, yellow[1], [0, 0, 0, 0]))
    drawAllCurves(curves)
    # eyes
    drawCircle(.209, .372, .075, black)
    drawCircle(.1985, .40, .04, [1, 1, 1, .9])
    drawCircle(.24, .37, .05, [1, 1, 1, .3])
    drawCircle(-.237, .3744, .075, black)
    drawCircle(-.234, .40, .04, [1, 1, 1, .9])
    drawCircle(-.21, .36, .05, [1, 1, 1, .3])
    # mouth
    curves = []
    curves.append(getCircle(-.002, .25, -.11, .220, .3, red, black))
    curves.append(getCircle(-.11, .220, -.001, .108, .1, red, black))
    curves.append(getCircle(-.001, .108, .097, .225, .1, red, black))
    curves.append(getCircle(.097, .225, -.002, .25, .3, red, black))
    drawAllCurves(curves)
    curves = []
    curves.append(getCircle(-.1, .1696, .09, .1724, .1, lightRed, [0, 0, 0, .9]))
    curves.append(getCircle(.09, .1724, -.1, .1696, .15, [1, .6, .6, 1], [0, 0, 0, .9]))
    drawAllCurves(curves)
    curves = []
    curves.append(getCircle(-.18, .23, -.002, .26, .3, [0, 0, 0, 0], black))
    curves.append(getCircle(-.002, .26, .18, .23, .3, [0, 0, 0, 0], black))
    curves.append(getCircle(.18, .23, .18, .231, 0, [0, 0, 0, 0], black))
    curves.append(getCircle(.18, .231, -.18, .231, 0, [0, 0, 0, 0], [0, 0, 0, 0]))
    curves.append(getCircle(-.18, .231, -.18, .23, 0, [0, 0, 0, 0], [0, 0, 0, 0]))
    drawAllCurves(curves)
    # cheeks
    curves = []
    curves.append(getCircle(.405, .272, .256, .24, .08, red, [0, 0, 0, 1]))
    curves.append(getCircle(.256, .24, .355, .079, .15, red, [0, 0, 0, .8]))
    curves.append(getCircle(.355, .079, .405, .272, .5, lightRed, [0, 0, 0, .7]))
    drawAllCurves(curves)
    curves = []
    curves.append(getCircle(-.39, .077, -.303, .299, .13, lightRed, [0, 0, 0, .7]))
    curves.append(getCircle(-.303, .299, -.438, .245, .08, red, [0, 0, 0, 1]))
    curves.append(getCircle(-.438, .245, -.39, .077, .4, red, [0, 0, 0, .8]))
    drawAllCurves(curves)
    # legs
    curves = []
    curves.append(getCircle(-.33, -.761, -.455, -.871, .11, yellow[2], black))
    curves.append(getCircle(-.455, -.871, -.2, -.787, .15, yellow[1], black))
    drawAllCurves(curves)
    curves = []
    curves.append(getCircle(.455, -.871, .33, -.761, .11, yellow[2], black))
    curves.append(getCircle(.2, -.787, .455, -.871, .15, yellow[1], black))
    drawAllCurves(curves)
    # body
    curves = []
    curves.append(getCircle(.0, -.07, 0, -.84, 10, yellow[1], [0, 0, 0, 0]))
    curves.append(getCircle(0, -.84, 0, -.8401, 10, yellow[1], [0, 0, 0, 0]))
    curves.append(getCircle(0, -.84, .249, -.804, .4, yellow[1], black))
    curves.append(getCircle(.249, -.804, .44, -.639, .3, yellow[1], black))
    curves.append(getCircle(.44, -.639, .39, -.24, .8, yellow[1], black))
    curves.append(getCircle(.39, -.24, .284, -.03, 1, yellow[1], [0, 0, 0, 0]))
    curves.append(getCircle(.284, -.03, .0, -.07, .8, yellow[1], [0, 0, 0, 0]))
    drawAllCurves(curves)
    curves = []
    curves.append(getCircle(0, -.84, .0, -.07, 10, yellow[1], [0, 0, 0, 0]))
    curves.append(getCircle(.0, -.07, -.284, -.03, .8, yellow[1], [0, 0, 0, 0]))
    curves.append(getCircle(-.284, -.03, -.39, -.24, 1, yellow[1], [0, 0, 0, 0]))
    curves.append(getCircle(-.39, -.24, -.44, -.639, .8, yellow[1], black))
    curves.append(getCircle(-.44, -.639, -.249, -.804, .3, yellow[1], black))
    curves.append(getCircle(-.249, -.804, 0, -.84, .4, yellow[1], black))
    curves.append(getCircle(0, -.8401, 0, -.84, 10, yellow[1], [0, 0, 0, 0]))
    drawAllCurves(curves)
    # hands
    curves = []
    curves.append(getCircle(.47, .153, .26, -.019, .35, yellow[2], black))
    curves.append(getCircle(.26, -.019, .22, -.154, .25, yellow[1], [0, 0, 0, 0]))
    curves.append(getCircle(.22, -.154, .308, -.242, .4, yellow[1], [0, 0, 0, 0]))
    curves.append(getCircle(.308, -.242, .4, -.259, .2, yellow[1], [0, 0, 0, 0]))
    curves.append(getCircle(.4, -.259, .583, -.021, .7, yellow[1], [0, 0, 0, 0]))
    curves.append(getCircle(.583, -.021, .47, .153, .115, yellow[2], black))
    drawAllCurves(curves)
    curves = []
    curves.append(getCircle(-.26, -.019, -.47, .153, .35, yellow[2], black))
    curves.append(getCircle(-.47, .153, -.583, -.021, .115, yellow[2], black))
    curves.append(getCircle(-.583, -.021, -.414, -.259, .7, yellow[1], [0, 0, 0, .5]))
    curves.append(getCircle(-.414, -.259, -.308, -.242, .2, yellow[1], [0, 0, 0, 0]))
    curves.append(getCircle(-.308, -.242, -.22, -.154, .4, yellow[1], [0, 0, 0, 0]))
    curves.append(getCircle(-.22, -.154, -.26, -.019, .25, yellow[1], [0, 0, 0, 0]))
    drawAllCurves(curves)
    # shade
    curves = []
    curves.append(getCircle(.25, 0, -.25, 0, .6, [1, .962, .378, 0], [0, 0, 0, 0]))
    curves.append(getCircle(-.25, 0, -.38, -.7, .9, [1, .962, .378, 0], [0, 0, 0, 0]))
    curves.append(getCircle(-.38, -.7, .35, -.7, .9, [1, .962, .378, .8], [0, 0, 0, 0]))
    curves.append(getCircle(.35, -.7, .25, 0, .7, [1, .962, .378, .4], [0, 0, 0, 0]))
    drawAllCurves(curves)
    glFlush()


glutInit()
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
glutInitWindowSize(800, 800)
glutCreateWindow(b"pika")
glutDisplayFunc(draw)
glutMainLoop()
