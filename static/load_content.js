let loadMovies = async () => {
    const response = await fetch('http://localhost:8000/api/films-and-people')
    const filmsAndPeople = await response.json()

    let listElement = document.getElementById('film-list')

    for (let [film, people] of Object.entries(filmsAndPeople)) {
        let itemElement = document.createElement("li")
        let itemText = film + ':\t' + (people.length ? people : '-')
        itemElement.appendChild(document.createTextNode(itemText))
        listElement.appendChild(itemElement)
    }
}
loadMovies()
