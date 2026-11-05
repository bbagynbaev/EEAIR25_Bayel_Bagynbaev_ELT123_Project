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