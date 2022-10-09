#/bin/sh

# If the case that the user does want to display
if [ "$1" == "show" ]; then
    gst-launch-1.0 udpsrc port=5001 ! application/x-rtp, encoding-name=JPEG, payload=26 ! rtpjpegdepay ! tee name=save ! queue ! jpegdec ! autovideosink save. ! multifilesink location="../../data/camera.jpg";
else
    gst-launch-1.0 udpsrc port=5001 ! application/x-rtp, encoding-name=JPEG, payload=26 ! rtpjpegdepay ! multifilesink location="../../data/camera.jpg";
fi