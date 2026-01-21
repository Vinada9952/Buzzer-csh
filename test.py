# custom sounds

import requests
from pydub import AudioSegment
from pydub.playback import play


response = requests.get(input("Enter the MyInstants sound page URL: "))

page = response.text
sound_line = ''
for line in page.split( '\n' ):
    if line.find( '.mp3' ) != -1:
        sound_line = line
        break

url = "https://www.myinstants.com" + sound_line.split( "'" )[1]
print( url )