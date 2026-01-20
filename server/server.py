from flask import Flask, request
import random

app = Flask(__name__)

room_example = {
    "code": 9952,
    "state": "reset", # reset : No one buzzed. buzzed : someone buzzed
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
    code_exists = True
    while code_exists:
        room_code = random.randint( 1000, 9999 )
        code_exists = False
        for room in rooms:
            if room["code"] == room_code:
                code_exists = True
    new_room = {
        "code": room_code,
        "state": "reset",
        "type": "button",
        "buzzed_players": [],
        "players": []
    }
    rooms.append( new_room )
    print( rooms )
    return new_room

@app.route( "/join-room", methods=["POST"] )
def join_room():
    global rooms
    json = None
    try:
        json = request.get_json( force=True )
    except Exception as e:
        print("Erreur JSON :", e)
        return {"error": "invalid JSON"}, 400
    
    code = json.get("code")
    name = json.get("name")
    return_json = {
        "valid_code": False,
        "valid_name": True
    }

    for room in rooms:
        if room["code"] == code:
            return_json["valid_code"] = True
            for player in room["players"]:
                if player == name:
                    return_json["valid_name"] = False
            for player in room["buzzed_players"]:
                if player["name"] == name:
                    return_json["valid_name"] = False
    
    if return_json["valid_code"] and return_json["valid_name"]:
        for room in rooms:
            if room["code"] == code:
                room["players"].append( name )
                break
    
    print( rooms )
    return return_json

@app.route( "/get_room", methods=["POST"] )
def get_room():
    json = None
    try:
        json = request.get_json( force=True )
    except Exception as e:
        print("Erreur JSON :", e)
        return {"error": "invalid JSON"}, 400

    code = json.get("code")
    for room in rooms:
        if room["code"] == code:
            return room
    return {"error": "room not found"}, 404

@app.route( "/get_all", methods=["POST"] )
def get_all():
    json = None
    try:
        json = request.get_json( force=True )
    except Exception as e:
        print("Erreur JSON :", e)
        return {"error": "invalid JSON"}, 400

    pwd = json.get("pwd")
    if pwd == 175028:
        return rooms
    return {"error": "invalid password"}, 404

@app.route( "/buzz", methods=["POST"] )
def buzz():
    json = None
    try:
        json = request.get_json( force=True )
    except Exception as e:
        print("Erreur JSON :", e)
        return {"error": "invalid JSON"}, 400
    
    print( "BUZZ" )
    print( json )
    room_code = json.get("code")
    player_name = json.get("player")
    time_buzz = json.get("time")
    for room in rooms:
        if room["code"] == room_code:
            room["buzzed_players"].append(
                {
                    "name": player_name,
                    "answer": "",
                    "timestamp_buzz": time_buzz
                }
            )
            room["state"] = "buzzed"
            # print( "remove", player_name, "from", room["players"] )
            room["players"].remove( player_name )
            room["buzzed_players"].sort( key=lambda x: x["timestamp_buzz"] )
    print( rooms )
    return {"success": True}

@app.route( "/submit", methods=["POST"] )
def submit_answer():
    json = None
    try:
        json = request.get_json( force=True )
    except Exception as e:
        print("Erreur JSON :", e)
        return {"error": "invalid JSON"}, 400
    
    room_code = json.get("code")
    player_name = json.get("player")
    answer_text = json.get("answer")
    time_buzz = json.get("time")
    for room in rooms:
        if room["code"] == room_code:
            room["buzzed_players"].append(
                {
                    "name": player_name,
                    "answer": answer_text,
                    "timestamp_buzz": time_buzz
                }
            )
            room["state"] = "buzzed"
            room["players"].remove( player_name )
            room["buzzed_players"].sort( key=lambda x: x["timestamp_buzz"] )
    print( rooms )
    return {"success": True}

@app.route( "/reset-room", methods=["POST"] )
def reset_room():
    json = None
    try:
        json = request.get_json( force=True )
    except Exception as e:
        print("Erreur JSON :", e)
        return {"error": "invalid JSON"}, 400

    room_code = json.get("code")
    reset_type = json.get("type")
    print( reset_type )
    for room in rooms:
        if room["code"] == room_code:
            room["state"] = "reset"
            room["type"] = "button" if reset_type == "buzz" else "text"
            for player in room["buzzed_players"]:
                room["players"].append( player["name"] )
            room["buzzed_players"] = []
    print( rooms )
    return {"success": True}

@app.route( "/close-room", methods=["POST"] )
def close_room():
    json = None
    try:
        json = request.get_json( force=True )
    except Exception as e:
        print("Erreur JSON :", e)
        return {"error": "invalid JSON"}, 400

    room_code = json.get("code")
    for room in rooms:
        if room["code"] == room_code:
            rooms.remove( room )
            break
    print( rooms )
    return {"success": True}

@app.route( "/quit-player", methods=["POST"] )
def quit_player():
    json = None
    try:
        json = request.get_json( force=True )
    except Exception as e:
        print("Erreur JSON :", e)
        return {"error": "invalid JSON"}, 400

    room_code = json.get("code")
    player_name = json.get("player")
    for room in rooms:
        if room["code"] == room_code:
            if player_name in room["players"]:
                room["players"].remove( player_name )
            if player_name in [p["name"] for p in room["buzzed_players"]]:
                room["buzzed_players"] = [p for p in room["buzzed_players"] if p["name"] != player_name]
            break
    print( rooms )
    return {"success": True}

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
                    window.location.href = 'http://127.0.0.1:9952/join';
                };
                document.getElementById('create-button').onclick = function() {
                    window.location.href = 'http://127.0.0.1:9952/create';
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

            #reset-buttons {
                flex-direction: column;
                align-items: center;
                align-content: center;
                align-self: center;
            }
            
            #buzz-answer {
                align-content: center;
                align-items: center;
                align-self: center;
            }
            
            #type-answer {
                align-content: center;
                align-items: center;
                align-self: center;
            }
        </style>
    </head>
    <body>
        <div id="container">
            
            <h1 style="color: white;">Buzzer CSH</h1>

            <h3 style="color: white;" id="room-code">Code de salle : </h3>

            <div id="reset-buttons">
                <button id="buzz-answer">Réinitialiser - question collective</button>
                <br><br>
                <button id="type-answer">Réinitialiser - question écrite</button>
            </div>

            <h2 style="color: white;">Joueurs ayant buzzé</h2>
            <div id="players-buzzed" style="color: white;"></div>
            <h2 style="color: white;">Joueurs</h2>
            <div id="players" style="color: white;"></div>
        </div>
        <script>
            globalThis.buzz_sound = new Audio( "https://www.myinstants.com/media/sounds/wrong-answer-sound-effect.mp3" )
            globalThis.last_state = "none";

            globalThis.room_code = 0;
            fetch('http://127.0.0.1:9952/create-room', {
                method: 'GET',
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('room-code').innerText += " " + data.code;
                room_code = data.code;
            })
            .catch(error => console.error('Erreur:', error));

            document.getElementById('buzz-answer').onclick = function() {
                fetch('http://127.0.0.1:9952/reset-room', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ code: room_code, type: "buzz" }),
                })
                .then(response => response.json())
                .then(data => {})
                .catch(error => console.error('Erreur:', error));
            }

            document.getElementById('type-answer').onclick = function() {
                fetch('http://127.0.0.1:9952/reset-room', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ code: room_code, type: "text" }),
                })
                .then(response => response.json())
                .then(data => {})
                .catch(error => console.error('Erreur:', error));
            }

            window.addEventListener("beforeunload", function (e) {
                fetch('http://127.0.0.1:9952/close-room', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ code: room_code }),
                })
            });

            setInterval(function() {
                if( room_code == 0 ) return;
                fetch('http://127.0.0.1:9952/get_room', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ code: room_code }),
                })
                .then(response => response.json())
                .then(data => {
                    if( data.error ) {
                        alert("Impossible de trouver la salle !");
                        window.location.reload();
                    }

                    if( last_state == "reset" && data.state == "buzzed" && data.type == "button" ) {
                        buzz_sound.play();
                    }

                    type_state = 'block';
                    buzz_state = 'block';
                    console.log( "data.state = " + data.state );
                    if( data.type == "text" ) {
                        document.getElementById('players-buzzed').innerHTML = data.buzzed_players.map(player => `<div>${player.name + " : " + player.answer + "<br>"}</div>`).join('');
                        document.getElementById('players').innerHTML = data.players.map(player => `<div>${player}</div>`).join('');
                        if( data.state == "reset" ) {
                            type_state = 'none';
                        }
                    }
                    if( data.type == "button" ) {
                        document.getElementById('players-buzzed').innerHTML = data.buzzed_players.map(player => `<div>${player.name+"<br>"}</div>`).join('');
                        document.getElementById('players').innerHTML = data.players.map(player => `<div>${player}</div>`).join('');
                        if( data.state == "reset" ) {
                            buzz_state = 'none';
                        }
                    }
                    document.getElementById( "type-answer" ).style.display = type_state;
                    document.getElementById( "buzz-answer" ).style.display = buzz_state;
                    document.getElementById( "reset-buttons" ).style.display = "flex";
                    last_state = data.state;
                })
                .catch(error => console.error('Erreur:', error));
            }, 100);
        </script>
    </body>
