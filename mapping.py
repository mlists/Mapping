"""A tool designed to overlay points onto an image of the field to assist in
getting co-ordinates"""
import os
import math
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
from scipy.misc import imread
import numpy as np
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
# Sets the directory to where the current file is being run from
FIG, AX = plt.subplots()
DATAFILE = cbook.get_sample_data(os.path.join(__location__, 'g152972.png'))
IMAGE = imread(DATAFILE)
plt.imshow(IMAGE, extent=[0, 16.46, -4.115, 4.115])

point_no = 0


def h_to_r2(pos: list, lmda: list):
    """
    A function to convert the vector lmda in the h representation back to R^2 to allow
    for mapping and easy visulisation
    :param pos: [X, Y, heading] value of the position from which the icr should be
    plotted, heading is measured CCW from +x axis (+y is forwards)
    :param lmda: the location of the icr (or any other point) in the h representation
    used in libswervedrive
    :return: the x y co-ordinates of lmda2
    """
    robot_xy = np.array(pos[:2])
    if abs(lmda[2]) < 1e-3:
        theta = math.atan2(lmda[1], lmda[0])
        return [robot_xy, theta, pos]
    lmda = np.array(lmda)
    heading = pos[2]
    lmda = lmda[:2] / lmda[2]
    rotation = np.array([[math.sin(heading), math.cos(heading)], [-math.sin(heading), math.cos(heading)]])
    lmda = rotation @ lmda
    return [lmda + robot_xy, None, pos]


def plot(point: np.ndarray, theta=None, bot_pos=None):
    """
    A function that plots the given point onto a map of the field.
    It can plot x, y, heading points (red), ICRs (blue) and robots (green)
    :param point: the x (away from alliance wall) and y co-ordinates
    as an array 0, 0 is located in the centre of the aliance wall, x should
    never > 0
    :param theta: the angle in radians which the robot will face measured
    CCW from the +x axis note +y is forwards on the robot
    :param bot_pos: the position of the robot in x,y plotted as a green arrow
    useful if this is being used to plot the ICR
    """
    global point_no
    point_no += 1
    phi = 0
    bot_phi = 0
    x = point[0]
    y = point[1]

    # ignore this is just array of 1's
    U = V = np.ones_like(x)

    # plots the icr arrow
    if theta is None:
        AX.plot(x, y, 'b.')
    else:
        # converts radians to degrees
        phi = math.degrees(theta)
        AX.quiver(x, y, U, V, angles=phi, color='red')
    plt.annotate(point_no, (x, y), color='black')
    # plots the robot arrow if needed
    if bot_pos is not None:
        if bot_pos[2] is None:
            AX.plot(bot_pos[0], bot_pos[1], 'g.')
        else:
            bot_phi = math.degrees(bot_pos[2])
            AX.quiver(bot_pos[0], bot_pos[1], U, V, angles=bot_phi, color='green')
        plt.annotate(point_no, (bot_pos[0], bot_pos[1]), color='black')


plotables = [
    h_to_r2([1, -1, 0], [0.5, 0.5, math.sqrt(2)]),
    h_to_r2([1, 1, math.pi], [0.5, 0.5, math.sqrt(2)]),
    h_to_r2([4, 1, 0], [1, 0, 0]),
    [[7, -2], math.pi],
]
for i in range(len(plotables)):
    if len(plotables[i]) == 1:
        plot(plotables[i][0])
    elif len(plotables[i]) == 2:
        plot(plotables[i][0], plotables[i][1])
    elif len(plotables[i]) == 3:
        plot(plotables[i][0], plotables[i][1], plotables[i][2])
    else:
        raise "Incorrect number of arguments must be < 4 > 0"

plt.show()
