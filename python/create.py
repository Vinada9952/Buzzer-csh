import socket
import random
import threading
import pygame

def play_mp3():
    # file = open( "../assets/audio.txt", 'r' )
    # file_path = "../assets/" + file.readline()
    # file.close()
    file_path = "./assets/shortBuzz.mp3"
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier : {e}")
    finally:
        pygame.mixer.music.stop()
        pygame.mixer.quit()



class Client:
    client = None
    ip = None
    name = None
    buzzed = 0

    def __init__( self, c, addr ):
        self.client = c
        self.ip = addr
    
    def send( self, msg ):
        self.client.send( msg.encode() )
    
    def receive( self ):
        x = self.client.recv( 1024 ).decode()
        return x
    
    def buzz( self ):
        global already_buzzed
        while True:
            x = self.receive()
            if x == "buzz" and self.buzzed == 0:
                self.buzzed = 1
                print( self.name, "buzzed" )
                send_to_all( "buzzed:" + self.name )
                if not already_buzzed:
                    already_buzzed = True
                    play_mp3()


def code():
    a = socket.gethostbyname( socket.gethostname() ).split( '.' )

    for i in range( len( a ) ):
        a[i] = str( hex( int( a[i] ) ) ).replace( '0x', '' )
        if len( a[i] ) == 1:
            a[i] = 'x' + a[i]
        

    print( ''.join( a ) )



def send_to_all( msg ):
    global client_list
    global clients

    for i in range( len( client_list ) ):
        clients[client_list[i]].send( msg )

s = socket.socket()

port = 57542

clients = {}
client_list = []
client_threads = []
already_buzzed = False

def connect():
    global clients
    global client_threads
    global client_list
    s.bind( ( '', port ) )
    while True:
        s.listen()
        a, b = s.accept()
        tmp_client = Client( a, b )
        tmp_client.send( "name?" )
        while True:
            name = tmp_client.receive()
            verification = False
            for i in client_list:
                if name == i:
                    verification = True
            if not verification:
                break
            else:
                tmp_client.send( "used" )
        tmp_client.send( "name_good" )


        tmp_client.name = name
        clients[name] = tmp_client
        client_list.append( name )
        client_threads.append( threading.Thread( target=clients[name].buzz ) )
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
            clients[ client_list[i] ].buzzed = 0
        already_buzzed = False



# ajouter le son - fait
# vérifier que le joueur buzz une seule fois, même du coté serveur - fait
# Faire que tout les joueurs savent qui a buzzé - fait
# deux joueurs ne peuvent pas avoir le même nom - à tester
# l'hôte ne doit pas crash quand des joueurs déconnectent