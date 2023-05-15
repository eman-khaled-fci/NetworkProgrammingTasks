import socket
import sys
import errno

# Defining the length of the header.
HEADER_LENGTH = 10

# Defining the IP address and Port Number.
IP = "127.0.0.1"
PORT = 1234

# Getting the name of the client.
my_username = input("Username: ")

# Creating a new client socket.
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connecting to the server.
client_socket.connect((IP, PORT))

# Setting the socket to non-blocking mode.
client_socket.setblocking(False)

# Encoding the username into bytes and preparing the header.
username = my_username.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')

# Sending the username header and username to the server.
client_socket.send(username_header + username)

# Running an infinite loop to send continuous client requests.
while True:
    # Getting user input.
    message = input(f'{my_username} > ')

    # Sending the message if it's not empty.
    if message:
        # Encoding the message into bytes and preparing the header.
        message = message.encode('utf-8')
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')

        # Sending the message header and message to the server.
        client_socket.send(message_header + message)

    try:
        # Looping over the received messages and printing them.
        while True:
            # Receiving the username header from the server.
            username_header = client_socket.recv(HEADER_LENGTH)

            # If no header is received, the server has closed the connection.
            if not len(username_header):
                print('Connection closed by the server')
                sys.exit()

            # Converting the header to an int value.
            username_length = int(username_header.decode('utf-8').strip())

            # Receiving the username from the server and decoding it.
            username = client_socket.recv(username_length).decode('utf-8')

            # Receiving the message header from the server.
            message_header = client_socket.recv(HEADER_LENGTH)

            # Converting the message header to an int value.
            message_length = int(message_header.decode('utf-8').strip())

            # Receiving the message from the server and decoding it.
            message = client_socket.recv(message_length).decode('utf-8')

            # Printing the received message.
            print(f'{username} > {message}')

    except IOError as e:
        # Handling normal errors on non-blocking connections.
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error: {}'.format(str(e)))
            sys.exit()

        # If we did not receive anything, continue.
        continue

    except Exception as e:
        print('Reading error: '.format(str(e)))
        sys.exit()
