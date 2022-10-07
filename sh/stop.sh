#/bin/sh

echo "Stopping all processes if they exist."

# This script stops all systems from running
id=$(pidof python3 ./main.py)

if [ ! -z "$id" ]; then
    sudo kill -9 $id;
fi;
id=$(pidof gst-launch-1.0)
if [ ! -z "$id" ]; then
    sudo kill -9 $id;
fi;
