const socket = io("http://localhost:57542");

document.getElementById("room-code-submit").addEventListener("click", startGame);

function startGame() {
    const roomCode = document.getElementById("room-code-input").value;
    const playerName = document.getElementById("player-name-input").value;

    if (roomCode.trim() === "" || playerName.trim() === "") {
        alert("Veuillez entrer un code de salle et un nom valide.");
        return;
    }

    // Envoyer le code de la salle et le nom du joueur au serveur
    socket.emit("join-room", { roomCode, playerName });

    console.log("game start");
    document.getElementById("in-game").style.display = "block";
    document.getElementById("room-code").style.display = "none";
}

// Gérer les événements du serveur
socket.on("update-players", (players) => {
    const playersDiv = document.getElementById("players");
    playersDiv.innerHTML = players.map(player => `<p>${player}</p>`).join("");
});

socket.on("player-buzzed", (player) => {
    const buzzedDiv = document.getElementById("players-buzzed");
    buzzedDiv.innerHTML += `<p>${player}</p>`;
});

document.getElementById("buzzer").addEventListener("click", () => {
    socket.emit("buzz");
});