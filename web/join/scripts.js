const socket = io("http://localhost:57542");

let buzzed = false;
playerName = "";

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
            playersDiv.innerHTML += "\n"+players[i];
        }
    }
});

socket.on("player-buzzed", (player) => {
    const buzzedDiv = document.getElementById("players-buzzed");
    buzzedDiv.innerHTML += `<p>${player}</p>`;
});

document.getElementById("buzzer").addEventListener("click", () => {
    if( !buzzed ) {
        buzzed = true;
        socket.emit("buzz", playerName);
        console.log("Buzz envoyé !");
    }
});

socket.on("reset-buzz-state", () => {
    const buzzedDiv = document.getElementById("players-buzzed");
    buzzedDiv.innerHTML = ""; // Réinitialiser la liste des joueurs ayant buzzé
    buzzed = false; // Réinitialiser l'état local
    console.log("Réinitialisation des buzz reçue !");
});