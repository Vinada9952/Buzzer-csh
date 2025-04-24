# Import socket module 
import socket

def decode( room ):
    a = []
    for i in range( 4 ):
        a.append( str( int( room[i+i].replace( 'x', '' ) + room[i+i+1].replace( 'x', '' ), 16 ) ) )
    return '.'.join( a )

# Create a socket object 
s = socket.socket()

# Define the port on which you want to connect 
port = 57542

# connect to the server on local computer 
s.connect( ( '192.168.0.114', port ) )

# receive data from the server and decoding to get the string.
print ( s.recv( 1024 ).decode() )
# close the connection
s.close()