// The code that sets up the cookies for each of the lists if none are present.
if ( document.cookie.indexOf( "favouriteArr" ) < 0 )
{
	console.log("Favorites not present, recreating" )
	var favourite = []
	Cookies.set('favouriteArr', JSON.stringify(favourite), {expires: 7, path: ''})
}
if ( document.cookie.indexOf( "watchedArr" ) < 0 )
{
	console.log("Watched not present, recreating" )
	var watched = []
	Cookies.set('watchedArr', JSON.stringify(watched), {expires: 7, path: ''})
}
if ( document.cookie.indexOf( "watchlistArr" ) < 0 )
{
	console.log("Watchlist not present, recreating" )
	var watchlist = []
	Cookies.set('watchlistArr', JSON.stringify(watchlist), {expires: 7, path: ''})
}


let title = ''
function getFilm(){
	let infoTitles = ["Actors","Plot","Released","Genre","Director","Runtime","Rated","Ratings"]
	// Accessing of all the necessary elements that need to be accessed for this function to work
	let filmTitle = document.getElementById('film').value
	let filmYear = document.getElementById('filmYear').value
	if(filmTitle === ''){
		console.log("Enter film title. ")
	}
	let filmDiv = document.getElementById('filmDiv')
	// Clearing everything that needs to be cleared prior to the creation of the filmDiv content.
	document.getElementById('film').value = ''
	document.getElementById('filmYear').value = ''
	filmDiv.innerHTML = ''
	
	let xhr = new XMLHttpRequest()
	xhr.onreadystatechange = () => {
        if (xhr.readyState == 4 && xhr.status == 200) {
            let response = JSON.parse(xhr.responseText)
			// Turning the response.Ratings array into a string that is more usable.
			let ratingString = ''
			for(var i = 0; i < response.Ratings.length; i++){
				ratingString = ratingString + response.Ratings[i].Source + ': ' + response.Ratings[i].Value + '<br/>'
			}
			filmTitle = response.Title
			title = response.Title + "~" + response.Year
			// Filling the film div with the response content of the searched film
 			filmDiv.innerHTML = filmDiv.innerHTML + `
			<h1> ${response.Title} (${response.Year}) </h1>
			<img src = ${response.Poster} width='300' height ='450'>
			<table id="infoTable" style="border-collapse:collapse">
			<div class="tab">
			<button class="tabs" onclick="watchedFunction()" style="margin-bottom: 20px;">Add to Watched</button>
			<button class="tabs" onclick="watchlistFunction()" style="margin-bottom: 20px;">Add to Watchlist</button>
			<button class="tabs" id="favouriteButton" onclick="favouriteFunction()" style="margin-bottom: 20px;">Favourite</button>
			</div>`
			// Building of and filling of the table that contains the film info.
			let tableID = document.getElementById('infoTable')
			for(var i = 0; i < infoTitles.length; i++){
				let row = tableID.insertRow(i)
				for(var j = 0; j < 2; j++){
					let cell = row.insertCell(j)
					let x = tableID.rows[i].cells
					x[j].style.border = "thin solid black"
					if(j===0){
						x[j].innerHTML = infoTitles[i]
					}
					else{
						x[j].width = 500
					}
				}	
			}
			tableID.rows[0].cells[1].innerHTML = `${response.Actors}`
			tableID.rows[1].cells[1].innerHTML = `${response.Plot}`
			tableID.rows[2].cells[1].innerHTML = `${response.Released}`
			tableID.rows[3].cells[1].innerHTML = `${response.Genre}`
			tableID.rows[4].cells[1].innerHTML = `${response.Director}`
			tableID.rows[5].cells[1].innerHTML = `${response.Runtime}`
			tableID.rows[6].cells[1].innerHTML = `${response.Rated}`
			tableID.rows[7].cells[1].innerHTML = `${ratingString}`
        }
    }
	// Encoding the film title so spaces and certain characters don't affect how it works
	filmTitle = encodeURIComponent(filmTitle)
	/* 	Checking if there is specific year of the film that is being searched for as 
		this is important when dealing with films that have had remakes with the same 
		name. 
	*/
	if(filmYear===''){
		xhr.open('GET', `/findMovie?t=${filmTitle}`)
	}
	else{
		xhr.open('GET', `/findMovie?t=${filmTitle}&y=${filmYear}`)
	}
    xhr.send()
}

