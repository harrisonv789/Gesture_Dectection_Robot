#!/bin/env/python3

import time, os, sys
from image import Image
from model import Model

# This is the main function that is executed to check for image and then process the results
def main ():

    # Load the model
    model = Model()
    model.load("../../models/sign_model")

    # Loop forever
    while True:
        
        # Load the image (until it works)
        while True:
            try:
                image = Image("../../data/camera.jpg")
                break
            except:
                time.sleep(0.001)

        # Make the prediction
        prediction = model.predict(image)
        os.system("clear")
        print(prediction)

        # Wait some time
        time.sleep(0.1)
    


# When the main loop is called
if __name__ == "__main__":
    main()