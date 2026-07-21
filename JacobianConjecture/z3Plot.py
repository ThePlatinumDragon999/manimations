import numpy as np
import matplotlib.pyplot as plt

# Create a grid of parameters for our "answers" (the cube roots)
# r is the distance from the center, t is the angle
r = np.linspace(0.1, 2, 60)
t = np.linspace(0, 2 * np.pi, 120)
R, T = np.meshgrid(r, t)

# The z-axis is the real part of the answer.
# Using polar coordinates, the real part is R * cos(T)
Z = R * np.cos(T)

# 3. Calculate the corresponding inputs (X and Y)
# If the root has angle T and radius R, cubing it multiplies the angle by 3 
# and cubes the radius. 
# This naturally wraps the surface around the origin 3 times!
X = (R**3) * np.cos(3 * T)
Y = (R**3) * np.sin(3 * T)

# 4. Set up the 3D plot
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Plot the surface, using a colormap to make the height easy to see
surf = ax.plot_surface(X, Y, Z, cmap='plasma', edgecolor='none', alpha=0.9)

# 5. Add our "Vertical Skewer" line at X=8, Y=0
# This simulates looking for the cube roots of the real number 8
z_line = np.linspace(-3, 3, 100)
x_line = np.full_like(z_line, 8)
y_line = np.full_like(z_line, 0)
ax.plot(x_line, y_line, z_line, color='cyan', linewidth=3, label="Vertical Skewer at Input = 8")

# Plot the three specific points where the skewer pierces the surface
# The three real parts of the cube roots of 8 are 2, -1, and -1
ax.scatter([8, 8, 8], [0, 0, 0], [2, -1, -1], color='red', s=100, zorder=5, label="The 3 Roots")

# Labels and aesthetics
ax.set_title("Riemann Surface for the Cube Root (Inverse of z³)", fontsize=14)
ax.set_xlabel("Input: Real Part (X)")
ax.set_ylabel("Input: Imaginary Part (Y)")
ax.set_zlabel("Output: Real Part (Z)")
ax.legend()

plt.show()