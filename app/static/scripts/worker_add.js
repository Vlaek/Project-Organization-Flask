

//
//function OnChange() {
//    if (forename.value == '' || surname.value == '' || dob.value == '') {
//        document.getElementById("btn1").setAttribute("disabled", "disabled");
//        console.log("da")
//    } else {
//        document.getElementById("btn1").removeAttribute("disabled");
//    }
//}
//
//OnChange();
//

const forename = document.getElementById("forename");
const surname = document.getElementById("surname");
const dob = document.getElementById("DOB");
const speciality = document.getElementById("speciality");

const btnAdd = document.getElementById('add');
const modal1 = document.getElementById('modal1');
const btnClose1 = document.getElementById('btn-close1');
const randomBtn = document.getElementById('random');

btnAdd.addEventListener('click', () => {
    modal1.style.display = 'flex';
})

btnClose1.addEventListener('click', () => {
    modal1.style.display = 'none';
})

window.addEventListener('click', (e) => {
    const target = e.target;

    if (!target.closest('.modal__content') && !target.closest('.header__btn')) {
        modal1.style.display = 'none';
    }
})

randomBtn.addEventListener('click', () => {
    const specialities = ['Инженер', 'Техник', 'Конструктор', 'Лаборант', 'Обслуживающий персонал'];
    $(document).ready(() => {
        let url = 'https://api.randomdatatools.ru/?count=10&params=LastName,FirstName';
        $.getJSON(url, {
            format: 'json'
        })
        .done((data) => {
            forename.value = data[1]['FirstName'];
            surname.value = data[1]["LastName"];
            dob.value = formatDate(getRandomInRange(1950, 2002), getRandomInRange(1, 12), getRandomInRange(1, 28));
            speciality.value = specialities[getRandomInRange(0, 4)];
        });
    });
});

function getRandomInRange(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

function formatDate(year, month, day) {
  if (day < 10) day = '0' + day;
  if (month < 10) month = '0' + month;
  return year + '-' + month + '-' + day;
}