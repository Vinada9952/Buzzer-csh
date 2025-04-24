# first of all import the socket library
import socket
import random
import threading

def code():
    a = socket.gethostbyname( socket.gethostname() ).split( '.' )

    for i in range( len( a ) ):
        a[i] = str( hex( int( a[i] ) ) ).replace( '0x', '' )
        if len( a[i] ) == 1:
            a[i] = 'x' + a[i]
        

    return ''.join( a )

print( "room code :", code() )

class Client:
    client = None
    ip = None
    name = None


# next create a socket object
s = socket.socket()
print( "Socket successfully created" )

# reserve a port on your computer in our
# case it is 57542 but it can be anything

port = 57542

# Next bind to the port 
# we have not typed any ip in the ip field
# instead we have inputted an empty string
# this makes the server listen to requests
# coming from other computers on the network



def connect():
    while True:
        s.bind( ( '', port ) )
        s.listen()

# a forever loop until we interrupt it or
# an error occurs
while True:

    c, addr = s.accept()
    print( 'Got connection from', addr )

    # send a thank you message to the client. encoding to send byte type.
    c.send( 'Thank you for connecting'.encode() )

    # Close the connection with the client
    c.close()

    # Breaking once connection closed
    break
