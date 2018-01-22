"""A tool designed to overlay points onto an image of the field to assist in getting co-ordinates"""
import os
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
from math import degrees
from scipy.misc import imread
import numpy as np
__location__ = os.path.realpath(
   os.path.join(os.getcwd(), os.path.dirname(__file__)))
   # Sets the directory to where the current file is being run from
fig, ax = plt.subplots()

DATAFILE = cbook.get_sample_data(os.path.join(__location__, 'g152972.png'))
IMAGE = imread(DATAFILE)
plt.imshow(IMAGE, extent=[0, 1646, -411.5, 411.5])

# Enter co-ordinates here
POINTS = [[0, -300, 1.5708], [800, -225,3], [610, -250,43], [525, -180,22], [750, -200,43]]

X_VALUE = []
Y_VALUE = []
PHI=[]




#phi = [2,3,4,2,43]

POINT_NUMBER = []
for i in range(len(POINTS)):
   X_VALUE.append(POINTS[i][0])
   Y_VALUE.append(POINTS[i][1])
   #converts radians to degrees
   PHI.append(degrees(POINTS[i][2]))
   POINT_NUMBER.append(i)
# Splits the point into an x and y component and adds it to 2 seperate lists
# For each list inside the  POINTS list, divide them into thier x and y components
# and add them to seperate lists. The POINT NUMBER list is the index of each point
# to help with ordering

#ignore this is just array of 1's
U = V = np.ones_like(X_VALUE)

ax.quiver(X_VALUE, Y_VALUE, U, V, angles=PHI,color='red')

#plt.scatter(X_VALUE, Y_VALUE, color='red')
for i, txt in enumerate(POINT_NUMBER):
   plt.annotate(txt, (X_VALUE[i], Y_VALUE[i]), color='blue')
plt.show()
# This bit actually does the plotting