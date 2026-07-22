import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# prime of form 4k+1
p = 41

# Generate all natural solutions (x, y, z) such that x^2 + 4yz = p
S = []
for y in range(1, p):  # positive integers
    for x in range(1, p):
        z = (p - x**2) / (4*y)
        if z.is_integer() and z > 0:
            S.append((x, y, int(z)))

S = np.array(S)

# Define the Zagier involution
def zagier(x, y, z):
    if (2*y > x) and (z + x > y):
        return (2*y - x, y, z + x - y)  # central region
    elif (x > 2*y) and (z + x > y):
        return (x - 2*y, z + x - y, y)  # left region
    elif (y > x + z):
        return (x + 2*z, z, y - x - z)  # right region

# Plot
fig = plt.figure(figsize=(10,8))
ax = fig.add_subplot(111, projection='3d')

colors = {'central':'#9ab5ff', 'left':'#87ff78', 'right':'#b00b69'}

# Iterate over each point in the list of psuedo-Pythagorean triples
# For each point, calculate its Zagier involution image
# It then determines which case the point fell into.
# It then plots the point, then draws an arrow to its image (as long as not fixed point)
for point in S:
    x, y, z = point
    x_new, y_new, z_new = zagier(x, y, z)
    
    # Determine region
    if (2*y > x) and (z + x > y):
        region = 'central'
    elif (x > 2*y) and (z + x > y):
        region = 'left'
    else:
        region = 'right'
    
    # Plot point
    ax.scatter(x, y, z, color=colors[region], s=50)
    
    # Draw arrow to its image
    if (x_new, y_new, z_new) != (x, y, z):
        ax.quiver(x, y, z, x_new-x, y_new-y, z_new-z,
              color=colors[region], length=1.0, normalize=True, alpha=0.5)

# Plot fixed point
fixed_point = (1, 1, (p - 1)//4)
ax.scatter(*fixed_point, color='red', s=80, label='Unique fixed point')

# Labels and camera
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
ax.set_title(f'Discrete natural solutions of x^2 + 4yz = {p} with inv1 mapping')
ax.legend()
ax.view_init(elev=30, azim=180)
ax.grid(True)
plt.show()