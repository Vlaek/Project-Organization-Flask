let modal1 = document.getElementById('id01');
let modal2 = document.getElementById('id02');

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

document.getElementById("StartDate").onchange = function () {
    let input = document.getElementById("EndDate");
    input.min = this.value;
    first_date = this.value;

    if (first_date > input.value) {
         input.value = '';
    }

    OnChange();
}

document.getElementById("StartDate2").onchange = function () {
    let input = document.getElementById("EndDate2");
    input.min = this.value;
    first_date = this.value;

    if (first_date > input.value) {
         input.value = '';
    }

    OnChange2();
}

function OnChange() {
    if (document.getElementById("Name").value == '' || document.getElementById("Cost").value == ''
        || document.getElementById("StartDate").value == '' || document.getElementById("EndDate").value == ''
        || document.getElementById("Leader").value == '')
    {
        document.getElementById("btn1").setAttribute("disabled", "disabled");
    } else {
        document.getElementById("btn1").removeAttribute("disabled");
    }
}

function OnChange2() {
    if (document.getElementById("Name2").value == '' || document.getElementById("Cost2").value == ''
        || document.getElementById("StartDate2").value == '' || document.getElementById("EndDate2").value == ''
        || document.getElementById("Leader2").value == '')
    {
        document.getElementById("btn2").setAttribute("disabled", "disabled");
    } else {
        document.getElementById("btn2").removeAttribute("disabled");
    }
}

OnChange();