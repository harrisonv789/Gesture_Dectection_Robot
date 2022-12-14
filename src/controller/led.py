import RPi.GPIO as GPIO
import time

# Defines the light types
LED_NONE: int = 0
LED_RED: int = 1
LED_YELLOW: int = 2
LED_GREEN: int = 3

class LED:
    '''
    This class is able to display different
    LED values based on an input. It has a 
    preset series of serial devices that it
    can connect to and power.
    '''
    
    # Defines the flashing variables
    is_flashing: bool = False
    flash_state: bool = False
    
    def __init__ (self) -> None:
        '''
        Initialises the pins for the lights
        to output power.
        '''
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.get_pin(LED_RED), GPIO.OUT)
        GPIO.setup(self.get_pin(LED_YELLOW), GPIO.OUT)
        GPIO.setup(self.get_pin(LED_GREEN), GPIO.OUT)
        
    def get_pin (self, light: int) -> int:
        '''
        Returns the PIN output pin for a respective
        color of some type.
        '''
        if light == LED_RED: return 17 # GPIO17
        if light == LED_YELLOW: return 27 # GPIO27
        if light == LED_GREEN: return 22 # GPIO22
        
    def set_led (self, light: int, state: bool):
        '''
        Sets a particular light with a particular
        state - either on or off. 
        '''
        if state: GPIO.output(self.get_pin(light), GPIO.HIGH)
        else: GPIO.output(self.get_pin(light), GPIO.LOW)

    def set_color (self, color: int, flash: bool = False):
        '''
        Sets a particular color and disables the rest.
        This ensures only one color is showing. If the flash is set, 
        it will flicker the state on and off periodically.
        '''
        self.is_flashing = flash
        self.set_led(LED_RED, False)
        self.set_led(LED_YELLOW, False)
        self.set_led(LED_GREEN, False)
        
        # Flip the flash state regardless
        self.flash_state = not self.flash_state
        
        # Check if the colour is valid and is flashing
        if color != LED_NONE:
            if not self.is_flashing or self.flash_state:
                self.set_led(color, True)       
        
if __name__ == "__main__":
    led = LED()
    led.set_color(LED_NONE)
    
    for _ in range(10):
        led.set_color(LED_RED, True)
        time.sleep(0.1)
    
    #led.set_color(LED_RED)
    #time.sleep(1.0)
      
    #led.set_color(LED_YELLOW)
    #time.sleep(1.0)
    
    #led.set_color(LED_GREEN)
    #time.sleep(1.0)
    
    led.set_color(LED_NONE)
    
