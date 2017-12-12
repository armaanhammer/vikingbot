# vikingbot-remote-control

This project is developed to facilitate ostacle avoidance for the humanoid robot HROS1.

We collaberated with three groups to work on this project:
  * https://github.com/vivanbhalla/Dancing-Hexapod for using sockets to communicate between Python scripts on the laptop and robot and for rudimentary OpenCV implementation in Python.
  * https://github.com/cvsandeep/vikingbot for motor control of the VikingBot.
  * https://github.com/Salyhakkoum/ECE-478 Ideals for more robust object tracking and route following which we hope to implement soon.
  
  

Our control structure is:
  * Camera mounted on VikingBot connected to laptop
  * VikingBot runs: 
    * vikingbot_server_if.py which:
      * allows laptop to control it by making calls to motor_controller.py
      * returns status messages to laptop
  * Laptop runs: 
      * object_detection_and_client_if.py which uses OpenCV to: 
        * watch through the webcam, 
        * determine obstacle locations, 
        * and send directives to the server running on the vikingbot. 
        
Once we make the OpenCV algorithms more robust in a setting with two degrees of freedom (allowing the scene to move left and right in the X and Y spatial dimensions, on the VikingBot), we will modify the project for three degrees of freedom (adding compenation for the scene to move up and down in the Z spatial dimension, on the HROS1).

