from PIL import Image as PILImage
import os
import numpy as np

class Image:
    '''
    This class acts as a wrapper for an image and is able to
    output particular image data for images.
    '''

    def __init__(self, file: str) -> None:
        '''
        The constructor requires a particular file to work. This file
        must be valid, otherwise an exception will be thrown.
        '''
        if not os.path.exists(file):
            raise Exception("Image file '%s' does not exist." % file)
        
        self.image = PILImage.open(file)
    
    def resize (self, width: int = 28, height: int = 28) -> None:
        '''
        Resizes the image to a new size and updates the current image
        to this sized image.
        '''
        self.image = self.image.resize((width, height))
    
    def save (self, file: str) -> None:
        '''
        Saves the image to a particular file location and overwrites the
        current image if one already exists.
        '''
        self.image.save(file)

    def get_raw (self):
        '''
        Returns the raw data from the image that can be read by
        OpenCV.
        '''
        return np.array(self.image.getdata())
    
    def get_opencv_data (self) -> np.ndarray:
        '''
        Returns the data in the format of an OPEN CV array.
        This will reformat the data into the correct process.
        '''

        # Get the raw data
        raw = self.get_raw()
        formatted: list = []

        # Loops through each row an
        for j in range (self.image.size[1]):
            row: list = []
            for i in range(self.image.size[0]):
                data = raw[j * self.image.size[0] + i]
                row.append([data[2], data[1], data[0]])
            formatted.append(row)
        return np.array(formatted).astype(np.uint8)

    
    def get_data (self, width: int = 28, height: int = 28) -> np.ndarray:
        '''
        Returns the raw pixel data of the image ready for the prediction
        of the image.
        '''
        # Resize if required
        if self.image.size != (width, height):
            self.resize()
        
        # Get the data
        raw_data = self.image.getdata()
        data = np.array([[raw_data[i * height + _] for _ in range(width)] for i in range(height)])
        
        # Turn it greyscale and reshape the data
        grey: np.ndarray = self.rgb_to_grey(data) / 255.0
        reshaped = grey.reshape((1, width, height, 1))
        return reshaped
    
    def rgb_to_grey (self, rgb: np.ndarray) -> np.ndarray:
        '''
        Converts an RGB array to greyscale array between 0 and 255 as 
        an array.
        '''
        return np.dot(rgb[...,:3], [0.299, 0.587, 0.114])

if __name__ == "__main__":
    image = Image("../../examples/L.png")
    image.resize()
    data = image.get_data()