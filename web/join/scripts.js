const socket = io("http://localhost:57542");

buzzed = false;
console.log( "buzzed : ", buzzed );
playerName = "";
all_buzzed = false;

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
    const playersDiv = document.getElementById("players");
    for( let i = 0; i < players.length; i++ ) {
        if( players[i] != "host")
        {
            playersDiv.innerText += players[i] + "\n";
        }
    }
});

socket.on("player-buzzed", (player) => {
    const buzzedDiv = document.getElementById("players-buzzed");
    buzzedDiv.innerHTML += `<p>${player}</p>`;
    console.log( "player : ", player );
    if( !all_buzzed )
    {
        const audio = new Audio('../../assets/shortBuzz.mp3');
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
    }
});

document.getElementById( "answer-submit" ).addEventListener("click", () => {
    answer = document.getElementById( "answer-input" ).value;
    if( answer.trim() === "" ) {
        alert( "Veuillez entrer une réponse valide." );
        return;
    }
    socket.emit( "answer", answer )
});

socket.on("reset-buzz-state", () => {
    document.getElementById("players-buzzed").innerText = "";
    document.getElementById("buzz-answer").style.display = "block";
    document.getElementById("type-answer").style.display = "none";
    buzzed = false; // Réinitialiser l'état local
    console.log( "buzzed : ", buzzed );
    console.log("Réinitialisation des buzz reçue !");
    all_buzzed = false;
});


socket.on("reset-answer-state", () => {
    document.getElementById("players-buzzed").innerText = "";
    document.getElementById("buzz-answer").style.display = "none";
    document.getElementById("type-answer").style.display = "block";
    document.getElementById( "answer-input" ).value = "";
    buzzed = false; // Réinitialiser l'état local
    console.log( "buzzed : ", buzzed );
    console.log("Réinitialisation des buzz reçue !");
    all_buzzed = false;
});
