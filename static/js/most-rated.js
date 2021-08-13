 function _api_get (url, callback) {
        fetch(url, {
            method: 'GET',
            credentials: 'same-origin'
        })
        .then(response => response.json()) // parse the response as JSON
        .then(json_response => callback(json_response));  // Call the `callback` with the returned object

}

function getMostRated (callback) {
        this._api_get('/get-most-rated', (response) => {
            this._data = response;
            callback(response);
        });}


function loadMostRated(){
        getMostRated(function (most_rated) {
        showMostRated(most_rated);
    });
}



function showMostRated (most_rated) {

    const headers = ['Title', 'Year', 'Runtime (min)', 'Rating', 'Genres', 'Trailer', 'Homepage'];
    const keys = ['title', 'year', 'runtime', 'rating', 'genres', 'trailer', 'homepage'];
    let showsContainer = document.querySelector('.table');
    const paginationElement = document.getElementById('pagination');

    let current_page = 1;
    let displayed_rows = 15;


    function displayPagination(items, wrapper, displayed_rows, current_page) {
        let rows = '';

        for (let header of headers) {
            let key = keys[headers.indexOf(header)];
            rows += `<th id='clickable'>${header}</th>`;
        }
        wrapper.innerHTML = "";
        current_page--;

        let loop_start = displayed_rows * current_page;
        let paginatedShows = items.slice(loop_start, loop_start + displayed_rows);

        for (let show of paginatedShows) {
            let row = '';
            for (let key of keys) {
                if (key == 'title') {
                    row += `
                <td> <a href="/show/${show.id}"> ${show[key]} </a></td>
            `;
                } else if (show[key] != null) {
                    row += `
                <td> ${show[key]}</td>
            `;
                } else {
                    row += `
                <td> No Url</td>
            `;
                }

            }
            rows += `<tr>
                ${row}
               </tr>`;
        }
        wrapper.insertAdjacentHTML("beforeend", rows);
        setupSort(items);
    }

    function setupSort(items){
        let columnHeaders = document.querySelectorAll('#clickable');

        for (let i=0; i<columnHeaders.length; i++){
            columnHeaders[i].toggleAttribute('desc')
            columnHeaders[i].addEventListener('toggle',  columnHeaders[i] )
            columnHeaders[i].addEventListener('click', function(){
                const headers = ['Title', 'Year', 'Runtime (min)', 'Rating', 'Genres', 'Trailer', 'Homepage'];
                const keys = ['title', 'year', 'runtime', 'rating', 'genres', 'trailer', 'homepage'];
                let key = keys[headers.indexOf(columnHeaders[i].innerHTML)];
                if (this.hasAttribute('desc')) {
                    sortByColumn(items, key, 'desc') ;}
                else{
                    sortByColumn(items, key, 'asc');
                }
            })

        }
    }

    function sortByColumn(items, column, order){
        function compareValues(key, order) {
            return function innerSort(a, b) {
                if (!a.hasOwnProperty(key) || !b.hasOwnProperty(key)) {
                    // property doesn't exist on either object
                    return 0;
                }

                const varA = (typeof a[key] === 'string')
                    ? a[key].toUpperCase() : a[key];
                const varB = (typeof b[key] === 'string')
                    ? b[key].toUpperCase() : b[key];

                let comparison = 0;
                if (varA > varB) {
                    comparison = 1;
                } else if (varA < varB) {
                    comparison = -1;
                }
                return (
                    (order === 'desc') ? (comparison * -1) : comparison
                );
            };
        }
        displayPagination(items.sort(compareValues(column, order)), showsContainer, displayed_rows, current_page);
    }



    function setupPagination(items, wrapper, displayed_rows) {
        wrapper.innerHTML = "";
        let page_count = Math.ceil(items.length / displayed_rows);
        let prevButton = document.createElement('button');
        prevButton.innerText = '<<';
        wrapper.appendChild(prevButton);
        prevButton.addEventListener('click', function () {
            if (current_page != 1) {
                current_page--;
            }
            displayPagination(most_rated, showsContainer, displayed_rows, current_page);
        })

        for (let i = 1; i < page_count + 1; i++) {
            let btn = paginationButton(most_rated, i);
            wrapper.appendChild(btn);
        }
        let nextButton = document.createElement('button');
        nextButton.innerText = '>>';
        nextButton.addEventListener('click', function () {
            if (current_page != page_count) {
                current_page++;
            }

            displayPagination(most_rated, showsContainer, displayed_rows, current_page);
        })
        wrapper.appendChild(nextButton);
    }

    function paginationButton(most_rated, page) {
        let button = document.createElement('button');
        button.innerText = page;
        button.addEventListener('click', function () {
            current_page = page;
            displayPagination(most_rated, showsContainer, displayed_rows, current_page);
        })
        if (current_page == page) {
            button.classList.add('active')
        }
        ;
        return button;
    }

    displayPagination(most_rated, showsContainer, displayed_rows, current_page);
    setupPagination(most_rated, paginationElement, displayed_rows);
}

 loadMostRated();
