import numpy as np
import matplotlib.pyplot as plt 

node_coords = np.array([
    [15.0, 20.0],   
    [85.0, 25.0],   
    [45.0, 85.0]    
])

pm25_readings = np.array([185.0, 35.0, 70.0])

DUST_THRESHOLD = 50.0