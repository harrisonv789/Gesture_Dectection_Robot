#!/bin/env/python3

import time, os, socket
from image import Image
from model import Model
from prediction import PredictionData


def main (ip: str = "192.168.1.112"):
    '''
    This is the main function that is executed to check for 
    image and then process the results
    '''

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

    # Load the model
    model = Model()
    model.load("../../models/sign_model")

    # Most recent letters
    recents: list = [None] * 10

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
        print("New Prediction. %s\n" % prediction)
        
        # Add the prediction to the list by shuffling
        recents = [recents[i - 1] for i in range(1, len(recents))]
        recents.insert(0, prediction)

        # Determine the letter
        letter: str = determine_letter(recents)

        # Check if the letter is valid
        if letter != None:
            print("Current Prediction: %s" % letter)
        else:
            print("No Prediction Made.")
        
        # Send through the letter (even if it is None)
        try:
            client.send(str(letter).encode())
        except:
            pass

        # Wait some time
        time.sleep(0.1)


def determine_letter (recents: "list[PredictionData]") -> str:
    '''
    Attempts to determine the letter most likely to be
    based on a list of predictions
    '''

    # Get the number of letters of the same type
    check: str = recents[0].letter
    count: int = 1
    for prediction in recents[1:]:
        if prediction != None and prediction.letter == check:
            count += 1
    
    # If the number of letters is not consistent, then return None
    if float(count) / float(len(recents)) < 0.95:
        return None

    # Next, sum the prediction accuracies and check to see if the sum of the
    #   correct letter results in 95% accuracy
    accuracies: float = 0
    for prediction in recents:
        if prediction != None and prediction.letter == check:
            accuracies += prediction.value
    
    if (accuracies / 100.0) / float(count) < 0.85:
        return None
    
    # Otherwise, return the letter
    return check






# When the main loop is called
if __name__ == "__main__":
    main()