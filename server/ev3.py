import socket
import threading
import json

class EV3Connection(threading.Thread):
    PASSWORD = "ev3pass"

    def __init__(self, host, port, move_state, color):
        super(EV3Connection, self).__init__()

        self._move_state = move_state
        self._color = color

        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        print(f"Starting EV3 server on {host}:{port}...")
        self._socket.bind((host, port))

    def __del__(self):
        print("Closing EV3 server...")
        self._socket.close()

    def run(self):
        while True:
            self._socket.listen()
            conn, addr = self._socket.accept()

            with conn:
                try:
                    print(f"Connection from {addr}")
                    data = conn.recv(1024)

                    sent_password = data.decode("utf-8")

                    if sent_password == EV3Connection.PASSWORD:
                        print(f"Authenticated sucessfully!")
                        self.handle_connection(conn)
                    else:
                        print(f"Password '{sent_password}' incorrect!")
                        conn.sendall("incorrect password".encode())
                        conn.close()
                except (ConnectionError, TimeoutError, UnicodeDecodeError):
                    print(f"Connection from {addr} lost.")
                    continue

    def handle_connection(self, conn):
        conn.sendall("connected".encode())
        conn.settimeout(5.0)

        while True:
            data = conn.recv(512)
            command = data.decode("utf-8")

            try:
                command_json = json.loads(command)

                if not command:
                    raise ConnectionError
            except json.decoder.JSONDecodeError:
                raise ConnectionError

            if "rgb" in command_json.keys():
                self._color.update(command_json)

                move_state = json.dumps(self._move_state)
                conn.sendall(move_state.encode())
