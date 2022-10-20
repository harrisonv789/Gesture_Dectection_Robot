#!/bin/python3

import time, os, socket, sys
from image import Image
from model import Model
from gesture import Gesture
from prediction import PredictionData

def main (ip: str = "172.20.10.4", use_cv: bool = False):
    '''
    This is the main function that is executed to check for 
    image and then process the results
    '''
    
    # Print out the current state of the result
    if use_cv:
        print("Using an OpenCV neural network for the sign language.")
        data_length: int = 5
        accuracy: float = 0.5
    else:
        print("Using a trained neural network for letters.")
        data_length: int = 10
        accuracy: float = 0.85

    # Set up the sockets (until one exists)
    while True:
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((ip, 9000))
            break
        except Exception as ex:
            print(ex)
            time.sleep(0.1)
    
    # Print the client connection status
    print("Client has been connected.")

    # Load the CV model
    if use_cv:
        model = Gesture()
    
    # Loads the standard neural network model
    else:
        model = Model()
        model.load("../../models/sign_model")

    # Most recent results
    recents: list = [None] * data_length

    # Loop forever
    while True:
        
        # Load the image (until it works)
        while True:
            try:
                image = Image("../../data/camera.jpg")
                break

            # If there is an issue loading image, send a none
            except:
                time.sleep(0.001)
                client.send("None".encode())

        # Make the prediction
        prediction = model.predict(image)
        os.system("clear")
        print("New Prediction. %s\n" % prediction)
        
        # Add the prediction to the list by shuffling
        recents = [recents[i - 1] for i in range(1, len(recents))]
        recents.insert(0, prediction)

        # Determine the result
        result: str = determine_result(recents, accuracy)

        # Check if the result is valid
        if result != None:
            print("Current Prediction: %s" % result)
        else:
            print("No Prediction Made.")
        
        # Send through the result (even if it is None)
        try:
            client.send(str(result).encode())
        except:
            pass

        # Wait some time
        time.sleep(0.02)


def determine_result (recents: "list[PredictionData]", accuracy: float) -> str:
    '''
    Attempts to determine the result most likely to be
    based on a list of predictions
    '''

    # Get the number of results of the same type
    check: str = recents[0].result
    count: int = 1
    for prediction in recents[1:]:
        if prediction != None and prediction.result == check:
            count += 1
    
    # If the number of results is not consistent, then return None
    if float(count) / float(len(recents)) < accuracy:
        return None

    # Next, sum the prediction accuracies and check to see if the sum of the
    #   correct result results in 95% accuracy
    accuracies: float = 0
    for prediction in recents:
        if prediction != None and prediction.result == check:
            accuracies += prediction.value
    
    if (accuracies / 100.0) / float(count) < accuracy:
        return None
    
    # Otherwise, return the result
    return check


# When the main loop is called
if __name__ == "__main__":

    # Specify the type of network used
    use_cv: bool = True if len(sys.argv) > 1 and sys.argv[1] == "opencv" else False

    # Call the main loop
    main(use_cv=use_cv)
