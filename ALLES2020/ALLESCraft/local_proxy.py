"""
This script should first accept an incomming connection from 
ALLES!. Next, it should start listening on :25565 and create a
comms channel.

When my cracked mc client connects to the proxy, it will actually connect, directly to the ALLES server, bypassing bungee and it's firewall rules.
"""

import socket

MC_PORT = 25567
CTF_PORT = 1337
# Should be quite large to allow initial chuck load
SIZE = 4096

s_ctf = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_ctf.bind(("", CTF_PORT))
s_ctf.listen()

# Now we can accept minecraft connections
s_mc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_mc.bind(("", MC_PORT))
s_mc.listen()

# Wait for the chal server to connect
ctf_conn, ctf_addr = s_ctf.accept()
print("Incomming connection from chal {}".format(ctf_addr))
ctf_conn.settimeout(0.5)

# For testing
#ctf_conn = s_ctf.connect(("127.0.0.1", 25565))


# Wait for my cracked client to connect
mc_conn, mc_addr = s_mc.accept()
mc_conn.settimeout(0.5)
print("Minecraft client connected from {}".format(mc_addr))


while True:
    # [MC] --> [Alles Proxy]
    try:
        client_data = mc_conn.recv(SIZE)
        ctf_conn.send(client_data)
#        print(">send")
    except socket.timeout:
        pass
    # [MC] <-- [Alles Proxy]
    try:
        ctf_data = ctf_conn.recv(SIZE)
        mc_conn.send(ctf_data)
 #       print("<recv")
    except socket.timeout:
        pass

