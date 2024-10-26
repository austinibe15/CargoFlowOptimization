from flask import Flask, render_template_string  
import numpy as np  

app = Flask(__name__)  

# Constants  
L = 12.2  # Length of a 40ft container in meters  
W = 2.44  # Width of a 40ft container in meters  
V_AGV = 5.0  # Average speed of AGV in meters/minute  
V_crane = 2.0  # Average speed of yard crane in meters/minute  
T_lift = 1.0  # Average lift time in minutes  
T_reshuffle = 0.5  # Average reshuffle time in minutes  
N_containers = 100  # Total number of containers expected for delivery  

# Example distances (in meters) from quay cranes to stacking blocks  
d_ij = np.array([[50, 60], [70, 80]])  
# Probabilities of AGV transport for each quay crane to yard blocks  
P_ij = np.array([[0.7, 0.3], [0.4, 0.6]])  

# Example crane distances (in meters)  
d_seaside = np.array([10, 15])  # Distances for seaside cranes  
d_landside = np.array([20, 25])  # Distances for landside cranes  
P_seaside = np.array([0.6, 0.4])  # Probabilities for seaside cranes  
P_landside = np.array([0.5, 0.5])  # Probabilities for landside cranes  

# Calculate expected AGV travel time  
def calculate_expected_agv_time(P_ij, d_ij, V_AGV):  
    E_T_AGV = np.sum(P_ij * (d_ij / V_AGV))  # Aggregate expected travel time  
    return E_T_AGV  

# Calculate expected crane handling time  
def calculate_expected_crane_time(P_seaside, d_seaside, P_landside, d_landside, V_crane, T_lift, T_reshuffle):  
    E_T_crane_seaside = np.sum(P_seaside * (T_lift + T_reshuffle + (d_seaside / V_crane)))  
    E_T_crane_landside = np.sum(P_landside * (T_lift + T_reshuffle + (d_landside / V_crane)))  
    E_T_crane = E_T_crane_seaside + E_T_crane_landside  
    return E_T_crane  

# Estimate number of containers that can be offloaded  
def estimate_offloaded_containers(total_containers, expected_crane_time, expected_agv_time):  
    total_processing_time = expected_crane_time + expected_agv_time  # Total expected time per cycle  
    processing_capacity = total_containers / total_processing_time  # Containers processed per minute  
    return int(processing_capacity)  

@app.route('/')  
def home():  
    expected_agv_time = calculate_expected_agv_time(P_ij, d_ij, V_AGV)  
    expected_crane_time = calculate_expected_crane_time(P_seaside, d_seaside, P_landside, d_landside, V_crane, T_lift, T_reshuffle)  
 
    # Estimate how many containers can be offloaded  
    offloaded_containers = estimate_offloaded_containers(N_containers, expected_crane_time, expected_agv_time)  

    # Creating the HTML output  
    output = f"""  
    <html>  
    <head><title>Warehouse Optimization Output</title></head>  
    <body>  
        <h1>Warehouse Container Stacking Output</h1>  
        <p>Expected AGV Travel Time: {expected_agv_time:.2f} minutes</p>  
        <p>Expected Crane Handling Time: {expected_crane_time:.2f} minutes</p>  
        <p>Estimated Number of Containers that can be Offloaded: {offloaded_containers} containers</p>  
    </body>  
    </html>  
    """  
    return render_template_string(output)  

if __name__ == '__main__':  
    app.run(debug=True)