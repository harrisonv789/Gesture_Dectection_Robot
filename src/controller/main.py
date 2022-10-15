#!/usr/bin/env python3

import socket, threading, time
from datetime import datetime
from led import LED, LED_NONE, LED_GREEN, LED_RED, LED_YELLOW
from drive import Driver
from distance import DistanceSensor

class Controller:
    '''
    This class handles the communications from the Raspberry PI
    to the neural network device and is able to send procedures
    that are interpreted to a GPIO output device.
    '''
    
    # The current result
    result: str = None
    
    # The previous receive time
    prev_time: datetime = None
    
    # The timeout for the server
    timeout: int = 1
    
    # The minimum distance before stopping
    MINIMUM_DISTANCE: float = 20.0
    
    def __init__ (self, ip: str = "192.168.1.112"):
        '''
        Initialises the main controller loop that is able
        to listen for a websocket from the neural network
        and receive the current prediction letter.
        '''
        
        # Set up the websockets
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # Loop until address becomes available
        while True: 
            try:
                self.server.bind((ip, 9000))
                self.server.listen()
                break
            except: time.sleep(0.1)

        # Create the LED class and set the LED to red while waiting
        self.led = LED()
        self.led.set_color(LED_RED)
        
        # Create the distance sensor class
        self.distance = DistanceSensor()
        
        # Create the driver class for controlling the wheels
        self.driver = Driver()
        
        # Start the listening thread
        self.thread = threading.Thread(target=self.listen)
        self.thread.start()
        
        log_msg("Server has been initialised and waiting for data...")
        
    def listen (self):
        '''
        Listens to the server sockets and waits to receive
        some data in the form of the current prediction. If
        None, then there is no prediction.
        '''
        while True:
        
            # Change the color to red while wait
            self.led.set_color(LED_RED)
        
            # Get the current server data if it exists
            (client, address) = self.server.accept()
            log_msg("Connection has been made with %s:%s!" % (address[0], address[1]))
            
            # Set the timeout
            client.settimeout(self.timeout)
            self.prev_time = None
            
            # Reset the LED to off
            self.led.set_color(LED_YELLOW)
            
            # Loop until the timeout is exhausted
            while self.prev_time == None or (datetime.now() - self.prev_time).seconds < self.timeout:
            
                # Once data has been received, we can decode it
                try:
                
                    # Attempts to receive some data and updates the result
                    data = client.recv(1024)
                    if data != b'' and data != None:
                        self.update_result(data.decode())
                        self.prev_time = datetime.now()
                    
                # If an exception is thrown, print and move on
                except Exception as ex:
                    log_msg("Failed to read client data because '%s'." % ex)
                    self.update_result(None)
                
                # Give some time before looking for data again
                time.sleep(0.1)
                
    def update_result (self, result: str):
        '''
        This method handles the result being updated and
        can send out the appropriate action .
        '''
        
        # Checks if the distance is less than the minimum
        distance: float = self.distance.get_average()
        move_forward: bool = True
        if distance != None and distance < self.MINIMUM_DISTANCE:
            # Make the LED flash if in the minimum
            move_forward = False
        
        # Checks if the letter has been updated     
        if result != None and (result == "None" or len(result) == 0): result = None
        if self.result == result:
            if result == None or not move_forward:
                self.led.set_color(LED_YELLOW, not move_forward)
            return
        
        # At this point, the letter has changed
        self.result = result
        
        # Update the LED based on the color
        if result == None: self.led.set_color(LED_YELLOW, not move_forward)
        else: self.led.set_color(LED_GREEN, not move_forward)
        
        # Dispatch the action
        self.dispatch_action(result, move_forward)
    
    
    def dispatch_action (self, result: str, move_forward: bool):
        '''
        This gets the appropriate action from the action
        list based on the result and dispatches the action
        to be executed. The move forward flag ensures that only
        forward commands can be executed when it is able to.
        '''
        
        # Check for the missing command
        if result == None:
            self.driver.stop()
            return
        
        # Get the new result
        result = result.lower()
        
        # Driving forward
        if result in ("thumbs up", "rock", "call me", "fist") and move_forward:
            self.driver.drive(1.0, 0.0)
        
        # Driving reverse
        elif result == "thumbs down":
            self.driver.drive(-1.0, 0.0)
        
        # Attempt a spin
        elif result == "okay" and move_forward:
            self.driver.drive(1.0, 1.0)
            
        # Any other action should stop
        else:
            self.driver.stop()
    
    
    def shutdown (self):
        '''
        Shuts down the thread and ensures that everything
        safely closes correctly.
        '''
        log_msg("Shutting down.")
        self.led.set_color(LED_NONE)
        self.thread.join()
        self.distance.close()
   
        
def log_msg (msg: str):
    '''
    This method logs a particular message from a current
    time to the log file that can be found on the user's
    Desktop directory.
    '''
    # The file path to write updates to.
    file_path: str = "/home/pi/Desktop/controller_status.txt"

    with open(file_path, "a+") as file:
        file.write("[%s] %s\n" % (datetime.now().strftime("%H:%M:%S %d/%m/%Y"), msg))
    
    # Also print the lines
    print(msg)


# When this file gets executed
if __name__ == "__main__":

    # Attempt to run the controller
    try:
        controller = Controller()
    except KeyboardInterrupt:
        controller.shutdown()
    except Exception as ex:
        log_msg("Program failed because '%s'.\n" % str(ex))
        
