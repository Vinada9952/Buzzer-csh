const { Server } = require("socket.io");
const http = require("http");
const server = http.createServer();
const express = require('express');
const path = require('path');
const app = require('app');

app.use(express.static(path.join(__dirname, 'web')));

port = 3000;

app.listen( port, () => {



    console.log( "\n\n\n\n\n\n\n\n\n\n\n\n" );


    // Configurer Socket.IO pour utiliser le serveur HTTP
    const io = new Server(server, {
        cors: {
            origin: "*", // Autoriser toutes les origines
            methods: ["GET", "POST"], // Autoriser les méthodes HTTP spécifiques
        },
    });

    const rooms = {}; // Stocker les salles et leurs joueurs
    const playerNames = {}; // Associer les sockets aux noms des joueurs

    roomCode = ""; // Utiliser l'adresse IP comme code de salle
    rooms[roomCode] = []; // Initialiser la salle

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
            
                // Envoyer la liste des joueurs à tous les clients de la salle
                const players = rooms[roomCode].map(id => playerNames[id]);
                io.to(roomCode).emit("update-players", players);
            }
        });
        
        

        socket.on("create-room", ( code, playerName ) => {
            console.log( "room-code : ", roomCode );
            console.log( "code : ", code );

            console.log(`Requête de création de salle : ${roomCode} avec le nom : ${playerName}`);

            console.log( "rooms[code] : ", rooms[code] );

            if( rooms[code] != undefined ) {
                socket.emit( "room-used" );
                console.log( "room used" );
            }
            else {
                roomCode = code;
                rooms[roomCode] = []; // Initialiser la salle

                rooms[roomCode].push(socket.id);
                playerNames[socket.id] = playerName; // Associer le nom au socket
                socket.join(roomCode); // Joindre le socket à la salle
                console.log(`${playerName} a créé la salle : ${roomCode}`);
            
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



});