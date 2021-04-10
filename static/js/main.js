 function _api_get (url, callback) {
        fetch(url, {
            method: 'GET',
            credentials: 'same-origin'
        })
        .then(response => response.json()) // parse the response as JSON
        .then(json_response => callback(json_response));  // Call the `callback` with the returned object

}

function getShows (callback) {
        // the boards are retrieved and then the callback function is called with the boards
        // Here we use an arrow function to keep the value of 'this' on dataHandler.
        //    if we would use function(){...} here, the value of 'this' would change.
        this._api_get('/get-shows', (response) => {
            this._data = response;
            callback(response);
        });}


function loadShows () {
    // retrieves boards and makes showBoards called
    getShows(function (shows) {
        showShows(shows);
    });
}

function showShows (shows) {
    // shows boards appending them to #boards div
    // it adds necessary event listeners also
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
