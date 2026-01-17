from flask import Flask
import random

app = Flask(__name__)

room_example = {
    "code": 9952,
    "state": "reset", # reset : No one buzzed. buzzes : someone buzzed
    "type": "button", # button : buzzing button. text : text input
    "buzzed_players": [
        {
            "name": "Player1",
            "answer": "Answer1",
            "timestamp_buzz": 1768663825462
        }
    ],
    "players": [
        "Player2"
    ]
}

rooms = []

@app.route( '/' )
def main_menu():
    return Pages.MAIN_PAGE

@app.route( '/create' )
def create_menu():
    return Pages.CREATE_PAGE

@app.route( '/join' )
def join_menu():
    return Pages.JOIN_PAGE

@app.route( "/create-room" )
def create_room():
    room_code = 9952
    while room_code == 9952:
        room_code = random.randint( 1000, 9999 )
    new_room = {
        "code": room_code,
        "state": "reset",
        "type": "button",
        "buzzed_players": [],
        "players": []
    }
    rooms.append( new_room )
    return new_room

class Pages:
    MAIN_PAGE = """<!DOCTYPE html>
<html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Buzzer CSH</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                background-color: #292c34;
            }



            #container {
                text-align: center;
                background: #2e313d;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                width: 90%;
                max-width: 500px;
            }

            button {
                padding: 10px 20px;
                background-color: #cea6eb;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }


            button:hover {
                padding: 10px 20px;
                background-color: #c08ae6;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }
        </style>
    </head>
    <body>
            <div id="container">
                <h1 style="color: white;">CSH buzzer</h1>
                <button id="join-button">Rejoindre</button>
                <button id="create-button">Créer une salle</button>
            </div> 
            <script>
                document.getElementById('join-button').onclick = function() {
                    window.location.href = 'http://192.168.0.110:9952/join';
                };
                document.getElementById('create-button').onclick = function() {
                    window.location.href = 'http://192.168.0.110:9952/create';
                };
            </script>
    </body>
</html>"""
    CREATE_PAGE = """<!DOCTYPE html>
<html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Buzzer CSH</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                background-color: #292c34;
            }



            #container {
                text-align: center;
                background: #2e313d;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                width: 90%;
                max-width: 500px;
            }


            button {
                padding: 10px 20px;
                background-color: #cea6eb;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }


            button:hover {
                padding: 10px 20px;
                background-color: #c08ae6;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }
        </style>
    </head>
    <body>
        <div id="container">
            
            <h1 style="color: white;">Buzzer CSH</h1>

            <h3 style="color: white;" id="room-code">Code de salle : </h3>

            <button id="buzz-answer">Rénitialiser et mettre une question collective</button>
            <br><br>
            <button id="type-answer">Rénitialiser et mettre une question par écrit</button>

            <h2 style="color: white;">Joueurs ayant buzzé</h2>
            <div id="players-buzzed" style="color: white;"></div>
            <h2 style="color: white;">Joueurs</h2>
            <div id="players" style="color: white;"></div>
        </div>
        <script>
            fetch('http://192.168.0.110:9952/create-room', {
                method: 'GET',
            })
            .then(response => response.json())
            .then(data => {
                console.log(data.code);
                document.getElementById('room-code').innerText += " " + data.code;
            })
            .catch(error => console.error('Erreur:', error));
        </script>
    </body>
</html>"""
    JOIN_PAGE = """
"""

if __name__ == '__main__':
    app.run( host='192.168.0.110', port=9952 )