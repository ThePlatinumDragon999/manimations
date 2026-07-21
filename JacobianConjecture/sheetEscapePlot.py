import numpy as np
import matplotlib.pyplot as plt

# Create a grid for our input plane (the floor).
# We start slightly away from 0 (r = 0.05) because at exactly 0, 
# the second sheet is already at infinity and would crash the math!
r = np.linspace(0.05, 2, 100)
theta = np.linspace(-np.pi, np.pi, 100)
R, Theta = np.meshgrid(r, theta)

# Calculate the complex input coordinates (Z_in)
Z_in = R * np.exp(1j * Theta)
X = np.real(Z_in)  # The X-axis of our floor
Y = np.imag(Z_in)  # The Y-axis of our floor

# The function is z*w^2 + w - 1 = 0.
# Using the quadratic formula, the output (w) has two answers:
# w = (-1 +/- sqrt(1 + 4z)) / (2z)
sqrt_term = np.sqrt(1 + 4 * Z_in)

# Branch 1: The "Safe" Sheet (using the + square root)
W1 = (-1 + sqrt_term) / (2 * Z_in)
Z_out1 = np.real(W1)

# Branch 2: The "Escaping" Sheet (using the - square root)
W2 = (-1 - sqrt_term) / (2 * Z_in)
Z_out2 = np.real(W2)

# Set up the 3D plot
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

# Plot the safe sheet (Top sheet, approaches height 1)
surf1 = ax.plot_surface(X, Y, Z_out1, cmap='Greens', alpha=0.9, 
                        edgecolor='none', label="Safe Sheet")

# Plot the escaping sheet (Bottom sheet, drops to -infinity)
surf2 = ax.plot_surface(X, Y, Z_out2, cmap='Reds', alpha=0.8, 
                        edgecolor='none', label="Escaping Sheet")

# Add a vertical dotted line pointing down the "infinity pit" at the origin
ax.plot([0, 0], [0, 0], [1, -10], color='black', linestyle='--', linewidth=2)
# Add a dot at (0,0,1) to show exactly where the safe sheet crosses
ax.scatter([0], [0], [1], color='black', s=50, zorder=10)

# Limit the Z-axis so the graph doesn't warp trying to draw infinity
ax.set_zlim(-10, 3)

# Labels and aesthetics
ax.set_title("Sheets Escaping to Infinity: z \u00B7 w\u00B2 + w - 1 = 0", fontsize=14)
ax.set_xlabel("Input: Real Part (X)")
ax.set_ylabel("Input: Imaginary Part (Y)")
ax.set_zlabel("Output: Real Part (Height)")

# To make the graph look cleaner, hide the background grid planes
ax.xaxis.pane.fill = False
ax.yaxis.pane.fill = False
ax.zaxis.pane.fill = False

plt.show()