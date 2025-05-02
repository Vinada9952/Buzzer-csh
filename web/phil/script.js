const socket = io("http://localhost:3000");

buzzed = false;
console.log( "buzzed : ", buzzed );
playerName = "";
all_buzzed = false;
type = "buzz";

document.getElementById("room-code-submit").addEventListener("click", startGame);

function startGame() {
    const roomCode = document.getElementById("room-code-input").value;
    playerName = document.getElementById("player-name-input").value;

    if (roomCode.trim() === "" || playerName.trim() === "") {
        alert("Veuillez entrer un code de salle et un nom valide.");
        return;
    }

    // Envoyer le code de la salle et le nom du joueur au serveur
    socket.emit("join-room", roomCode, playerName );
    console.log( "room-code : ", roomCode );
    console.log( "playerName : ", playerName );

    console.log("game start");
    document.getElementById("in-game").style.display = "block";
    document.getElementById("room-code").style.display = "none";
}


// Gérer les événements du serveur
socket.on("update-players", (players) => {
    console.log( "update-players", players )
    document.getElementById("players").innerText = "";
    const playersDiv = document.getElementById("players");
    for( let i = 0; i < players.length; i++ ) {
        if( players[i] != "host")
        {
            playersDiv.innerText += players[i]+"\n";
        }
    }

    ver = true;
    for( let i = 0; i < players.length; i++ ) {
        if( players[i] == "host" )
        {
            ver = false;
        }
    }
    console.log( ver )
    if( ver ) {
        console.log( "reload" );
        location.reload();
    }
});

socket.on("player-buzzed", (player) => {
    const buzzedDiv = document.getElementById("players-buzzed");
    buzzedDiv.innerHTML += `<p>${player}</p>`;
    console.log( "player : ", player );
    if( !all_buzzed )
    {
        const audio = new Audio('https://cdn.glitch.global/fff151b3-947e-47f6-9965-3a1e4ae8d6ea/shortBuzz.mp3?v=1746032493487');
        audio.play();
    }
    all_buzzed = true;
});

socket.on("player-answer", (player, answer) => {
    const buzzedDiv = document.getElementById("players-buzzed");
    buzzedDiv.innerHTML += `<p>${player}</p>`;
    all_buzzed = true;
});

document.getElementById("buzzer").addEventListener("click", () => {
    if( !buzzed ) {
        buzzed = true;
        console.log( "buzzed : ", buzzed );
        socket.emit("buzz", playerName);
        console.log("Buzz envoyé !");
        document.getElementById( "no-buzzed" ).style.display = "none";
        document.getElementById( "buzzed" ).style.display = "block";
    }
});

document.getElementById( "answer-submit" ).addEventListener("click", () => {
    answer = document.getElementById( "answer-input" ).value;
    if( answer.trim() === "" ) {
        if( !buzzed ) {
            buzzed = true;
            alert( "Veuillez entrer une réponse valide." );
            return;
        }
    }
    socket.emit( "answer", answer )
});

socket.on("reset-buzz-state", () => {
    type = "buzz";
    document.getElementById("players-buzzed").innerText = "";
    document.getElementById("buzz-answer").style.display = "block";
    document.getElementById("type-answer").style.display = "none";
    document.getElementById( "no-buzzed" ).style.display = "block";
    document.getElementById( "buzzed" ).style.display = "none";
    buzzed = false; // Réinitialiser l'état local
    console.log( "buzzed : ", buzzed );
    console.log("Réinitialisation des buzz reçue !");
    all_buzzed = false;
});


socket.on("reset-answer-state", () => {
    type = "answer";
    document.getElementById("players-buzzed").innerText = "";
    document.getElementById("buzz-answer").style.display = "none";
    document.getElementById("type-answer").style.display = "block";
    document.getElementById( "answer-input" ).value = "";
    buzzed = false; // Réinitialiser l'état local
    console.log( "buzzed : ", buzzed );
    console.log("Réinitialisation des buzz reçue !");
    all_buzzed = false;
});


socket.on( "name-used", () => {
    alert( "nom déjà utilisé, veuillez en trouver un autre" );
    location.reload();
} );

socket.on( "delete-room", () => {
    location.reload();
} );


document.addEventListener('keydown', function(event) {
    console.log( event.keyCode );
    console.log( type );
    console.log( buzzed );
    if( event.keyCode == 32 ) {
        if( type == "buzz" ) {
            if( !buzzed ) {
                buzzed = true;
                console.log( "buzzed : ", buzzed );
                socket.emit("buzz", playerName);
                console.log("Buzz envoyé !");
                document.getElementById( "no-buzzed" ).style.display = "none";
                document.getElementById( "buzzed" ).style.display = "block";
            }
        }
    }
});