const socket = io("http://localhost:57542");


// Afficher l'adresse IP comme code de salle
tmp = fetch("http://localhost:57542/get-code")
    .then(response => response.text())
    .then(ip => {
        document.getElementById("room-code").innerText = `Code de salle : ${ip}`;
        console.log( "room code : ", ip );
        return ip;
    });


const n = "host";

    
console.log( "c : ", c );
console.log( "n :  ", n );
socket.emit("join-room", c, n );


socket.on( "search-host", () => {
    console.log( "Hôte connecté" );
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