import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('localhost', 4000)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)

sock.sendto('{ "power": 123, "cadence": 50 }'.encode(), ('localhost', 3000))
