import RPi.GPIO as gpio
import time
from PCA9685 import PCA9685


class Driver:
    '''
    This class handles the GPIO pin output
    for sending commands to the motor drivers
    and being able to steer the robot.
    '''
    
    # Define the outputs for the motors
    LEFT_MOTOR_GPIO: int = 16 # Pin 16, GPIO23
    RIGHT_MOTOR_GPIO: int = 11 # Pin 11, GPIO17
    
    # Store the pinouts for the PCA device
    PWMA = 0
    AIN1 = 1
    PWMB = 5
    AIN2 = 2
    BIN1 = 3
    BIN2 = 4

    def __init__ (self):
        '''
        The consrtructor sets up the GPIO connection
        and allows for sending commands to the output
        pins.
        '''
        
        # Set up the PWM
        self.pwm = PCA9685(0x40, debug=False)
        self.pwm.setPWMFreq(50)
        
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
        self.motor_send(self.LEFT_MOTOR_GPIO, 0.5)#speed if steer <= 0.0 else speed - steer)
        #self.motor_send(self.RIGHT_MOTOR_GPIO, speed if steer >= 0.0 else speed + steer)
        
        
    def motor_send (self, motor: int, power: float = 1.0):
        '''
        Moves a motor with a particular amount of power
        based on the power value passed through.
        '''
        duty: int = int(abs(power) * 100)
        self.pwm.setDutycycle(self.PWMA, duty)
        print(abs(power) * 100.0)
        if power > 0.0:
            self.pwm.setLevel(self.AIN1, 0)
            self.pwm.setLevel(self.AIN2, 1)
        elif power < 0.0:
            self.pwm.setLevel(self.AIN1, 1)
            self.pwm.setLevel(self.AIN2, 0)
        else:
            self.pwm.setDutycycle(self.PWMA, 0)

        print("Driver :: Sending Motor %d at power %s" % (motor, power))
    
    
    def stop (self):
        '''
        Stops all motors and stops the robot from driving
        in any direction.
        '''
        self.motor_send(self.LEFT_MOTOR_GPIO, 0)
        self.motor_send(self.RIGHT_MOTOR_GPIO, 0)
        print("Driver :: Stop Action.")
    
        
if __name__ == "__main__":
    output = Driver()
    output.stop()
