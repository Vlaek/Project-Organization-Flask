var modal1 = document.getElementById('id01');
var modal2 = document.getElementById('id02');

window.onclick = function(event) {
    if (event.target == modal1) {
        modal1.style.display = "none";
    };

    if (event.target == modal2) {
        modal2.style.display = "none";
    };

    cancel.onclick = function() {
        modal1.style.display = "none";
    };

    cancel2.onclick = function() {
        modal2.style.display = "none";
    };

    kreuz.onclick = function() {
        modal1.style.display = "none";
    };

    kreuz2.onclick = function() {
        modal2.style.display = "none";
    };
}

function OnChange() {
    if (document.getElementById("Name").value == '' || document.getElementById("Client").value == '' || $('.require-one:checked').length < 1) {
        document.getElementById("btn1").setAttribute("disabled", "disabled");
    } else {
        document.getElementById("btn1").removeAttribute("disabled");
    }
}

function OnChange2() {
    if (document.getElementById("Name2").value == '' || document.getElementById("Client2").value == '') {
        document.getElementById("btn2").setAttribute("disabled", "disabled");
    } else {
        document.getElementById("btn2").removeAttribute("disabled");
    }
}

OnChange();