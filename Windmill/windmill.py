import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# prime of form 4k+1
p = 37

# Generate all natural solutions (x, y, z)
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
    else:
        return None

# Plot
fig = plt.figure(figsize=(10,8))
ax = fig.add_subplot(111, projection='3d')

colors = {'central':'skyblue', 'left':'lightgreen', 'right':'orange'}

for point in S:
    x, y, z = point
    target = zagier(x, y, z)
    if target:
        x_new, y_new, z_new = target
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
        if target and (x_new, y_new, z_new) != (x, y, z):
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