"""A tool designed to overlay points onto an image of the field to assist in
getting co-ordinates"""
import os
import math
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
from scipy.misc import imread
import numpy as np

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
# Sets the directory to where the current file is being run from
FIG, AX = plt.subplots()
datafile = cbook.get_sample_data(os.path.join(__location__, "map.png"))
image = imread(datafile)
plt.imshow(image, extent=[0, 16.46, -4.115, 4.115])

point_no = 0


def h_to_r2(r_pos: list, lmda: list):
    """
    A function to convert the vector lmda in the h representation back to R^2 to allow
    for mapping and easy visulisation
    :param r_pos: [X, Y, heading] value of the position from which the icr should be
    plotted, heading is measured CCW from +x axis (+y is forwards)
    :param lmda: the location of the icr (or any other point) in the h representation
    used in libswervedrive. Passes x, y co-ordinates of lmda2, direction of travel if
    the ICR is infinite, position of the robot and robot heading onto plot_icr.
    """
    r_xy = np.array(r_pos[:2])
    if abs(lmda[2]) < 1e-3:
        theta = math.atan2(lmda[1], lmda[0])
        plot_icr(r_xy, theta, r_xy, r_pos[2])
    else:
        lmda = np.array(lmda)
        heading = r_pos[2]
        lmda = lmda[:2] / lmda[2]
        rotation = np.array(
            [
                [math.sin(heading), math.cos(heading)],
                [-math.sin(heading), math.cos(heading)],
            ]
        )
        lmda = rotation @ lmda
        plot_icr(lmda + r_xy, None, r_xy, r_pos[2])


def plot_icr(ICR: np.ndarray, theta: float, r_pos: list, r_theta: float):
    """
    A function that plots the given ICR onto a map of the field.
    It plots the ICR as a blue dot, the robot as a green arrow and the
    robots path around the ICR as a green circle.
    :param ICR: the x (away from alliance wall) and y co-ordinates of the ICR
    as an array 0, 0 is located in the centre of the aliance wall, x should
    never > 0
    :param theta: the angle in radians which the robot will face measured
    CCW from the +x axis note +y is forwards on the robot
    :param r_pos: the position of the robot in x,y plotted as a green arrow
    :param r_theta: the heading of the robot, determines direction of the
    robot arrow
    """
    global point_no
    point_no += 1
    # ICR x and y
    x = ICR[0]
    y = ICR[1]
    # robot x and y
    r_x = r_pos[0]
    r_y = r_pos[1]
    # theta and r_theta in degrees
    phi = 0
    r_phi = 0

    # ignore this is just array of 1's
    U = V = np.ones_like(x)

    # plots the icr arrow
    if theta is None:
        AX.plot(x, y, "b.")
    else:
        # converts radians to degrees
        phi = math.degrees(theta)
        AX.quiver(x, y, U, V, angles=phi, color="red")
    plt.annotate(point_no, (x, y), color="black")

    # plots the robot
    if r_theta is None:
        AX.plot(r_x, r_y)
    else:
        r_phi = math.degrees(r_theta)
        AX.quiver(r_x, r_y, U, V, angles=r_phi, color="green")
    # Add a circle showing the robots path around the ICR
    radius = np.linalg.norm(ICR - r_pos)
    circle = plt.Circle((x, y), radius, color="g", fill=False)
    AX.add_artist(circle)


h_to_r2([1, 1, math.pi], [0.5, 0.5, math.sqrt(2)])
h_to_r2([4, 1, 0], [1, 0, 0])
h_to_r2([3, -2, math.pi / 2], [0.58834841, 0.78446454, 0.19611614])
plt.show()
