import time
import RPi.GPIO as GPIO
import threading

class DistanceSensor:
    '''
    The distance sensor can be attached to the
    Raspberry Pi and is able to return the distance
    in cm to the nearest object or wall.
    '''
    
    # Define the constants
    GPIO_TRIGGER: int = 18
    GPIO_ECHO: int = 24
    
    # The sonic speed in cm/s
    SONIC_SPEED: float = 34300.0
    
    # Anything above this distance will be culled
    MAX_DISTANCE: float = 100.0
    
    # The distance readings
    recent_readings: list = [None] * 3
    
    
    def __init__ (self) -> None:
        '''
        The init method initialises the connections
        and establishes any variables that are required
        for the sensor to run.
        '''
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.GPIO_TRIGGER, GPIO.OUT)
        GPIO.setup(self.GPIO_ECHO, GPIO.IN)
        GPIO.output(self.GPIO_TRIGGER, False)
        
        # The loop for the thread
        self.loop = True
        
        # Start the update thread
        self.thread = threading.Thread(target=self.__update__)
        self.thread.start()
        
        print("Initialised Distance Sensor.")
        
    
    def __update__ (self) -> None:
        '''
        This method simply updates the sensor data and
        stores the distance in the list. It is used for
        a thread that is executed.
        '''
        
        # Loop forever until the thread is closed
        while self.loop:
        
            # Get a new distance reading and add to the list
            distance: float = self.__get_distance__()
            self.recent_readings.append(distance)
            
            # Remove the oldest
            del self.recent_readings[0]
            
            # Sleep some time
            time.sleep(0.1)
        
    
    def __get_distance__ (self) -> float:
        '''
        Calls the GPIO with the correct values and
        is able to decode the output to return the
        distance in cm.
        '''
        GPIO.output(self.GPIO_TRIGGER, True)
        
        # Set the trigger to false after a small amount of time
        time.sleep(0.00001)
        GPIO.output(self.GPIO_TRIGGER, False)
        
        # Store the start and stop times
        start_time = time.time()
        stop_time = time.time()

        # Save the new start time
        while GPIO.input(self.GPIO_ECHO) == 0:
            start_time = time.time()
        
        # Determine the stop time
        while GPIO.input(self.GPIO_ECHO) == 1:
            stop_time = time.time()
        
        # Calculate the time elapsed
        elapsed = stop_time - start_time
        
        # Return the distance which is the time over the sonic speed
        distance = elapsed * self.SONIC_SPEED / 2.0
        
        # Cull the distance
        if distance > self.MAX_DISTANCE:
            distance = None
        return distance
    
    
    def get_average (self) -> float:
        '''
        Calculates the average distance that the sensor is
        away from the object and is able to ignore any values
        that are missing or incorrect.
        '''
        
        # Cleaning up data that is invalid
        data = self.recent_readings
        if data[0] == None and data[2] == None:
            data[1] = None
        elif data[1] == None and data[0] != None and data[2] != None:
            data[0] = None
            data[2] = None
        
        # Calculate the sums and totals
        total: float = sum([x for x in data if x != None])
        count: int = sum([1 for x in data if x != None])
        
        # Returns the average
        return total / float(count) if count > 1 else None
    
    
    def close (self) -> None:
        '''
        Handles the closing of the distance sensor and ensures
        that all of the threads are complete and the GPIO pins
        are closed off.
        '''
        self.loop = False
        self.thread.join()
        GPIO.cleanup()
        print("Cleaned up Distance Sensor.")
        

# If executing from command line
if __name__ == "__main__":
    sensor = DistanceSensor()
    try:
        while True:
            time.sleep(0.05)
            distance: float = sensor.get_average()
            print("The current distance to the wall is: %s cm" % distance)
            
    except KeyboardInterrupt:
        pass
    finally:
        sensor.close()
    