/* 	The function that creates the favourites table and adds it to the filmDiv along
	with all of its content. 
*/
function favouritesList(){
	filmDiv.innerHTML = ''
	document.getElementById('film').value = ''
	filmDiv.innerHTML = filmDiv.innerHTML + `
	<h2 align="center"> FAVOURITE: </h2>
	<table id="favouriteTable" align="center" width='300' style="border-collapse:collapse">`
	var table = document.getElementById('favouriteTable')
	var favouriteArray = JSON.parse(Cookies.get('favouriteArr'))
	/* 	Creating the favourites table in which all of the films in the favourites
		list will be contained along with an event listener that allows the user to
		access the pages of the film they choose by clicking within the bounds of its
		cell.
	*/
	for(let i = 0; i < favouriteArray.length; i++){
		var row = table.insertRow(i)
		var cell = row.insertCell(0)
		cell.style.border = "thin solid black"
		let filmInfoArr = separateYearFromTitle(favouriteArray[i])
		cell.innerHTML = filmInfoArr[0] + " (" + filmInfoArr[1] + ")"
		/* 	Event listener for each row which allows the user to click on the
			name of a film in the favourite list page and be taken to the page
			of that film.
		*/		
		row.addEventListener("click", () => {
			document.getElementById('film').value = filmInfoArr[0]
			document.getElementById('filmYear').value = filmInfoArr[1]
			getFilm()
		})
	}
}
// A function that separates the year from the title
function separateYearFromTitle(input){
	var titleYear = input.split('~')
	return titleYear
}
/* 	The function that adds/removes elements from the favourites list depending on
	if the film is already on the list or not
*/
function favouriteFunction(){
	var favouriteArray = JSON.parse(Cookies.get('favouriteArr'))
	var index = favouriteArray.indexOf(title)
	if(index > -1){favouriteArray.splice(index,1)}
	else{favouriteArray.push(title)}
	Cookies.set('favouriteArr', JSON.stringify(favouriteArray))
}

/* 	The function that creates the watchlist table and adds it to the filmDiv along
	with all of its content. 
*/
function watchedList(){
	filmDiv.innerHTML = ''
	document.getElementById('film').value = ''
	filmDiv.innerHTML = filmDiv.innerHTML + `
	<h2 align="center"> WATCHED: </h2>
	<table id="watchedTable" align="center" width='300' style="border-collapse:collapse">`
	var table = document.getElementById('watchedTable')
	var watchedArray = JSON.parse(Cookies.get('watchedArr'))
	/* 	Creating the watched table in which all of the films in the watched
		list will be contained along with an event listener that allows the user to
		access the pages of the film they choose by clicking within the bounds of its
		cell.
	*/
	for(let i = 0; i < watchedArray.length; i++){
		var row = table.insertRow(i)
		var cell = row.insertCell(0)
		cell.style.border = "thin solid black"
		let filmInfoArr = separateYearFromTitle(watchedArray[i])
		console.log(filmInfoArr)
		cell.innerHTML = filmInfoArr[0] + " (" + filmInfoArr[1] + ")"	
		/* 	Event listener for each row which allows the user to click on the
			name of a film in the watched list page and be taken to the page
			of that film.
		*/
		row.addEventListener("click", () => {
			document.getElementById('film').value = filmInfoArr[0]
			document.getElementById('filmYear').value = filmInfoArr[1]
			getFilm()
		})
	}
	
}
/* 	The function that adds/removes elements from the watched list depending on
	if the film is already on the list or not
*/
function watchedFunction(){
	var watchedArray = JSON.parse(Cookies.get('watchedArr'))
	var index = watchedArray.indexOf(title)
	if(index > -1){watchedArray.splice(index,1)}
	else{watchedArray.push(title)}
	Cookies.set('watchedArr', JSON.stringify(watchedArray))
}

