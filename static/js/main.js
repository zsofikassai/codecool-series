const app = {
    getData: function(){
        fetch('/get-shows')
            .then(response => response.json())
            .then(data => this.showData(data))

    },

    showData: function (data){
        let container = document.querySelector('#shows');

        let rows ='';
        let header = '<thead> <tr> <th> Name </th>  <th> Char count </th> <th> Char names </th> <th> Rating</th> </tr></thead>';
        for (let d of data){
            console.log(d);
            rows += `<tr> <td class="title"> ${d['name']} </td> <td> ${d['chars']} </td><td> ${d['string_agg']} </td><td id="rating"> ${d['rating']} </td>`
        }
        container.innerHTML= header + rows;
        this.linkToGoogle();
    },

    createAnimations: function(){
        let titles = document.querySelectorAll('.title');
        let section = document.querySelector('section');
        for (let title of titles){
            title.addEventListener('click', function(){
            let myModal = document.createElement('div');
            myModal.setAttribute('id', 'myModal');
            myModal.classList.add('modal');
            myModal.innerHTML = `<div class="modal-content"> 
                <span class="close">&times;</span> 
                <p><iframe width="420" height="315"
                src="https://www.youtube.com/embed/tgbNymZ7vqY">
                    </iframe></p> </div>`
            section.appendChild(myModal);
                myModal.style.display = "block";
                let closeBtn = document.getElementsByClassName("close")[0];
                closeBtn.addEventListener('click', function (){
                    myModal.style.display ="none";
                })
              })}
    },
    linkToGoogle: function(){
    let tableDatas  = document.querySelectorAll('.title');
    for(let tableData of tableDatas) {
        tableData.addEventListener("click", function (event) {
            let index = tableDatas.indexOf(tableData.innerText);
            console.log(index);
            let title = event.currentTarget
            if (confirm(`Do you want to Google ${title.innerText}`)) {
                window.open(`https://google.com/search?q=${title.innerText}`)
            } else {
                alert('You are a potato!')
            }

        })
    }
}


}

function init(){
    app.getData();

}
init();