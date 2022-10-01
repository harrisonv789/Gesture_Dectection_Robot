#/bin/sh

gst-launch-1.0 v4l2src device=/dev/video1 ! videorate ! video/x-raw, width=320, framerate=10/1 ! videoconvert ! jpegenc ! rtpjpegpay ! udpsink host="127.0.0.1" port=5001
