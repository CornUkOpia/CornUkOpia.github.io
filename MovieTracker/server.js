const express = require('express')
const http_request = require('request')
const PORT = 3000
let api_key = '8ca389d6'

const app = express()

// EXPRESS MIDDLEWARE
app.use(express.static(__dirname + '/public'))

//ROUTING
app.get('/movieTracker', (req,res) => {
	res.sendFile(__dirname + '/Display/main.html')
})
app.get('/mainMenu', (req,res) => {
	res.sendFile(__dirname + '/Display/main.html')
})
app.get('/', (req,res) => {
	res.sendFile(__dirname + '/Display/main.html')
})
app.get('/findMovie', (req,res) => {
	let filmTitle = req.query.t
	let filmYear = req.query.y
	let url = ''
	/* 	checks to see if the value that was put into the film title box contains
		any '<' or '>' symbols as having both present in one string might be 
		indicative of HTML or <script> injection. Replaces the harmful value put 
		into the text box with a harmless one. */ 
	if(filmTitle.includes('<') && filmTitle.includes('>')){
		filmTitle = "Hackers"
	}
	if(typeof filmYear !== "undefined"){
		if(filmYear.includes('<') && filmYear.includes('>')){
			filmYear = ''
			filmTitle = "Hackers"
		}
	}
	if(filmTitle === ''){
		return res.sendFile(__dirname + '/Display/main.html')
	}
	else{
		filmTitle = filmTitle.replace("#", "%23")
		if(filmYear === ''){
			url = `http://www.omdbapi.com/?t=${filmTitle}&apikey=${api_key}`
			console.log( url )
		}
		else{
			url = `http://www.omdbapi.com/?t=${filmTitle}&y=${filmYear}&apikey=${api_key}`
			console.log( url )
		}
	}
	http_request.get(url, (err, response, data) => {
		console.log( data )
		try
		{
			ret = res.contentType('application/json').json(JSON.parse(data))
		}
		catch (error)
		{
			console.log( "Error while handling response from " + url + ": " + error )
			return res.contentType("application/json").json( { error:true } )
		}
		return ret
	})
})

app.listen(PORT, err => {
	if(err){
		console.log("ERROR: " + err)
	}
	else{
		console.log("To start at the main menu")
		console.log(`http://localhost:${PORT}/`)
		console.log(`http://localhost:${PORT}/mainMenu`)
		console.log("To search for a film by its title through the URL")
		console.log(`http://localhost:${PORT}/?t=Alien`)
		console.log(`http://localhost:${PORT}/?t=Star+Trek`)
		console.log("To search for a film by its title and year through the URL")
		console.log(`http://localhost:${PORT}/?t=The+Thing&y=1982`)
		console.log(`http://localhost:${PORT}/?t=The+Thing&y=2011`)
	}
})
