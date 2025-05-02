console.log( 1 );
const { Server } = require("socket.io");
console.log( 2 );
const http = require("http");
console.log( 3 );
const express = require('express');
console.log( 4 );
const path = require('path');

console.log( "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n" )

const app = express();
const server = http.createServer(app);

app.use(express.static(path.join(__dirname, 'web')));

const port = process.env.PORT || 3000; // Utiliser un port dynamique pour Glitch
const io = new Server(server, {
    cors: {
        origin: "*",
        methods: ["GET", "POST"],
    },
});

const rooms = {}; // Stocker les salles et leurs joueurs
const playerNames = {}; // Associer les sockets aux noms des joueurs

io.on("connection", (socket) => {
    console.log("Un client s'est connecté");

        socket.on("join-room", ( roomCode, playerName ) => {
            console.log( "room-code : ", roomCode );

            console.log(`Requête de connexion à la salle : ${roomCode} avec le nom : ${playerName}`);

        if (!rooms[roomCode]) {
            socket.emit("error", "Salle introuvable.");
            return;
        }

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

            const players = rooms[roomCode].map(id => playerNames[id]);
            io.to(roomCode).emit("update-players", players);
        }
    });

    socket.on("create-room", (code, playerName) => {
        if (rooms[code]) {
            socket.emit("room-used");
        } else {
            rooms[code] = [socket.id];
            playerNames[socket.id] = playerName;
            socket.join(code);

            const players = rooms[code].map(id => playerNames[id]);
            io.to(code).emit("update-players", players);
        }
    });

    socket.on("buzz", () => {
        const roomCode = Object.keys(rooms).find(code => rooms[code].includes(socket.id));
        if (roomCode) {
            const playerName = playerNames[socket.id];
            io.to(roomCode).emit("player-buzzed", `${playerName} a buzzé !`);
        }
    });

    socket.on("reset-buzz", () => {
        const roomCode = Object.keys(rooms).find(code => rooms[code].includes(socket.id));
        if (roomCode) {
            io.to(roomCode).emit("reset-buzz-state");
        }
    });

    socket.on("disconnect", () => {
        for (const roomCode in rooms) {
            rooms[roomCode] = rooms[roomCode].filter(id => id !== socket.id);
                player = playerNames[socket.id];
            delete playerNames[socket.id];

            if (player === "host") {
                io.to(roomCode).emit("delete-room");
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

server.listen(port, () => {
    console.log(`Serveur en cours d'exécution sur le port ${port}`);
});