</html>"""
    JOIN_PAGE = """<!DOCTYPE html>
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

            #buzzer {
                background-color: #cea6eb;
                border: none;
                color: white;
                padding: 110px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin: 4px 2px;
                border-radius: 50%;
            }

            #buzzer:hover {
                background-color: #c08ae6;
                border: none;
                color: white;
                padding: 110px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin: 4px 2px;
                border-radius: 50%;
            }

            #buzzed {
                display: none;
            }

            #buzzer-buzzed {
                background-color: #292c34;
                border: none;
                color: white;
                padding: 110px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin: 4px 2px;
                border-radius: 50%;
            }

            input {
                width: 80%;
                padding: 10px;
                margin: 10px 0;
                border: 1px solid #ccc;
                border-radius: 5px;
            }


            #in-game {
                display: none;
            }

            #type-answer {
                display: none;
                flex-direction: column;
                align-items: center;
            }

            #type-answer input {
                width: 80%;
            }

            #type-answer button {
                width: auto;
            }
        </style>
    </head>
    <body>
        <div id="container">
            
            <h1 style="color: white;">Buzzer CSH</h1>

            <div id="room-code">
                <input type="text" id="room-code-input" placeholder="Code de la salle" required><br>
                <input type="text" id="player-name-input" placeholder="Votre nom" required><br>
                <button id="room-code-submit">Entrer</button>
            </div>
            
            <div id="in-game">
                <div id="buzz-answer">
                    <div id="no-buzzed">
                        <button id="buzzer">Buzz</button>
                    </div>
                    <div id="buzzed">
                        <button id="buzzer-buzzed">Buzzed</button>
                    </div>
                </div>

                <div id="type-answer">
                    <input type="text" id="answer-input" placeholder="Entrez votre réponse" required><br>
                    <button id="answer-submit">Soumettre</button>
                </div>

                <h2 style="color: white;">Joueurs ayant buzzé</h2>
                <div id="players-buzzed" style="color: white;"></div>
                <h2 style="color: white;">Joueurs</h2>
                <div id="players" style="color: white;"></div>
            </div>
        </div>
        <script>
            globalThis.buzz_sound = new Audio( "https://www.myinstants.com/media/sounds/wrong-answer-sound-effect.mp3" )
            globalThis.last_state = "none";
            globalThis.room_code = 0;
            globalThis.player_name = "";
            document.getElementById('room-code-submit').onclick = function() {
                room_code = parseInt( document.getElementById('room-code-input').value );
                player_name = document.getElementById('player-name-input').value;

                fetch('http://127.0.0.1:9952/join-room', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ code: room_code, name: player_name }),
                })
                .then(response => response.json())
                .then(data => {
                    if( data.valid_code == false ) {
                        alert("Code de salle invalide !");
                        return;
                    }
                    if( data.valid_name == false ) {
                        alert("Nom invalide !");
                        return;
                    }
                    document.getElementById('room-code').style.display = 'none';
                    document.getElementById('in-game').style.display = 'block';
                })
                .catch(error => console.error('Erreur:', error));
            };

            document.getElementById('buzzer').onclick = function() {
                document.getElementById('no-buzzed').style.display = 'none';
                document.getElementById('buzzed').style.display = 'block';
                fetch('http://127.0.0.1:9952/buzz', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ code: room_code, player: player_name, time: Date.now() }),
                })
                .then(response => response.json())
                .then(data => {})
                .catch(error => console.error('Erreur:', error));
            };

            document.getElementById('answer-submit').onclick = function() {
                document.getElementById('answer-submit').style.display = 'none';
                fetch('http://127.0.0.1:9952/submit', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ code: room_code, player: player_name, answer: document.getElementById('answer-input').value, time: Date.now() }),
                })
                .then(response => response.json())
                .then(data => {})
                .catch(error => console.error('Erreur:', error));
                document.getElementById('answer-input').value = "";
            };

            window.addEventListener("beforeunload", function (e) {
                fetch('http://127.0.0.1:9952/quit-player', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ code: room_code, name: player_name }),
                })
            });

            setInterval(function() {
                if( room_code == 0 ) return;
                fetch('http://127.0.0.1:9952/get_room', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ code: room_code }),
                })
                .then(response => response.json())
                .then(data => {
                    if( data.error ) {
                        // alert("Erreur lors de la récupération de la salle !");
                        window.location.reload();
                    }

                    if( last_state == "reset" && data.state == "buzzed" && data.type == "button" ) {
                        buzz_sound.play();
                    }
                    document.getElementById('players-buzzed').innerHTML = data.buzzed_players.map(player => `<div>${player.name}<br></div>`).join('');
                    document.getElementById('players').innerHTML = data.players.map(player => `<div>${player}</div>`).join('');
                    if( data.state == "reset" ) {
                        if( data.type == "button" ) {
                            document.getElementById('buzz-answer').style.display = 'block';
                            document.getElementById('no-buzzed').style.display = 'block';
                            document.getElementById('buzzed').style.display = 'none';
                            document.getElementById('type-answer').style.display = 'none';
                        } else if( data.type == "text" ) {
                            document.getElementById('buzz-answer').style.display = 'none';
                            document.getElementById('type-answer').style.display = 'flex';
                            document.getElementById('answer-input').style.display = 'block';
                            document.getElementById('answer-submit').style.display = 'block';
                        }
                    }
                    if( data.state == "buzzed" && !data.players.includes(player_name) ) {
                        if( data.type == "button" ) {
                            document.getElementById('no-buzzed').style.display = 'none';
                            document.getElementById('buzzed').style.display = 'block';
                        } else if( data.type == "text" ) {
                            document.getElementById('answer-submit').style.display = 'none';
                            document.getElementById('answer-input').value = "";
                        }
                    }
                    last_state = data.state;
                })
                .catch(error => console.error('Erreur:', error));
            }, 100);
        </script>
    </body>
</html>"""

if __name__ == '__main__':
    app.run( host='0.0.0.0', port=9952 )