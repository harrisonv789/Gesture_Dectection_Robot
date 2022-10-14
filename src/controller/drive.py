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
    LEFT_MOTOR: int = 0
    RIGHT_MOTOR: int = 1
    
    # Define the speed multiplier
    MULTIPLIER: float = 0.6

    def __init__ (self) -> None:
        '''
        The constructor sets up the GPIO connection
        and allows for sending commands to the output
        pins.
        '''
        
        # Set up the PWM
        self.pwm = PCA9685(0x40, debug=False)
        self.pwm.setPWMFreq(50)

        print("Initialised PWM for motor controls.")
        self.stop()


    def __get_pwm_pin__ (self, motor: int) -> int:
        '''
        Returns the ID for the pinout of the PWM
        associated with this particular motor.
        '''
        return 0 if motor == self.LEFT_MOTOR else 5
    
    
    def __get_input_pins__ (self, motor: int) -> tuple[int]:
        '''
        Returns the pair of input pinouts depending on
        the motor that is returned to be commanded.
        '''
        if motor == self.LEFT_MOTOR:
            return (1, 2)
        else:
            return (3, 4)
    
        
    def drive (self, speed: float, steer: float = 0.0) -> None:
        '''
        Drives the motor forward in some direction,
        with a steering factor that has -1.0 to move
        left and 1.0 to move right.
        '''
        
        # Determine the new speed
        speed *= self.MULTIPLIER
        
        # Send both motors
        self.motor_send(self.LEFT_MOTOR, speed)
        self.motor_send(self.RIGHT_MOTOR, speed)
        
        
    def motor_send (self, motor: int, power: float = 1.0) -> None:
        '''
        Moves a motor with a particular amount of power
        based on the power value passed through.
        '''
        
        # Determines the duty cycle from 0 to 100
        duty: int = int(abs(power) * 100)
        
        # Get the appropriate pins
        pwm_pin: int = self.__get_pwm_pin__(motor)
        input_pins: tuple[int] = self.__get_input_pins__(motor)
        
        # Update the duty cycle of the PWM
        self.pwm.setDutycycle(pwm_pin, duty)
        
        # Positive spinning
        if power > 0.0:
            self.pwm.setLevel(input_pins[0], 0)
            self.pwm.setLevel(input_pins[1], 1)
        
        # Negative spinning
        elif power < 0.0:
            self.pwm.setLevel(input_pins[0], 1)
            self.pwm.setLevel(input_pins[1], 0)
        
        # Send zeroes
        else:
            self.pwm.setDutycycle(pwm_pin, 0)

        print("Driver :: Sending Motor %d at power %s" % (motor, power))
    
    
    def stop (self) -> None:
        '''
        Stops all motors and stops the robot from driving
        in any direction.
        '''
        self.motor_send(self.LEFT_MOTOR, 0)
        self.motor_send(self.RIGHT_MOTOR, 0)
        print("Driver :: Stop Action.")
    
        
if __name__ == "__main__":
    output = Driver()
    output.stop()
    output.drive(0.5)
    time.sleep(1.0)
    output.stop()
