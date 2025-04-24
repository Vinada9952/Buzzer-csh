# Import socket module 
import socket
import threading

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
s.connect( ( decode( input( "room code\n-> " ) ), port ) )

if s.recv( 1024 ).decode() == 'name?':
    name = input( "name\n-> " )
    print( name )
    s.send( name.encode() )

buzzed = 0

def buzz():
    global buzzed
    while True:
        input()
        if buzzed == 0:
            s.send( 'buzz'.encode() )
            print( "\n\n"*100 )
            print( "buzzed" )

def reset():
    global buzzed
    while True:
        if s.recv( 1024 ).decode() == 'reset':
            buzzed = 0
            print( "\n\n"*100 )
            print( "buzz" )

print( "\n\n"*100 )
print( "buzz" )

th_buzz = threading.Thread( target=buzz )
th_reset = threading.Thread( target=reset )

th_buzz.start()
th_reset.start()