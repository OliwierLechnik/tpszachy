import socket
import threading
import sys
import select
# from shared.Board import Board
# from DrawableNode import DrawableNode

def recv_with_timeout(client_socket, timeout_ms):
    """
    Receive data from a socket with a specified timeout.

    Args:
        client_socket (socket.socket): The socket to receive data from.
        timeout_ms (int): Timeout in milliseconds.

    Returns:
        bytes or None: The received data, or None if no data is received within the timeout.
    """
    timeout_sec = timeout_ms / 1000.0  # Convert milliseconds to seconds
    ready, _, _ = select.select([client_socket], [], [], timeout_sec)
    if ready:
        return client_socket.recv(1024)  # Adjust the buffer size as needed
    return None
def actuallGameLoop(socket, mycolor, players):
    b = Board(DrawableNode)
    b.generateBoard()
    b.generatePawns(6)




def read_from_server(client_socket):
    while True:
        try:
            # Receive data from the server
            response = client_socket.recv(1024)
            if not response:
                break  # Connection closed
            if response.decode('ascii') == "Game Started.":

            print("Server says:", response.decode('ascii'))

        except Exception as e:
            print(f"Error while reading from server: {e}")
            break

def write_to_server(client_socket):
    while True:
        try:
            # Get user input and send to the server
            user_input = input("> ")
            if user_input.lower() == "exit":
                print("Closing connection...")
                client_socket.send(b"exit\n")  # Optionally, send "exit" to the server
                break
            client_socket.send((user_input + "\n").encode())
        except Exception as e:
            print(f"Error while sending data: {e}")
            break

def telnet_client(host, port):
    try:
        # Create a socket and connect to the server
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))

        # Start a thread to handle reading from the server
        read_thread = threading.Thread(target=read_from_server, args=(client_socket,))
        read_thread.daemon = True
        read_thread.start()

        # Start the main loop to handle writing to the server
        write_to_server(client_socket)

        # Close the connection after exiting the write loop
        client_socket.close()
        print("Connection closed.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    host = "127.0.0.1"  # Replace with the IP of the server you want to connect to
    port = 42069  # Default Telnet port, or specify the correct port if needed

    telnet_client(host, port)