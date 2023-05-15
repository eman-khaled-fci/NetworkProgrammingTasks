import socket
import sys
import errno

# Define the length of the header for the username and message.
HEADER_LENGTH = 10

# Define the IP address and port number to connect to.
IP = "127.0.0.1"
PORT = 1234

# Get the client's username from the user.
my_username = input("Username: ")

# Create a socket and connect to the server.
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))

# Set the socket to non-blocking mode so we can use the select() function.
client_socket.setblocking(False)

# Encode the username and prepare the header for sending.
username = my_username.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')

# Send the username to the server.
client_socket.send(username_header + username)

# Enter an infinite loop to send and receive messages.
while True:
    # Get user input for a message to send.
    message = input(f'{my_username} > ')

    # If the message is not empty, prepare it for sending and send it.
    if message:
        message = message.encode('utf-8')
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
        client_socket.send(message_header + message)

    try:
        # Loop over received messages from the server.
        while True:
            # Get the header for the username.
            username_header = client_socket.recv(HEADER_LENGTH)

            # If no header is received, the server has closed the connection.
            if not len(username_header):
                print('Connection closed by the server')
                sys.exit()

            # Decode the username header to get the length of the username.
            username_length = int(username_header.decode('utf-8').strip())

            # Receive the username and decode it.
            username = client_socket.recv(username_length).decode('utf-8')

            # Receive the header for the message and decode it to get the message length.
            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode('utf-8').strip())

            # Receive the message and decode it.
            message = client_socket.recv(message_length).decode('utf-8')

            # Print the received message with the username of the sender.
            print(f'{username} > {message}')

    except IOError as e:
        # If we get a non-blocking I/O error, it means there is no data to receive.
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error: {}'.format(str(e)))
            sys.exit()

        # If there is no data to receive, continue the loop.
        continue

    except Exception as e:
        print('Reading error: '.format(str(e)))
        sys.exit()
