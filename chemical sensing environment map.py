import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import gaussian_filter

#create map
x = np.linspace (-2, 2, 100)
y= np.linspace(-2, 2, 100)
x, y = np.meshgrid(x, y)
rng = np.random.default_rng()

#map setup
fig, ax = plt.subplots()
z = np.exp(-x**2 - y**2)
heatmap = ax.imshow(z, extent = [-3, 3, -3, 3], origin = 'lower', cmap = 'viridis', vmin = 0, vmax = 1.2)
fig.colorbar(heatmap, ax=ax, label='Concentration')

moverandom_x, moverandom_y = 0.0, 0.0

#animation and updating data based off random fluctuations
def update(frame):
    global moverandom_x, moverandom_y, z
    t = frame / 20

    moverandom_x = 0.92 * moverandom_x + rng.normal(0,0.06)
    moverandom_y = 0.92 * moverandom_y + rng.normal(0,0.06)
    x0 = np.clip(moverandom_x, -2.5, 2.5)
    y0 = np.clip(moverandom_y, -2.5, 2.5)
    
    sigma = 0.8 + 0.15 * np.sin(t * 2.3) + rng.normal(0, 0.02)

    warp_x = gaussian_filter(rng.normal(0, 1.5, size=x.shape), sigma=6)
    warp_y = gaussian_filter(rng.normal(0, 1.5, size=y.shape), sigma=6)

    z = np.exp(-(((x + warp_x) - x0)**2 + ((y + warp_y) - y0)**2) / (2 * sigma**2))

    eddies = gaussian_filter(rng.normal(1.0, 1.8, size=z.shape), sigma=3)
    z = z * np.clip(eddies, 0.1, 2.0)

    sensor_noise = np.abs(rng.normal(0, 0.015, size = z.shape))
    z = np.clip(z + sensor_noise, 0, 1.2)

    heatmap.set_data(z)
    return [heatmap]

#start animation
ani = animation.FuncAnimation(fig, update, frames=200, interval=30, blit=True)
plt.title('Environment Test Heat Map')
plt.show()