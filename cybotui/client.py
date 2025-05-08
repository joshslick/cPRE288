# Author: Phillip Jones
# Date: 10/30/2023
# Description: Client starter code that combines: 1) Simple GUI, 2) creation of a thread for
#              running the Client socket in parallel with the GUI, and 3) Simple recieven of mock sensor 
#              data for a server/cybot.for collecting data from the cybot.

# General Python tutorials (W3schools):  https://www.w3schools.com/python/

# Serial library:  https://pyserial.readthedocs.io/en/latest/shortintro.html 
import serial # Serial library for UART communication 
import time # Time library   
# Socket library:  https://realpython.com/python-sockets/  
# See: Background, Socket API Overview, and TCP Sockets  
import socket
import tkinter as tk # Tkinter GUI library
from tkinter import simpledialog # Tkinter simple dialog library for user input
# Thread library: https://www.geeksforgeeks.org/how-to-use-thread-in-tkinter-python/
import threading
import os  # import function for finding absolute path to this python script
import matplotlib as plt 
from matplotlib.animation import FuncAnimation # Matplotlib library for plotting data  

##### START Define Functions  #########

# Main: Mostly used for setting up, and starting the GUI
def main():

        global window  # Made global so quit function (send_quit) can access
        global degree_entry  # Entry widget for degree input
        global degree  # Variable to store the degree value

        

        window = tk.Tk() # Create a Tk GUI Window
        degree = tk.StringVar()  # Create a StringVar to hold the degree input

        # Last command label  
        global Last_command_Label  # Made global so that Client function (socket_thread) can modify
        Last_command_Label = tk.Label(text="Last Command Sent: ") # Creat a Label
        Last_command_Label.pack() # Pack the label into the window for display

        # Degree input label
        degree_label = tk.Label(text="Enter Degree:")  # Label for the degree input
        degree_label.pack()  # Pack the label into the window for display

        # Degree input box
        degree_entry = tk.Entry(window, textvariable=degree)  # Entry widget for degree input
        degree_entry.pack()  # Pack the entry widget into the window for display

        # Quit command Button
        quit_command_Button = tk.Button(text ="Press to Quit", command = send_quit)
        quit_command_Button.pack()  # Pack the button into the window for display

        # Cybot Scan command Button
        scan_command_Button = tk.Button(text ="Press to Scan", command = send_scan)
        scan_command_Button.pack() # Pack the button into the window for display

        # Cybot Move command Button
        move_command_Button = tk.Button(text="Press to Move", command=send_move)
        move_command_Button.pack()  # Pack the button into the window for display

       # Turn Left command Button
        turn_left_command_Button = tk.Button(text="Turn Left", command=send_turn_left)
        turn_left_command_Button.pack()  # Pack the button into the window for display

        # Turn Right command Button
        turn_right_command_Button = tk.Button(text="Turn Right", command=send_turn_right)
        turn_right_command_Button.pack()  # Pack the button into the window for display

        # Connect Button
        connect_button = tk.Button(text="Connect to Server", command=connect_to_cybot_uart)
        connect_button.pack()  # Pack the button into the window for display

        # Start the graph in a separate thread
        graph_thread = threading.Thread(target=start_graph)
        graph_thread.daemon = True  # Ensure the thread exits when the main program exits
        graph_thread.start()


        # Create a Thread that will run a fuction assocated with a user defined "target" function.
        # In this case, the target function is the Client socket code
        my_thread = threading.Thread(target=socket_thread) # Creat the thread
        my_thread.start() # Start the thread

        # Start event loop so the GUI can detect events such as button clicks, key presses, etc.
        window.mainloop()


# Quit Button action.  Tells the client to send a Quit request to the Cybot, and exit the GUI
def send_quit():
        global gui_send_message # Command that the GUI has requested be sent to the Cybot
        global window  # Main GUI window
        
        gui_send_message = "quit\n"   # Update the message for the Client to send
        time.sleep(1)
        window.destroy() # Exit GUI

def use_degree():
    global degree
    print(f"Degree entered: {degree.get()}")  # Access the degree value using degree.get()

def send_turn_left():
    global gui_send_message  # Command that the GUI has requested sent to the Cybot
    global degree  # Degree input from the user

    # Get the degree value from the input box
    degree_value = degree.get()
    if degree_value.isdigit():  # Ensure the input is a valid number
        gui_send_message = f"TurnLeft {degree_value}\n"  # Update the message for the Client to send
        print(f"TurnLeft command sent with degree: {degree_value}")
    else:
        print("Invalid degree value. Please enter a valid number.")

# Turn Right Button action. Sends a TurnRight command with the degree value to the server
def send_turn_right():
    global gui_send_message  # Command that the GUI has requested sent to the Cybot
    global degree  # Degree input from the user

