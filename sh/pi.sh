#/bin/bash

echo "Running the executable file for the PI."

# Change the root directory
cd "/home/pi/Desktop/Sign_Language_Neural/"

# Start the streaming service
./src/cameras/gst_source.sh &

# Run the main file
cd "src/controller/"
python3 main.py

# Retrieve the process ID of the camera and kill service
pid=$(pidof gst-launch-1.0)
sudo kill -9 $pid

# Disable all lights
python3 led.py 0

echo "Completed the execution file of the PI."
