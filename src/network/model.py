# Import all required models
import pandas as pd
import keras
import numpy as np
from keras.models import Sequential

class Model:
    '''
    A wrapper class for the sign language neural network with the correct
    data and is able to load a model and train a new one with some exposed
    parameters.
    '''

    # The CNN model that is produced
    model: Sequential = None

    # The list of labels
    labels: list = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y"]

    def __init__(self) -> None:
        '''
        The default constructor that is able to initialise any values.
        '''
        pass

    def load (self, file: str) -> None:
        '''
        Loads the model from a particular file and then updates the current
        model variable.
        '''
        self.model = keras.models.load_model(file)

    def get_model (self) -> Sequential:
        '''
        Returns the model that is currently loaded. If no model is to be
        loaded, then the model needs to be trained.
        '''
        return self.model

    def train (self, output: str, epochs: int = 5) -> None:
        '''
        Attempts to retrain the model with a series of parameters using
        the training and testing data and creates the model.
        '''

        # Import the correct modules for this section
        from keras.layers import Dense, Conv2D, MaxPool2D, Flatten, Dropout, BatchNormalization
        from keras.callbacks import ReduceLROnPlateau
        from keras.preprocessing.image import ImageDataGenerator
        from sklearn.preprocessing import LabelBinarizer

        # Get the raw training set
        raw_training_data = pd.read_csv('../../training/sign_mnist_train.csv')
        raw_testing_data = pd.read_csv('../../training/sign_mnist_test.csv')

        # Get the binary data for the labels
        label_binarizer = LabelBinarizer()
        train_data_result = label_binarizer.fit_transform(raw_training_data['label'])
        test_data_result = label_binarizer.fit_transform(raw_testing_data['label'])

        # Remove the labels from the data
        del raw_training_data['label']
        del raw_testing_data['label']

        # Get the image data
        train_data_image = raw_training_data.values / 255
        test_data_image = raw_testing_data.values / 255

        # Reshape the image data
        train_data_image = train_data_image.reshape(-1,28,28,1)
        test_data_image = test_data_image.reshape(-1,28,28,1)

        # Create the model
        self.model = Sequential()

        # Set up the model parameters and layers
        self.model.add(Conv2D(75 , (3,3) , strides = 1 , padding = 'same' , activation = 'relu' , input_shape = (28,28,1)))
        self.model.add(BatchNormalization())
        self.model.add(MaxPool2D((2,2) , strides = 2 , padding = 'same'))
        self.model.add(Conv2D(50 , (3,3) , strides = 1 , padding = 'same' , activation = 'relu'))
        self.model.add(Dropout(0.2))
        self.model.add(BatchNormalization())
        self.model.add(MaxPool2D((2,2) , strides = 2 , padding = 'same'))
        self.model.add(Conv2D(25 , (3,3) , strides = 1 , padding = 'same' , activation = 'relu'))
        self.model.add(BatchNormalization())
        self.model.add(MaxPool2D((2,2) , strides = 2 , padding = 'same'))
        self.model.add(Flatten())
        self.model.add(Dense(units = 512 , activation = 'relu'))
        self.model.add(Dropout(0.3))
        self.model.add(Dense(units = 24 , activation = 'softmax'))
        self.model.compile(optimizer = 'adam' , loss = 'categorical_crossentropy' , metrics = ['accuracy'])
        self.model.summary()

        # With data augmentation to prevent overfitting
        datagen = ImageDataGenerator(
            featurewise_center=False,  # set input mean to 0 over the dataset
            samplewise_center=False,  # set each sample mean to 0
            featurewise_std_normalization=False,  # divide inputs by std of the dataset
            samplewise_std_normalization=False,  # divide each input by its std
            zca_whitening=False,  # apply ZCA whitening
            rotation_range=10,  # randomly rotate images in the range (degrees, 0 to 180)
            zoom_range = 0.1, # Randomly zoom image 
            width_shift_range=0.1,  # randomly shift images horizontally (fraction of total width)
            height_shift_range=0.1,  # randomly shift images vertically (fraction of total height)
            horizontal_flip=False,  # randomly flip images
            vertical_flip=False)  # randomly flip images

        # Fit the data
        datagen.fit(train_data_image)

        # Perform the learning
        learning_rate_reduction = ReduceLROnPlateau(monitor='val_accuracy', patience = 2, verbose=1, factor=0.5, min_lr=0.00001)
        print("Beginning Neural Network training with %d Epochs." % epochs)
        self.history = self.model.fit(datagen.flow(train_data_image, train_data_result, batch_size = 128), epochs = epochs, validation_data = (test_data_image, test_data_result), callbacks = [learning_rate_reduction])

        # Print the accuracy
        print("Training complete. Accuracy of the model is: %s" % self.model.evaluate(test_data_image, test_data_result)[1])

        # Save the model
        self.model.save(output)
        print("Model has been saved.")

    def predict (self, image_name: str) -> str:
        '''
        This method takes in an image and attempts to predict what letter
        the image is based on the current CNN model that has been loaded.
        The letter is returned as an output string.
        '''
        # Include the necessary libraries
        import matplotlib.image as mpimg

        # Read the image
        img = mpimg.imread(image_name)

        # Converts the image to a greyscale, and gets it in the form that we need it in
        grey = self.rgb_to_grey(img)
        grey = grey.reshape((grey.shape[0], 28, 1))
        array = np.array([grey])

        prediction = self.model.predict(array)
        return self.labels[np.argmax(prediction)]

    def rgb_to_grey (self, rgb):
        return np.dot(rgb[...,:3], [0.299, 0.587, 0.114])



if __name__ == "__main__":
    model = Model()
    #model.train("../../models/sign_model")
    model.load("../../models/sign_model")
    prediction = model.predict("../../examples/A.png")
    print(prediction)