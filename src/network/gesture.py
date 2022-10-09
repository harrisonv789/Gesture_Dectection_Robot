# Import all required models
import cv2, time
import numpy as np
import mediapipe as mp
import tensorflow as tf
from tensorflow.keras.models import load_model
from image import Image
from prediction import PredictionData

class Gesture:
    '''
    This class is able to take in an image of a specific format
    and using the open-CV python wrapper library, produce a gesture
    from the image. This is an alternative to the trained neural
    network model that determines letters from different images.

    This AI system can produce the following outputs:
    ['okay', 'peace', 'thumbs up', 'thumbs down', 'call me', 'stop', 'rock', 'live long', 'fist', 'smile']
    '''

    def __init__(self, show: bool = True) -> None:
        '''
        The default constructor sets up the class
        and prepares for the recognition.
        '''

        # Initialize mediapipe for the hand recognition
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
        self.draw = mp.solutions.drawing_utils

        # Save the parameters
        self.show = show

        # Loads the model
        self.load_model()
    
    def load_model (self) -> None:
        '''
        Loads the model using tensorflow and read the model.
        '''
        # Load the gesture recognizer model
        self.model = load_model("../opencv-model/mp_hand_gesture")

        # Load class names
        with open("../opencv-model/gesture.names", 'r') as file:
            self.class_names = file.read().split('\n')

    def predict (self, image: Image) -> PredictionData:
        '''
        Makes a prediction from a particular image that has
        been captured by the camera stream. It returns the 
        prediction as a string of the image.
        '''
        data = image.get_opencv_data()

        # Store the dimensions
        x , y, c = data.shape

        framergb = cv2.cvtColor(data, cv2.COLOR_BGR2RGB)

        # Get hand landmark prediction
        result = self.hands.process(framergb)

        # The resulted class name
        predict_data: PredictionData = PredictionData("None", 0.0)

        # post process the result
        if result.multi_hand_landmarks:
            landmarks = []
            for handslms in result.multi_hand_landmarks:
                for lm in handslms.landmark:
                    lmx = int(lm.x * x)
                    lmy = int(lm.y * y)
                    landmarks.append([lmx, lmy])

            # Drawing landmarks on frames
            self.draw.draw_landmarks(data, handslms, self.mp_hands.HAND_CONNECTIONS)

            # Create the prediction
            prediction = self.model.predict([landmarks])
            class_id = np.argmax(prediction)
            class_name = self.class_names[class_id]
            predict_data = PredictionData(class_name, np.max(prediction) * 100.0)

        # Show the image
        if self.show:
            cv2.imshow("Output", data)
            cv2.waitKey(1)
        
        # Return the class
        return predict_data


# Called when the script is executed
if __name__ == "__main__":
    g = Gesture()

    while True:
        image = Image("../../data/camera.jpg")
        prediction = g.predict(image)
        print(prediction)
    
    # Removes the windows
    cv2.destroyAllWindows()
