import RPi.GPIO as gpio
import time


class Driver:
    '''
    This class handles the GPIO pin output
    for sending commands to the motor drivers
    and being able to steer the robot.
    '''
    
    # Define the outputs for the motors
    LEFT_MOTOR_GPIO: int = 16 # Pin 16, GPIO23
    RIGHT_MOTOR_GPIO: int = 11 # Pin 11, GPIO17

    def __init__ (self):
        '''
        The consrtructor sets up the GPIO connection
        and allows for sending commands to the output
        pins.
        '''
        
        # Initialise all the pins
        #gpio.setmode(gpio.BOARD)
        #gpio.setwarnings(False)
        #gpio.setup(self.LEFT_MOTOR_GPIO, gpio.OUT)
        #gpio.setup(self.RIGHT_MOTOR_GPIO, gpio.OUT)
        print("Initialised GPIO pins for motor controls.")
        
        
    def drive (self, speed: float, steer: float = 0.0):
        '''
        Drives the motor forward in some direction,
        with a steering factor that has -1.0 to move
        left and 1.0 to move right.
        '''
        self.motor_send(self.LEFT_MOTOR_GPIO, speed if steer <= 0.0 else speed - steer)
        self.motor_send(self.RIGHT_MOTOR_GPIO, speed if steer >= 0.0 else speed + steer)
        
        
    def motor_send (self, motor: int, power: float = 1.0):
        '''
        Moves a motor with a particular amount of power
        based on the power value passed through.
        '''
        #gpio.output(motor, gpio.LOW)
        #if power == 1.0: gpio.output(motor, gpio.HIGH)
        #else: gpio.output(motor, gpio.LOW)
        print("Driver :: Sending Motor %d at power %s" % (motor, power))
    
    
    def stop (self):
        '''
        Stops all motors and stops the robot from driving
        in any direction.
        '''
        print("Driver :: Stop Action.")
    
        
if __name__ == "__main__":
    output = Driver()
    while True:
        output.drive(0.0)
        time.sleep(0.01)
    gpio.cleanup()
