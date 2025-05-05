const { Server } = require("socket.io");
const http = require("http");
const server = http.createServer();
const os = require('os');


function getLocalIPAddress() {
    const networkInterfaces = os.networkInterfaces();
    for (const interfaceName in networkInterfaces) {
        const addresses = networkInterfaces[interfaceName];
        for (const address of addresses) {
            if (address.family === 'IPv4' && !address.internal) {
                return address.address; // Retourne l'adresse IP locale
            }
        }
    }
    return 'Adresse IP non trouvée';
}


const io = new Server(server, {
    cors: {
        origin: "*", // Autoriser toutes les origines
        methods: ["GET", "POST"], // Autoriser les méthodes HTTP spécifiques
    },
});

const playerNames = {}; // Associer les sockets aux noms des joueurs
room = "a"

all_buzzed = false;


io.on("connection", (socket) => {
    console.log("Un client s'est connecté");

    socket.on("join-room", ( playerName ) => {

        console.log(`Requête de connexion à la salle avec le nom : ${playerName}`);

        console.log( "PlayerNames : ", playerNames );
        if( Object.values(playerNames).includes(playerName) )
        {
            socket.emit( "name-used" );
        }
        else
        {
            rooms[roomCode].push(socket.id);
            playerNames[socket.id] = playerName; // Associer le nom au socket
            socket.join(roomCode); // Joindre le socket à la salle
            console.log(`${playerName} a rejoint la salle : ${roomCode}`);
        
            // Envoyer la liste des joueurs à tous les clients de la salle
            const players = rooms[roomCode].map(id => playerNames[id]);
            io.to(roomCode).emit("update-players", players);
        }
    });
    

    socket.on("buzz", () => {
        const roomCode = Object.keys(rooms).find(code => rooms[code].includes(socket.id));
        if (roomCode) {
            const playerName = playerNames[socket.id];
            io.to(roomCode).emit("player-buzzed", `${playerName} a buzzé !`);
        }
    });
    
    socket.on( "answer", ( answer ) => {
        const roomCode = Object.keys(rooms).find(code => rooms[code].includes(socket.id));
        if (roomCode) {
            const playerName = playerNames[socket.id];
            io.to(roomCode).emit("player-answer",playerName, answer);
        }
    });

    socket.on("reset-buzz", () => {
        console.log("Réinitialisation des buzz !");
        const roomCode = Object.keys(rooms).find(code => rooms[code].includes(socket.id));
        console.log(`Room code: ${roomCode}`);
        if (roomCode) {
            io.to(roomCode).emit("reset-buzz-state"); // Événement spécifique pour réinitialiser
            console.log(`Événement reset-buzz-state émis à la salle : ${roomCode}`);
        }
    });

    socket.on("reset-answer", () => {
        console.log("Réinitialisation des buzz !");
        const roomCode = Object.keys(rooms).find(code => rooms[code].includes(socket.id));
        console.log(`Room code: ${roomCode}`);
        if (roomCode) {
            io.to(roomCode).emit("reset-answer-state"); // Événement spécifique pour réinitialiser
            console.log(`Événement reset-answer-state émis à la salle : ${roomCode}`);
        }
    });

    socket.on("disconnect", () => {
        console.log("Un client s'est déconnecté");
        for (const roomCode in rooms) {
            rooms[roomCode] = rooms[roomCode].filter(id => id !== socket.id);
            player = playerNames[socket.id];
            delete playerNames[socket.id];
            if( player == "host" )
            {
                io.to(roomCode).emit( "delete-room" );
                delete rooms[roomCode];
            }
            else
            {
                const players = rooms[roomCode].map(id => playerNames[id]);
                io.to(roomCode).emit("update-players", players);
            }
        }
    });
});

// Démarrer le serveur HTTP et Socket.IO
server.listen(57542, () => {
    console.log("Serveur en cours d'exécution sur le port 57542");
});


document.getElementById( "room-code" ).innerText += " "+c;

// Gérer les événements du serveur
socket.on("update-players", (players) => {
    console.log( "update-players", players );
    document.getElementById("players").innerText = "";
    const playersDiv = document.getElementById("players");
    for( let i = 0; i < players.length; i++ ) {
        if( players[i] != "host")
        {
            playersDiv.innerText += "\n" + players[i] + "\n";
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
    buzzedDiv.innerHTML += `<p>${player} a répondu : ${answer}</p>`;
    all_buzzed = true;
});

socket.on( "room-used", () => {
    location.reload();
});