def connect_to_cybot_uart():
    global cybot  # UART connection object

    # Create a new Toplevel window for input
    connect_window = tk.Toplevel()
    connect_window.title("Connect to CyBot via UART")

    # Label and Entry for COM Port
    tk.Label(connect_window, text="Enter COM Port (e.g., COM3):").pack(pady=5)
    com_port_entry = tk.Entry(connect_window)
    com_port_entry.pack(pady=5)

    # Label and Entry for Baud Rate
    tk.Label(connect_window, text="Enter Baud Rate (e.g., 115200):").pack(pady=5)
    baud_rate_entry = tk.Entry(connect_window)
    baud_rate_entry.pack(pady=5)

    # Function to handle the input and establish the UART connection
    def submit_connection():
        com_port = com_port_entry.get()
        baud_rate = baud_rate_entry.get()

        if not com_port:
            print("Invalid COM port. Please enter a valid COM port.")
            return

        if not baud_rate.isdigit():
            print("Invalid Baud Rate. Please enter a valid number.")
            return

        try:
            # Establish UART connection
            global cybot
            cybot = serial.Serial(com_port, int(baud_rate), timeout=1)
            print(f"Successfully connected to CyBot via UART on {com_port} with baud rate {baud_rate}")
            connect_window.destroy()  # Close the input window
        except Exception as e:
            print(f"Failed to connect to CyBot via UART: {e}")

    # Submit Button
    submit_button = tk.Button(connect_window, text="Connect", command=submit_connection)
    submit_button.pack(pady=10)

# Global variables for CyBot's position
cybot_x = [0]  # List to store x-coordinates
cybot_y = [0]  # List to store y-coordinates

# Function to update the CyBot's position on the graph
def update_graph(frame):
    global cybot_x, cybot_y

    # Read the CyBot's position from the UART (mocked here for demonstration)
    try:
        rx_message = cybot.readline().decode().strip()  # Read a line from the CyBot
        if rx_message.startswith("POS"):  # Example format: "POS x y"
            _, x, y = rx_message.split()
            cybot_x.append(float(x))  # Append the new x-coordinate
            cybot_y.append(float(y))  # Append the new y-coordinate
    except Exception as e:
        print(f"Error reading position: {e}")

    # Update the graph
    ax.clear()
    ax.plot(cybot_x, cybot_y, marker='o', linestyle='-', color='b')
    ax.set_title("CyBot Position")
    ax.set_xlabel("X Coordinate")
    ax.set_ylabel("Y Coordinate")
    ax.grid(True)
    ax.set_xlim(-10, 10)  # Set x-axis limits (adjust as needed)
    ax.set_ylim(-10, 10)  # Set y-axis limits (adjust as needed)

# Function to start the graph in a separate thread
def start_graph():
    global fig, ax

    # Create the figure and axis for the graph
    fig, ax = plt.subplots()

    # Use FuncAnimation to continuously update the graph
    ani = FuncAnimation(fig, update_graph, interval=500)  # Update every 500ms

    # Show the graph
    plt.show()




# Scan Button action.  Tells the client to send a scan request to the Cybot
def send_scan():
        global gui_send_message # Command that the GUI has requested sent to the Cybot
        
        gui_send_message = "M\n"   # Update the message for the Client to send