/* 	The function that creates the watchlist table and adds it to the filmDiv along
	with all of its content. 
*/
function watchlistList(){
	filmDiv.innerHTML = ''
	document.getElementById('film').value = ''
	filmDiv.innerHTML = filmDiv.innerHTML + `
	<h2 align="center"> WATCHLIST: </h2>
	<table id="watchlistTable" align="center" width='300' style="border-collapse:collapse">`
	var table = document.getElementById('watchlistTable')
	var watchlistArray = JSON.parse(Cookies.get('watchlistArr'))
	/* 	Creating the watchlist table in which all of the films in the watchlist
		list will be contained along with an event listener that allows the user to
		access the pages of the film they choose by clicking within the bounds of its
		cell.
	*/
	for(let i = 0; i < watchlistArray.length; i++){
		var row = table.insertRow(i)
		var cell = row.insertCell(0)
		cell.style.border = "thin solid black"
		let filmInfoArr = separateYearFromTitle(watchlistArray[i])
		cell.innerHTML = filmInfoArr[0] + " (" + filmInfoArr[1] + ")"	
		/* 	Event listener for each row which allows the user to click on the
			name of a film in the watchlist list page and be taken to the page
			of that film.
		*/
		row.addEventListener("click", () => {
			document.getElementById('film').value = filmInfoArr[0]
			document.getElementById('filmYear').value = filmInfoArr[1]
			getFilm()
		})
	}
}
/* 	The function that adds/removes elements from the watchlist depending on
	if the film is already on the list or not
*/
function watchlistFunction(){
	var watchlistArray = JSON.parse(Cookies.get('watchlistArr'))
	var index = watchlistArray.indexOf(title)
	if(index > -1){watchlistArray.splice(index,1)}
	else{watchlistArray.push(title)}
	Cookies.set('watchlistArr', JSON.stringify(watchlistArray))
}
/* 	function that gets the URL upon the loading of the page and 
	calls the appropriate function based on the content of the url.
*/
function getURL() {
    let url = new URLSearchParams(window.location.search)
	if(url.has('t')){ 
		document.getElementById('film').value = decodeURIComponent(url.get('t'))
		document.getElementById('filmYear').value = decodeURIComponent(url.get('y'))
		getFilm()
	}
	else{
		getMainMenu()
	}
}
// function that takes the user to the main menu
function getMainMenu(){
	let xhr = new XMLHttpRequest()
	// clears what was originally in the filmDiv when the request was made
	filmDiv.innerHTML = ''
    xhr.open('GET', `/mainMenu`)
    xhr.send()
}

const ENTER=13
//Event Listener for the Film Title text box
document.getElementById("film").addEventListener("keyup", function(event) {
    event.preventDefault();
	//gets the value of the film title text box
	let filmTitle = document.getElementById('film').value
	/* 	checks if the keyCode pressed is equivalent to the value of ENTER and
		then gets the submit button element and utilises its click property 
	*/
    if (event.keyCode === ENTER) {
        document.getElementById("submit").click();
    }
});
//Event Listener for the Film Year text box
document.getElementById("filmYear").addEventListener("keyup", function(event) {
    event.preventDefault();
	//gets the value of the film year text box
	let filmYear = document.getElementById('filmYear').value
	/* 	checks if the keyCode pressed is equivalent to the value of ENTER and
		then gets the submit button element and utilises its click property 
	*/
    if (event.keyCode === ENTER) {
        document.getElementById("submit").click();
    }
});
