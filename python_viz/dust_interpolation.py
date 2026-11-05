import numpy as np
import matplotlib.pyplot as plt 

node_coords = np.array([
    [15.0, 20.0],   
    [85.0, 25.0],   
    [45.0, 85.0]    
])

pm25_readings = np.array([185.0, 35.0, 70.0])

DUST_THRESHOLD = 50.0

def idw_interpolation(x_grid, y_grid, coords, values, power=2.0):

    grid_z = np.zeros(x_grid.shape)
    
    for i in range(x_grid.shape[0]):
        for j in range(x_grid.shape[1]):
            px = x_grid[i, j]
            py = y_grid[i, j]
            
            distances = np.sqrt((coords[:, 0] - px)**2 + (coords[:, 1] - py)**2)

            if np.any(distances == 0):
                grid_z[i, j] = values[np.argmin(distances)]
            else:
                weights = 1.0 / (distances ** power)
                grid_z[i, j] = np.sum(weights * values) / np.sum(weights)
                
    return grid_z

x_min, x_max = 0, 100
y_min, y_max = 0, 100

grid_x, grid_y = np.meshgrid(
    np.linspace(x_min, x_max, 200),
    np.linspace(y_min, y_max, 200)
)

grid_z = idw_interpolation(grid_x, grid_y, node_coords, pm25_readings, power=2.0)

fig, ax = plt.subplots(figsize=(9, 8))

contour_fill = ax.contourf(grid_x, grid_y, grid_z, levels=50, cmap='YlOrRd', alpha=0.85)
cbar = fig.colorbar(contour_fill, ax=ax)
cbar.set_label('Концентрация PM2.5 (мкг/м³)', fontsize=11, fontweight='bold')

boundary_line = ax.contour(
    grid_x, grid_y, grid_z, 
    levels=[DUST_THRESHOLD], 
    colors='red', 
    linewidths=2.5, 
    linestyles='--'
)
ax.clabel(boundary_line, fmt={DUST_THRESHOLD: f'Граница облака ({DUST_THRESHOLD} мкг/м³)'}, inline=True, fontsize=10)

triangle_x = np.append(node_coords[:, 0], node_coords[0, 0])
triangle_y = np.append(node_coords[:, 1], node_coords[0, 1])
ax.plot(triangle_x, triangle_y, 'b:', linewidth=1.5, label='3-Node Mesh Boundary (Зона высокой точности)')

ax.scatter(node_coords[:, 0], node_coords[:, 1], color='blue', s=120, zorder=5, edgecolors='black', label='Сенсорные узлы (ESP32 + SDS011)')

for i, (x, y) in enumerate(node_coords):
    ax.annotate(
        f'Node {i+1}\n{pm25_readings[i]} µg/m³', 
        (x, y), 
        textcoords="offset points", 
        xytext=(10, -5), 
        ha='left',
        fontsize=9,
        fontweight='bold',
        bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8)
    )