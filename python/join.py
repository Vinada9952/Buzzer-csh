import socket
import random
import threading
import pygame
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL

def play_mp3():
    # file = open( "../assets/audio.txt", 'r' )
    # file_path = "../assets/" + file.readline()
    # file.close()
    file_path = "../assets/shortBuzz.mp3"
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


def set_volume( level ):
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = interface.QueryInterface(IAudioEndpointVolume)
        
        volume.SetMasterVolumeLevelScalar(level/100, None)
    except Exception as e:
        print(f"Erreur lors du réglage du volume : {e}")


def decode( room ):
    a = []
    for i in range( 4 ):
        a.append( str( int( room[i+i].replace( 'x', '' ) + room[i+i+1].replace( 'x', '' ), 16 ) ) )
    return '.'.join( a )

s = socket.socket()

port = 57542

s.connect( ( decode( input( "room code\n-> " ) ), port ) )

if s.recv( 1024 ).decode() == 'name?':
    name = input( "name\n-> " )
    print( name )
    s.send( name.encode() )

buzzed = 0
buzzed_list = []

def buzz():
    global buzzed
    global buzzed_list
    while True:
        input()
        if buzzed == 0:
            buzzed = 1
            s.send( 'buzz'.encode() )
            play_mp3()

def revc():
    global buzzed_list
    global buzzed
    while True:
        recv = s.recv( 1024 ).decode()
        if recv == 'reset':
            buzzed = 0
            print( "\n\n"*100 )
            print( "buzz" )
        elif recv == 0:
            recv = recv.replace( 'buzzed:', '' )
            buzzed_list.append( recv )
            print( '\n\n'*100 )
            for i in range( len( buzzed_list ) ):
                print( buzzed_list[i] )
            print( "buzz" )


print( "\n\n"*100 )
print( "buzz" )

th_buzz = threading.Thread( target=buzz )
th_revc = threading.Thread( target=revc )

th_buzz.start()
th_revc.start()