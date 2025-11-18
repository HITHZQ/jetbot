# jetbot
## part1--5 tasks
1. JetBot Hardware and Software Environment Configuration  
   Understand the hardware components of the JetBot and their functions;  
   Configure the virtual machine environment and establish an SSH remote connection to the JetBot. Set up the network connection between the JetBot and the virtual machine to ensure they operate within the same network.  

2. Workspace Creation  
   Create a new workspace in the JetBot;  
   Configure environment variables.  

3. NFS Mounting and Program Development  
   Mount the JetBot's ROS workspace to the virtual machine via NFS.  
   Compile and run a keyboard control program for the JetBot.  

4. Topic Mechanism  
   Execute the JetBot initialization program, and use tools such as `rostopic` and `rqt` to view the topics, nodes, and other information of the JetBot.  

5. SLAM Implementation and Visualization  
   Run the SLAM program and use Rviz for SLAM visualization. Load configuration files in Rviz to monitor the JetBot's real-time positioning and map-building process in the environment, and analyze the results.  
   Compare four 2D mapping algorithms and 3D mapping algorithms.

<img width="992" height="1056" alt="Gemini_Generated_Image_1xbob31xbob31xbo" src="https://github.com/user-attachments/assets/a9a3ae45-6133-417d-b192-0361a7a0b096" />

time-online picture
<img width="1806" height="778" alt="屏幕截图 2024-10-20 153225" src="https://github.com/user-attachments/assets/9a0d4197-493e-420e-9c11-51ed13cd6a8e" />

3d-mapping
<img width="1055" height="550" alt="屏幕截图 2024-10-20 162557" src="https://github.com/user-attachments/assets/628b2388-8843-46be-b2a2-74a2d4eb8c3a" />



## part2--4 tasks
1.  Open the maps built in the first session individually.
   
2.  Place the JetBot at the starting position on the map and assign a target point, enabling it to navigate towards the target while avoiding obstacles. The requirements are as follows:
    (1) Use the Dijkstra algorithm and the A* algorithm respectively as the global path planning algorithms.
    (2) Use the DWA algorithm and the TEB algorithm respectively as the local obstacle avoidance algorithms.
    
3.  Compare the navigation performance of different global path planning algorithms and different local obstacle avoidance algorithms across various maps.
   
4.  Based on the provided parameter configuration files, adjust the experimental parameters and compare the experimental results under different parameter settings.

Dijkstra +TEB 

<img width="692" height="323" alt="image" src="https://github.com/user-attachments/assets/d439dbf2-27b6-4298-a7a5-10dc60670f6a" />

A*+TEB 

<img width="691" height="303" alt="image" src="https://github.com/user-attachments/assets/cdd2bbdf-1d1e-46e2-964c-8e42fb4c29d3" />

Dijkstra +DWA

<img width="692" height="319" alt="image" src="https://github.com/user-attachments/assets/615a1575-c01f-4fd1-9cf8-988cfe5e266c" />

A*+DWA 

<img width="692" height="311" alt="image" src="https://github.com/user-attachments/assets/8291794f-f41c-4b72-9040-cb69ad7b535a" />



## part3--3 tasks

1.  Dataset Annotation
   
    (1) Data Collection
    
    Collect image data containing the target objects. These images will be used to train the YOLOv10 model.
    
    (2) Dataset Annotation
    
    Use the LabelImg tool for data annotation:
    
    *   Open LabelImg and load the collected image data.
    *   Draw bounding boxes around the target object in each image.
    *   Assign a target class to each marked bounding box.
    *   Save the annotation files (typically in XML or TXT format; choose the appropriate format required for YOLOv10 training).

3.  YOLOv10 Model Training and Detection
   
    (1) Model Training:
    
    *   Initialize the parameter configuration for the YOLOv10 model, such as learning rate and batch size.
    *   Import the annotated dataset.
    *   Perform model training using a deep learning framework (such as TensorFlow or PyTorch).
    *   Save the trained model weights.
    
    (2) Target Detection:

    *   Use the trained YOLOv10 model for real-time target detection.
    *   Input camera stream data, process it, and output the detection results.
    *   Display the bounding boxes and class labels of the target objects.

4.  Target Tracking
   
    (1) Tracking Algorithm Implementation
    
    Implement a target tracking algorithm based on the detection results.
    
    (2) JetBot Control:
    
    *   Convert the tracking results into motion control commands for the JetBot.
    *   Test the JetBot's automatic tracking performance after a target is detected.

labeling

<img width="613" height="359" alt="image" src="https://github.com/user-attachments/assets/c770a86a-c7d1-4416-903c-1d276bf78ff6" />

training

<img width="613" height="233" alt="image" src="https://github.com/user-attachments/assets/dc456e90-db4b-4396-81d2-fade969e87da" />

result

<img width="604" height="403" alt="image" src="https://github.com/user-attachments/assets/32b51b62-0143-45d1-9bd0-cbe1bc676355" />

<img width="621" height="414" alt="image" src="https://github.com/user-attachments/assets/5ad92877-5978-4a22-9bbd-77a00b90b36e" />

<img width="614" height="409" alt="image" src="https://github.com/user-attachments/assets/84d21b72-d1c2-46bd-a001-820005bb65c8" />

<img width="614" height="409" alt="image" src="https://github.com/user-attachments/assets/b5c00423-459e-4591-9f89-6d93ec1f4f17" />

<img width="685" height="343" alt="image" src="https://github.com/user-attachments/assets/673ac86a-8d4b-46ec-ac7d-0b509ca74b55" />

<img width="664" height="664" alt="image" src="https://github.com/user-attachments/assets/48b5d2f8-2142-4b8b-b4a2-b1a859a50f88" />


## part4--1 tasks

follow & catch

<img width="700" height="700" alt="image" src="https://github.com/user-attachments/assets/8c35bc01-c6e1-46ca-b033-b31727b3d3c4" />




