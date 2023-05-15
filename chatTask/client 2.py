import socket
import sys
import errno

# Length of the header used to send/receive messages
HEADER_LENGTH = 10

# IP address and port number of the server
IP = "127.0.0.1"
PORT = 1234

# Ask the user for their username
my_username = input("Username: ")

# Create a client socket using TCP connection
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the client socket to the server
client_socket.connect((IP, PORT))

# Set the socket to non-blocking mode so that recv() function does not block the program
client_socket.setblocking(False)

# Encode the username to bytes and prepare the header
username = my_username.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')

# Send the username to the server
client_socket.send(username_header + username)

# Infinite loop to send and receive messages
while True:
    # Ask the user for input
    message = input(f'{my_username} > ')

    # Send the message to the server if it's not empty
    if message:
        # Encode the message to bytes and prepare the header
        message = message.encode('utf-8')
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
        client_socket.send(message_header + message)

    try:
        # Loop over all the messages received from the server
        while True:
            # Receive the username header
            username_header = client_socket.recv(HEADER_LENGTH)

            # If no header is received, the connection is closed
            if not len(username_header):
                print('Connection closed by the server')
                sys.exit()

            # Convert the username header to an int value
            username_length = int(username_header.decode('utf-8').strip())

            # Receive the username and decode it to utf-8
            username = client_socket.recv(username_length).decode('utf-8')

            # Receive the message header
            message_header = client_socket.recv(HEADER_LENGTH)

            # Convert the message header to an int value
            message_length = int(message_header.decode('utf-8').strip())

            # Receive the message and decode it to utf-8
            message = client_socket.recv(message_length).decode('utf-8')

            # Print the message received from the server
            print(f'{username} > {message}')

    except IOError as e:
        # If the error is not related to the non-blocking socket, exit the program
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error: {}'.format(str(e)))
            sys.exit()

        # If there is no data to receive, continue to the next iteration
        continue

    except Exception as e:
        print('Reading error: {}'.format(str(e)))
        sys.exit()
