
const express = require( "express" );
const path = require( "path" );
const app = express();
port = 3000;


app.use( express.static( "public" ) );

console.log( "hello world" );

app.listen( port, () => {
    console.log( "ello" )
} )