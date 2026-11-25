import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt


#chem source position
source = np.array([0.0, 0.0])

#cell starting positions
cell_A = np.array([3.0, 0.0])
cell_B = np.array([-3.0, 0.0])

#settings for simulation, can be changed
step_size = 0.1
number_of_steps = 500

#sensing accuracy
sigma_A = 5
sigma_B = 60

#graph path
path_A = [cell_A.copy()]
path_B = [cell_B.copy()]

rng = np.random.default_rng(42)

#movement func of cell
def move_cell(position, sigma):
    direction = source - position

    theta = np.arctan2(direction[1], direction[0])
    error = rng.normal(0, sigma)
    theta = theta + np.deg2rad(error)

    movement = step_size * np.array([
        np.cos(theta),
        np.sin(theta)
    ])

    return position + movement

for step in range(number_of_steps):

    cell_A = move_cell(cell_A, sigma_A)
    cell_B = move_cell(cell_B, sigma_B)
    path_A.append(cell_A.copy())
    path_B.append(cell_B.copy())

path_A = np.array(path_A)
path_B = np.array(path_B)

plt.figure(figsize=(8, 7))
plt.scatter(0, 0, color="green", marker="*", s=200,
            label="Chemical source")
plt.plot(path_A[:, 0], path_A[:, 1],
         color="blue", label="Cell A (imperfect sensing)")
plt.plot(path_B[:, 0], path_B[:, 1],
         color="orange", label="Cell B (perfect sensing)")

plt.xlabel("x position")
plt.ylabel("y position")
plt.title("Basic Cell Movement Simulation")
plt.grid(True)
plt.legend()
plt.axis("equal")
plt.show()