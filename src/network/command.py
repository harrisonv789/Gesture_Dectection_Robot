#!/bin/python3

import time, socket, threading

# Defines the current action
current_action: str = None

# The current client
client: socket.socket = None

# Define the thread
thread: threading.Thread = None

# Whether to stop it all
stop: bool = False


def main (ip: str = "172.20.10.2"):
    '''
    This is the main function that is executed for sending through
    fake commands to the robot for testing purposes.
    '''

    global current_action, client

    # Set up the sockets (until one exists)
    while True:
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((ip, 9000))
            break
        except Exception as ex:
            print(ex)
            time.sleep(0.1)

    # Start the thread
    thread = threading.Thread(target=loop)
    thread.start()
    
    # Print the client connection status
    print("Client has been connected.")

    # Start the loop

    # Loop forever
    while not stop:

        # Get the current text
        print("\nPlease enter one of the following, or nothing for 'None'.")
        gesture: str = input("[F]orward, [B]ackwards, [S]pin, [N]one: ")

        # Determine the action
        if len(gesture) == 0: current_action = None
        elif gesture[0].lower() == "f": current_action = "thumbs up"
        elif gesture[0].lower() == "b": current_action = "thumbs down"
        elif gesture[0].lower() == "s": current_action = "okay"


def loop ():

    while not stop:

        # Send the result
        client.send(str(current_action).encode())

        # Wait some time
        time.sleep(0.1)


# When the main loop is called
if __name__ == "__main__":

    # Call the main loop
    try:
        main()
    
    except KeyboardInterrupt:
        stop = True
        if thread != None:
            thread.join()
