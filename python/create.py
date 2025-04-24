import socket
import random
import threading
import pygame
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL

def play_mp3():
    file = open( "../assets/audio.txt", 'r' )
    file_path = "../assets/" + file.readline()
    file.close()
    try:
        set_volume( 50 )
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


def set_volume( level ):
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = interface.QueryInterface(IAudioEndpointVolume)
        
        volume.SetMasterVolumeLevelScalar(level/100, None)
    except Exception as e:
        print(f"Erreur lors du réglage du volume : {e}")




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
        already_buzzed = False



# ajouter le son - fait
# vérifier que le joueur buzz une seule fois, même du coté serveur - fait
# Faire que tout les joueurs savent qui a buzzé