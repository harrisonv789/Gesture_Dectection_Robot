#!/usr/bin/env python3

import socket, threading, time
from datetime import datetime
from led import LED, LED_NONE, LED_GREEN, LED_RED, LED_YELLOW

class Controller:
    
    # The current letter
    letter: str = None
    
    def __init__ (self, ip: str = "192.168.1.112"):
        '''
        Initialises the main controller loop that is able
        to listen for a websocket from the neural network
        and receive the current prediction letter.
        '''
        
        # Set up the websockets
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((ip, 9000))
        self.server.listen()

        # Create the LED class
        self.led = LED()
        # Set the LED to red while waiting
        self.led.set_color(LED_RED)
        
        # Start the listening thread
        self.thread = threading.Thread(target=self.listen)
        self.thread.start()
        
        print("Server has been initialised and waiting for data...")
        
    def listen (self):
        '''
        Listens to the server sockets and waits to receive
        some data in the form of the current prediction. If
        None, then there is no prediction.
        '''
        while True:
        
            # Get the current server data if it exists
            (client, address) = self.server.accept()
            print("Connection has been made with %s:%s!" % (address[0], address[1]))
            
            # Reset the LED to off
            self.led.set_color(LED_NONE)
            
            while True:
                # Once data has been received, we can decode it
                try:
                    data: str = client.recv(1024).decode()
                    if data != "":
                        self.update_letter(data)
                except Exception as ex:
                    print(ex)
                time.sleep(0.1)
                
    def update_letter (self, letter: str):
        '''
        This method handles the letter being updated and
        can send out the appropriate action .
        '''
        
        # Checks if the letter has been updated     
        if letter == "None" or len(letter) > 1: letter = None
        if self.letter == letter: return
        
        # At this point, the letter has changed
        self.letter = letter
        print(self.letter)
        
        # Update the LED based on the color
        if letter == None: self.led.set_color(LED_YELLOW)
        else: self.led.set_color(LED_GREEN)
    
    
    def shutdown (self):
        '''
        Shutsdown the thread and ensures that everything
        safely closes correctly.
        '''
        print("Shutting down.")
        self.led.set_color(LED_NONE)
        self.thread.join()
        

# When this file gets executed
if __name__ == "__main__":

    # The file path to write updates to.
    file_path: str = "/home/pi/Desktop/controller_status.txt"

    with open(file_path, "a+") as file:
        file.write("%s - Executing control script.\n" % datetime.now().strftime("%H:%M:%S %d/%m/%Y"))
        
    # Attempt to run the controller
    try:
        controller = Controller()
    except KeyboardInterrupt:
        controller.shutdown()
    except Exception as ex:
        with open(file_path, "a") as file:
            file.write("Program failed because '%s'.\n" % str(ex))
        