# Client socket code (Run by a thread created in main)
def socket_thread():
        # Define Globals
        #global HOST, PORT  # Use the updated HOST and PORT variables
        global Last_command_Label # GUI label for displaying the last command sent to the Cybot
        global gui_send_message   # Command that the GUI has requested be sent to the Cybot

        # A little python magic to make it more convient for you to adjust where you want the data file to live
        # Link for more info: https://towardsthecloud.com/get-relative-path-python 
        absolute_path = os.path.dirname(__file__) # Absoult path to this python script
        relative_path = "./"   # Path to sensor data file relative to this python script (./ means data file is in the same directory as this python script)
        full_path = os.path.join(absolute_path, relative_path) # Full path to sensor data file
        filename = 'sensor-scan.txt' # Name of file you want to store sensor data from your sensor scan command

        # Choose to create either a UART or TCP port socket to communicate with Cybot (Not both!!)
        # UART BEGIN
        try:
            cybot = serial.Serial('COM100', 115200, timeout=1)  # UART (Make sure you are using the correct COM port and Baud rate!!)
            print("Successfully connected to CyBot via UART on COM100")
        except Exception as e:
            print(f"Failed to connect to CyBot via UART: {e}")
            return
        #UART END

        # TCP Socket BEGIN (See Echo Client example): https://realpython.com/python-sockets/#echo-client-and-server
       # HOST = "127.0.0.1"  # The server's hostname or IP address
       # PORT = 65432        # The port used by the server
       # cybot_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket object
       # cybot_socket.connect((HOST, PORT))   # Connect to the socket  (Note: Server must first be running)
       # cybot_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket object
       # try:
       #      cybot_socket.connect((HOST, PORT))  # Connect to the socket (Note: Server must first be running)
       #      print(f"Successfully connected to {HOST}:{PORT}")
       # except Exception as e:
       #      print(f"Failed to connect to {HOST}:{PORT}: {e}")
       #      return
                      
       # cybot = cybot_socket.makefile("rbw", buffering=0)  # makefile creates a file object out of a socket:  https://pythontic.com/modules/socket/makefile
        # TCP Socket END

        # Send some text: Either 1) Choose "Hello" or 2) have the user enter text to send
        send_message = "Hello\n"                            # 1) Hard code message to "Hello", or
        # send_message = input("Enter a message:") + '\n'   # 2) Have user enter text
        gui_send_message = "wait\n"  # Initialize GUI command message to wait                                

        cybot.write(send_message.encode()) # Convert String to bytes (i.e., encode), and send data to the server

        print("Sent to Cybot: " + send_message) 

        # Send messges to server until user sends "quit"
        while send_message != 'quit\n':
                
                # Update the GUI to display command being sent to the CyBot
                command_display = "Last Command Sent:\t" + send_message
                Last_command_Label.config(text = command_display)  
        
                # Check if a sensor scan command has been sent
                if (send_message == "M\n") or (send_message == "m\n"):

                        print("Requested Sensor scan from Cybot:\n")
                        rx_message = bytearray(1) # Initialize a byte array

                        # Create or overwrite existing sensor scan data file
                        file_object = open(full_path + filename,'w') # Open the file: file_object is just a variable for the file "handler" returned by open()

                        while (rx_message.decode() != "END\n"): # Collect sensor data until "END" recieved
                                rx_message = cybot.readline()   # Wait for sensor response, readline expects message to end with "\n"
                                file_object.write(rx_message.decode())  # Write a line of sensor data to the file
                                print(rx_message.decode()) # Convert message from bytes to String (i.e., decode), then print

                        file_object.close() # Important to close file once you are done with it!!                
                elif send_message.startswith("MOVE"):
                        print(f"Requested Move command: {send_message}")
                        rx_message = cybot.readline()  # Wait for server response
                        print("Server response: " + rx_message.decode())


                else:                
                        print("Waiting for server reply\n")
                        rx_message = cybot.readline()      # Wait for a message, readline expects message to end with "\n"
                        print("Got a message from server: " + rx_message.decode() + "\n") # Convert message from bytes to String (i.e., decode)

                
                # Choose either: 1) Idle wait, or 2) Request a periodic status update from the Cybot
                # 1) Idle wait: for gui_send_message to be updated by the GUI
                while gui_send_message == "wait\n":
                    time.sleep(.1)  # Sleep for .1 seconds
                send_message = gui_send_message

                gui_send_message = "wait\n"  # Reset gui command message request to wait                        

                cybot.write(send_message.encode())  # Convert String to bytes (i.e., encode), and send data to the CyBot

        print("Client exiting, and closing UART connection\n")
        time.sleep(2)  # Sleep for 2 seconds
        cybot.close()  # Close UART connection

                # 2) Request a periodic Status update from the Cybot:
                # every .1 seconds if GUI has not requested to send a new command
                #time.sleep(.1)
                #if(gui_send_message == "wait\n"):   # GUI has not requested a new command
                #        send_message = "status\n"   # Request a status update from the Cybot
                #else:
                #        send_message = gui_send_message  # GUI has requested a new command

       #         gui_send_message = "wait\n"  # Reset gui command message request to wait                        
#
 #               cybot.write(send_message.encode()) # Convert String to bytes (i.e., encode), and send data to the server
                
 #       print("Client exiting, and closing file descriptor, and/or network socket\n")
  #      time.sleep(2) # Sleep for 2 seconds
   #     cybot.close() # Close file object associated with the socket or UART
    #    cybot_socket.close()  # Close the socket (NOTE: comment out if using UART interface, only use for network socket option)

##### END Define Functions  #########
# Move Button action. Tells the client to send a move request to the Cybot
def send_move():
        global gui_send_message  # Command that the GUI has requested sent to the Cybot
        
        # Prompt the user to input the distance
        distance = tk.simpledialog.askstring("Input", "Enter distance to move:")
        if distance:
                gui_send_message = f"MOVE {distance}\n"  # Update the message for the Client to send


### Run main ###
main()

