var click = document.getElementById('submit');
click.addEventListener('click', addData);

var arr = new Array();

function addData(){
    DeleteData();
    getData();
    arr.push({
        spotify_username:document.getElementById('spotify_username').value,
        spotify_email:document.getElementById('spotify_email').value,
        spotify_password:document.getElementById('spotify_password').value,
        netflix_email:document.getElementById('netflix_email').value,
        netflix_password:document.getElementById('netflix_password').value,
    });

        localStorage.setItem("localData", JSON.stringify(arr));
}

function getData(){
    var str = localStorage.getItem("localData");
    if (str!= null)
        arr = JSON.parse(str);
}

function DeleteData(){
localStorage.clear();
}

$(document).ready(function(){
    var arr1 = new Array();
    arr1 = JSON.parse(localStorage.getItem("localData"));

    var tbl = document.getElementById('user-information');

    for(i = 0; i < arr1.length; i++){
        var r = tbl.insertRow();
        var cell1 = r.insertCell();
        var cell2 = r.insertCell();
        var cell3 = r.insertCell();
        var cell4 = r.insertCell();
        var cell5 = r.insertCell();

        cell1.innerHTML = arr1[i].spotify_username;
        cell2.innerHTML = arr1[i].spotify_email;
        cell3.innerHTML = arr1[i].spotify_password;
        cell4.innerHTML = arr1[i].netflix_email;
        cell5.innerHTML = arr1[i].netflix_password;

    }

});

