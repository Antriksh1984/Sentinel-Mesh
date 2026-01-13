import socket
import time

BANNER = b"SSH-2.0-OpenSSH_7.4p1 Debian-10\r\n"

s = socket.socket()
s.bind(("0.0.0.0", 22))
s.listen(5)

while True:
    conn, addr = s.accept()
    conn.send(BANNER)
    time.sleep(1)
    conn.close()
