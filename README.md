# Gesture Detection Autonomous Robot
This repository was used for a class at Monash University (FIT3146 - Maker Lab) for developing a small rover that would be able to move forwards and backwards through detecting various hand gestures. For example, a thumbs-up would make the rover move forwards, while a thumbs-down would make the rover move backwards. Additionally, the rover had a distance sensor and LEDs for indicating various actions. The rover code ran on a Raspberri-Pi 3 model and was able to stream a camera feed (via GStreamer) to another laptop to perform the detection on opencv. The laptop would then respond to the Pi with the current detected symbol and the rover would handle the rest of the electronic functionality.

<br>
<img src="img/forwards.png"/>
<br><br>

This rover was made in four weeks and presented at the unit's final MakerLab expo, where it was showcased for everyone to see. The following links show the expo video and process video that was created alongside the robot.

[Showcase Video](https://drive.google.com/file/d/1ixSwt9YsMuz16ylT5Pp-rkC9DpjovgPJ/view?usp=sharing)

[Process Video](https://drive.google.com/file/d/1EIZdqRdU-tphqFfNITE4hw-vhuAkQmuy/view?usp=sharing)
<hr/>
<br>


<h2>Starting Up</h2>
Starting up the rover is simple. On the laptop, run the following two scripts:
<br><br>

```
. /src/cameras/gst_sink.sh
python3 /src/network/main.py opencv
```

Alternatively, to use a hard-coded terminal based control system instead of the neural network, run the following lines:
```
python3 /src/network/command.py
```

<br>
Similarly, to start up the scripts on the rover, the following two lines must be added:
<br><br>

```
. /src/cameras/gst_source.sh
python3 /src/controller/main.py
```
However, in the Raspberri-Pi's case, these two scripts are automatically started when the rover is turned on. One thing to ensure is correct is the IP addresses. These will need to be adjusted in the controller file, the network file and the command file if needed.
<br>