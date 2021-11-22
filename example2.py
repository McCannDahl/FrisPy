# %% [markdown]
# # Visualizing a trajectory
# 
# Let's make some figures to visualize the trajectory of a disc's flight path. Let's simulate a slow and a fast throw so that we can make comparisons.

# %%
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D # <--- This is important for 3d plotting 
from frispy.disc import all_MccDiscs
plt.rc("font", size=14, family="serif")

# %%
# Negative theta is an airbounce
discs = all_MccDiscs
i = 0
for mccdisc in discs:
    mccdisc.disc.set_default_initial_conditions(vx=23, vy=0, theta=0, phi=0.2)
    mccdisc.disc.reset_initial_conditions()
    i += 1
# %%
results = []
for mccdisc in discs:
    results.append(mccdisc.disc.compute_trajectory(flight_time=4))


# %%
fig, ax = plt.subplots(ncols=1, nrows=3, sharex=True)
plt.subplots_adjust(hspace=0.01)

for res in results:
    ax[0].plot(res.times, res.phi)
    ax[1].plot(res.times, res.theta)
    ax[2].plot(res.times, res.gamma)

ax[0].set_ylabel(r"Azimuthal angle $\phi$ [rad]")
ax[1].set_ylabel(r"Polar angle $\theta$ [rad]")
ax[2].set_ylabel(r"Spin angle $\gamma$ [rad]")
ax[2].set_xlabel("Time [s]", size=20)

fig.set_size_inches(10, 10)
plt.show()

# %%
phi = results[0].phi[50]
theta = results[0].theta[50]
r = discs[0].disc.eom.rotation_matrix_from_phi_theta(phi, theta)
print(r)

# %%
from matplotlib.tri import Triangulation
def get_edge(radii, n=20):
    alpha = np.linspace(0, 2*np.pi, n)
    r = radii * np.ones(n)
    x = r * np.cos(alpha)
    y = r * np.sin(alpha)
    z = np.zeros(n)
    return np.array([x, y, z]).T
edge = get_edge(discs[0].disc.eom.diameter / 2 * 10)
edge_T = edge @ r

# %%
fig = plt.figure()
ax = fig.add_subplot(projection="3d")
i = 0
for result in results:
    ax.plot(result.x, result.y, result.z, label=discs[i].name)
    i += 1
ax.legend()

ax.plot_trisurf(edge_T[:, 0] + results[0].x[50], edge_T[:, 1] + results[0].y[50], edge_T[:, 2] + results[0].z[50])
ax.set_xlim(0, 40)
ax.set_ylim(-20, 20)
ax.set_zlim(0, 10)

fig.set_size_inches(8, 8)
plt.show()
# %%



