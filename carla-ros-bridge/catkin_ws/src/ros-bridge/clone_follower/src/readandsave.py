import numpy as np
import csv



with open('/home/dianzhaoli/carla-ros-bridge/catkin_ws/src/ros-bridge/clone_follower/src/drivetest5.csv', newline='') as f:     
    vl = []
    vf = []
    a = []
    lead_a = []
    distance = []
    reader = csv.reader(f)
    for row in reader:
        vl_data = row[0]
        vf_data = row[1]
        #a_data = row[8]
        #lead_a_data =  row[11]
        distance_data = row[4]
        vl.append(vl_data)
        vf.append(vf_data)
        #a.append(a_data)
        #lead_a.append(lead_a_data)
        distance.append(distance_data) 
        
data = np.zeros((3,33036))        
        
for i in range(len(vl)):       
    data[0,i] = vl[i]
    data[1,i] = vf[i]
    #data[2,i] = a[i]      
    data[2,i] = distance[i]
    #data[4,i] = lead_a[i]
    
    
np.save("/home/dianzhaoli/carla-ros-bridge/catkin_ws/src/ros-bridge/clone_follower/src/drivetest5.csv",data)   



np.load("/home/dianzhaoli/carla-ros-bridge/catkin_ws/src/ros-bridge/clone_follower/src/drivetest5.npy")   

data2 = data[0]  


