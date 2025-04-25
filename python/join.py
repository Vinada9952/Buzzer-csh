import socket
import random
import threading
import pygame

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




def decode( room ):
    a = []
    for i in range( 4 ):
        a.append( str( int( room[i+i].replace( 'x', '' ) + room[i+i+1].replace( 'x', '' ), 16 ) ) )
    return '.'.join( a )

s = socket.socket()

port = 57542

s.connect( ( decode( input( "room code\n-> " ) ), port ) )

while True:
    x = s.recv( 1024 ).decode()
    if x == "name?":
        name = input( "name\n-> " )
        s.send( name.encode() )
    elif x == "used":
        print( "name already used" )
        name = input( "name\n-> " )
        s.send( name.encode() )
    elif x == "name_good":
        break
    else:
        print( "error" )
        exit( 0 )




buzzed = False
buzzed_list = []

def buzz():
    global buzzed
    global buzzed_list
    while True:
        input()
        if not buzzed:
            buzzed = True
            s.send( 'buzz'.encode() )

def revc():
    global buzzed_list
    global buzzed
    while True:
        recv = s.recv( 1024 ).decode()
        if recv == 'reset':
            buzzed = False
            print( "\n\n"*100 )
            print( "buzz" )
        elif recv.find( "buzzed:" ) == 0:
            recv = recv.replace( 'buzzed:', '' )
            buzzed_list.append( recv )
            print( '\n\n'*100 )
            print( "player buzzed:" )
            for i in range( len( buzzed_list ) ):
                print( buzzed_list[i] )
            if len( buzzed_list ) == 1:
                play_mp3()
            if not buzzed:
                print( "buzz" )


print( "\n\n"*100 )
print( "buzz" )

th_buzz = threading.Thread( target=buzz )
th_revc = threading.Thread( target=revc )

th_buzz.start()
th_revc.start()