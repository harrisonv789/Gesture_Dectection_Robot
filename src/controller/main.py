#!/bin/python3

import socket, threading, time

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
        if letter == "None": letter = None
        if self.letter == letter: return
        
        # At this point, the letter has changed
        self.letter = letter
        print(self.letter)
        

if __name__ == "__main__":
    controller = Controller()
