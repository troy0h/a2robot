# a2robot
A ROS 2 project, made to move a robotic vehicle autonomously.
Utilizes a TensorFlow Keras model for image recognition, created using Teachable Machines.

## Folders
Inside the folder named `a2robot`, the source code files can be found.
`arduinoControl.py` contains code used to control the robot itself.
`camera.py` contains code used to get a webcam frame, output it to the screen, and send the image to the `detectImage` node.
`detectImage.py` contains code for the Keras model to detect things found in the webcam frame, and sends instructions to the `arduinoControl` node based on what is found.
The `ArduinoCode` folder contains the Arduino code needed to move the robotic vehicle.

The `resource` folder contains the Keras model, a text file containing labels to name the images recognised, and two more folders, full of images that were trained on.

