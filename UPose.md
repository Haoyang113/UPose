# How UPose.py calculates joint angles from mediapipe data
This tutorial explains how to calculate joint angles from the x,y,z coordinates of a human skeleton such as the world coordinates produced by mediapipe. 

### Why do I need joint angles?
- Joint angles are representing a local rotation that is needed for animating avatars.
- They are also good posture descriptors because they are indicating how much an elbow is bent for example.
- Finally, they are also consistent for the same posture accross different people and they are location invariant.

### How many angles are in each joint?
- In each joint there is a local coordinate system, therefore we could rotate around x, y, and z, which are the three Euler angles.
- The image below shows the local coordinate system of an elbow, where the trajectory around x is shown in red, around y in green, and arouns z in blue. 
<img src="Screenshots/local_coordinate_system.png" alt="Your Scene Name" width="600"/>
