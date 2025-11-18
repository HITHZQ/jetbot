# jetbot
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
