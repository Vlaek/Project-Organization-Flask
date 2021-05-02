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

    function getRandomInRange(min, max) {
      return Math.floor(Math.random() * (max - min + 1)) + min;
    }

    function formatDate(year, month, day) {

      if (day < 10) day = '0' + day;

      if (month < 10) month = '0' + month;

      return year + '-' + month + '-' + day;
    }

    random.onclick = function(){
        $( document ).ready(function(){
            var url = "https://api.randomdatatools.ru/?count=10&params=LastName,FirstName";
            $.getJSON( url, {
                format: "json"
            })
            .done(function( data ) {
                document.getElementById('forename').value = data[1]["FirstName"];
                document.getElementById('surname').value = data[1]["LastName"];
                document.getElementById('DOB').value = formatDate(getRandomInRange(1950, 2002), getRandomInRange(1, 12), getRandomInRange(1,28));
                let o1 = getRandomInRange(0, 4)
                if (o1 == 0)
                {
                    document.querySelector('#speciality').value = "Инженер";
                }
                if (o1 == 1)
                {
                    document.querySelector('#speciality').value = "Техник";
                }
                if (o1 == 2)
                {
                    document.querySelector('#speciality').value = "Конструктор";
                }
                if (o1 == 3)
                {
                    document.querySelector('#speciality').value = "Лаборант";
                }
                if (o1 == 4)
                {
                    document.querySelector('#speciality').value = "Обслуживающий персонал";
                }

                OnChange();
            });
        });
    };
}

function OnChange()
{
    if (document.getElementById("forename").value == '' || document.getElementById("surname").value == ''
        || document.getElementById("DOB").value == '')
    {
        document.getElementById("btn1").setAttribute("disabled", "disabled");
    }
    else
    {
        document.getElementById("btn1").removeAttribute("disabled");
    }
}


function OnChange2()
{
    if (document.getElementById("Forename2").value == '' || document.getElementById("Surname2").value == ''
        || document.getElementById("DOB2").value == '')
    {
        document.getElementById("btn2").setAttribute("disabled", "disabled");
    }
    else
    {
        document.getElementById("btn2").removeAttribute("disabled");
    }
}

OnChange();
