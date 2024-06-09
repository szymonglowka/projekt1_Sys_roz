baimport socket
import sys

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def connect(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.host, self.port))
            print("Połączono z", self.client_socket)
        except Exception as e:
            print("Błąd połączenia:", e)
            sys.exit(-1)

    def start(self):
        try:
            while True:
                line = input()
                if line:
                    print("Wysyłam:", line)
                    self.client_socket.sendall((line + "\r\n").encode())

                    if line == "quit":
                        print("Kończenie pracy...")
                        self.client_socket.close()
                        sys.exit(0)

                    response = self.client_socket.recv(1024).decode()
                    print("Otrzymano:", response)
        except Exception as e:
            print("Błąd wejścia-wyjścia:", e)
            sys.exit(-1)

if __name__ == "__main__":
    host = "localhost"
    port = 7005

    client = Client(host, port)
    client.connect()
    client.start()
