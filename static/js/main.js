function _api_get (url, callback) {
        fetch(url, {
            method: 'GET',
            credentials: 'same-origin'
        })
        .then(response => response.json()) // parse the response as JSON
        .then(json_response => callback(json_response));  // Call the `callback` with the returned object

}

//Get shows with Fetch API get request
function getShows (callback) {
        this._api_get('/get-shows', (response) => {
            this._data = response;
            callback(response);
        });}


function loadShows () {
    getShows(function (shows) {
        showShows(shows);
    });
}

//Display show data
function showShows (shows) {
    let showsContainer = document.querySelector('#shows');
    let showList = '';
    for (let show of shows) {

        showList += `
                <li class="board-name">${show.title}</li>
            `;
    }

    const outerHtml = `
            <ul class="board-container">
                ${showList}
            </ul>
        `;
    showsContainer.insertAdjacentHTML("beforeend", outerHtml);
}

loadShows();

