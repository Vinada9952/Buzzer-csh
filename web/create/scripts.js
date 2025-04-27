const socket = io("http://localhost:57542");

// Afficher l'adresse IP comme code de salle
fetch("http://localhost:57542/get-ip")
    .then(response => response.text())
    .then(ip => {
        document.getElementById("room-code").innerText = `Code de salle : ${ip}`;
    });

// Gérer les événements du serveur
socket.on("update-players", (players) => {
    const playersDiv = document.getElementById("players");
    playersDiv.innerHTML = players.map(player => `<p>${player}</p>`).join("");
});

socket.on("player-buzzed", (player) => {
    const buzzedDiv = document.getElementById("players-buzzed");
    buzzedDiv.innerHTML += `<p>${player} a buzzé !</p>`;
});

// Boutons pour réinitialiser les états
document.getElementById("buzz-answer").addEventListener("click", () => {
    socket.emit("reset-buzz");
});

document.getElementById("type-answer").addEventListener("click", () => {
    socket.emit("reset-answer");
});