const socket = io("https://localhost:57542/");

all_buzzed = false;

c = "";
n = "host";
for( let i = 0; i < 4; i++ ) {
    c += Math.floor( Math.random() * 10 ).toString();
}
socket.emit( "create-room", c, n );

document.getElementById( "room-code" ).innerText += " "+c;

// Gérer les événements du serveur
socket.on("update-players", (players) => {
    console.log( "update-players", players );
    document.getElementById("players").innerText = "";
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
    if( !all_buzzed )
    {
        const audio = new Audio('https://cdn.glitch.global/fff151b3-947e-47f6-9965-3a1e4ae8d6ea/shortBuzz.mp3?v=1746032493487');
        audio.play();
    }
    all_buzzed = true;
});

// Boutons pour réinitialiser les états
document.getElementById("buzz-answer").addEventListener("click", () => {
    socket.emit("reset-buzz");
    document.getElementById( "players-buzzed" ).innerText = "";
    all_buzzed = false;
});

document.getElementById("type-answer").addEventListener("click", () => {
    socket.emit("reset-answer");
    document.getElementById( "players-buzzed" ).innerText = "";
    all_buzzed = false;
});


socket.on("player-answer", (player, answer) => {
    const buzzedDiv = document.getElementById("players-buzzed");
    buzzedDiv.innerHTML += `<p>${player} a répondu ${answer}</p>`;
    all_buzzed = true;
});

socket.on( "room-used", () => {
    location.reload();
});