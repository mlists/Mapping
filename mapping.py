"""A tool designed to overlay points onto an image of the field to assist in getting co-ordinates"""
import os
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
from scipy.misc import imread
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
    # Sets the directory to where the current file is being run from

DATAFILE = cbook.get_sample_data(os.path.join(__location__, 'map.jpg'))
IMAGE = imread(DATAFILE)
plt.imshow(IMAGE, extent=[0, 165, -41, 41])

# Enter co-ordinates here
POINTS = [[1, 2], [3, 4]]

X_VALUE = []
Y_VALUE = []
POINT_NUMBER = []
for i in range(len(POINTS)):
    X_VALUE.append(POINTS[i][0])
    Y_VALUE.append(POINTS[i][1])
    POINT_NUMBER.append(i)
print(X_VALUE, Y_VALUE)
# Splits the point into an x and y component and adds it to 2 seperate lists
# For each list inside the  POINTS list, divide them into thier x and y components
# and add them to seperate lists. The POINT NUMBER list is the index of each point
# to help with ordering

plt.scatter(Y_VALUE, X_VALUE, color='red')
for i, txt in enumerate(POINT_NUMBER):
    plt.annotate(txt, (Y_VALUE[i], X_VALUE[i]), color='white')
plt.show()
# This bit actually does the plotting
