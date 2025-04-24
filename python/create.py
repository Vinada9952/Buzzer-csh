# first of all import the socket library
import socket
import random
import threading

class Client:
    client = None
    ip = None
    name = None

    def __init__( self, c, addr ):
        self.client = c
        self.ip = addr
    
    def send( self, msg ):
        self.client.send( msg.encode() )
    
    def receive( self ):
        x = self.client.recv( 1024 ).decode()
        return x
    
    def buzzed( self ):
        while True:
            x = self.receive()
            if x == "buzz":
                print( self.name, "buzzed" )

def code():
    a = socket.gethostbyname( socket.gethostname() ).split( '.' )

    for i in range( len( a ) ):
        a[i] = str( hex( int( a[i] ) ) ).replace( '0x', '' )
        if len( a[i] ) == 1:
            a[i] = 'x' + a[i]
        

    print( ''.join( a ) )




# next create a socket object
s = socket.socket()

# reserve a port on your computer in our
# case it is 57542 but it can be anything

port = 57542

# Next bind to the port 
# we have not typed any ip in the ip field
# instead we have inputted an empty string
# this makes the server listen to requests
# coming from other computers on the network

clients = {}
client_list = []
client_threads = []

def connect():
    global clients
    global client_threads
    s.bind( ( '', port ) )
    while True:
        s.listen()
        a, b = s.accept()
        tmp_client = Client( a, b )
        tmp_client.send( "name?" )
        name = tmp_client.receive()
        tmp_client.name = name
        clients[name] = tmp_client
        client_list.append( name )
        client_threads.append( threading.Thread( target=clients[name].buzzed ) )
        client_threads[len( client_threads )-1].start()


code()


th_connect = threading.Thread( target=connect )
th_connect.start()
while True:
    if input() == '':
        print( "\n\n"*100 )
        print( "player buzzed:" )
        for i in range( len( client_list ) ):
            clients[ client_list[i] ].send( 'reset' )