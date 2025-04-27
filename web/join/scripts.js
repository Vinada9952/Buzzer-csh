document.getElementById( "room-code-submit" ).addEventListener( "click", startGame )


function startGame() {
    console.log( "game start" )
    document.getElementById( "in-game" ).style.display = "block";
    document.getElementById( "room-code" ).style.display = "none";
}