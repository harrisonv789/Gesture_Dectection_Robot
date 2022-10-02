class PredictionData:
    '''
    The predicition data acts a struct for storing letters and
    the percentage fraction that resulted in that prediction
    '''
    # The letter of the prediction
    letter: str = None

    # The percentage chance that this letter is correct
    value: float = 0.0


    def __init__(self, letter: str, value: float) -> None:
        '''
        The default constructor for setting up the prediction
        with the associated percentage
        '''
        self.letter = letter if letter != "" else None
        self.value = value

    
    # The default to string method
    def __str__(self) -> str:
        return "Prediction: %s, Accuracy: %f%%" % (self.letter, self.value)