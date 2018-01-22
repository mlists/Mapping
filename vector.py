import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots()

X, Y = np.meshgrid(np.arange(15), np.arange(10))
U = V = np.ones_like(X)
phi = (np.random.rand(15, 10) - .5) * 150
ax.quiver(X, Y, U, V, angles=phi)
print(phi)
plt.show()

