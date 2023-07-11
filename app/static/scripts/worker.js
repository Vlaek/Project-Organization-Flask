const close = document.getElementsByClassName('close');
const openBtn = document.getElementsByClassName('btn-open');

const btnDelete = document.querySelector('.btnDelete');
const leadersArray = JSON.parse(btnDelete.getAttribute('data-leaders'));

leadersArray.forEach(id => {
    let btn = document.querySelector('.idBtnDelete-' + id);
    btn.classList.add('btnDisabled');
    btn.addEventListener('click', (e) => e.preventDefault())
})

Array.from(close, closeButton => {
    closeButton.addEventListener('click', e => {
        e.target.closest('.modal').style.display = 'none'
    });
});

Array.from(openBtn, openButton => {
    openButton.addEventListener('click', e => {
        const modalId = e.target.getAttribute('data-id');
        const modal = document.getElementById(modalId);
        modal.style.display = 'flex';

        const dataArray = modal.querySelectorAll('.modal__input');
        const idInput = dataArray[0];
        const forenameInput = dataArray[1];
        const surnameInput = dataArray[2];
        const dobInput = dataArray[3];
        const specialityInput = dataArray[4];
        const positionInput = dataArray[5];

        window.addEventListener('click', (e) => {
            const target = e.target;
            if (!target.closest('.modal__content') && !target.closest('.btn-open')) {
                document.getElementById(modalId).style.display = 'none';
            }
        });

        modal.addEventListener('change', () => {
            formValidation(forenameInput, surnameInput, dobInput, modal);
        });

        if (modalId === 'modalAdd') {
            const randomBtn = document.getElementById('random');
            randomBtn.addEventListener('click', () => {
                const specialities = ['Инженер', 'Техник', 'Конструктор', 'Лаборант', 'Обслуживающий персонал'];
                let url = 'https://api.randomdatatools.ru/?count=10&params=LastName,FirstName';
                fetch(url)
                .then(resp => resp.json())
                .then(data => {
                    forenameInput.value = data[1]["LastName"];
                    surnameInput.value = data[1]['FirstName'];
                    dobInput.value = formatDate(getRandomInRange(1950, 2002), getRandomInRange(1, 12), getRandomInRange(1, 28));
                    specialityInput.value = specialities[getRandomInRange(0, 4)];
                    formValidation(forenameInput, surnameInput, dobInput, modal);
                })
            });

        } else if (modalId === 'modalEdit') {
            const dataArray = e.target.getAttribute('data-info').split(', ');
            const [id, forename, surname, dob, speciality, position] = dataArray;

            const projects = document.querySelectorAll('.projectsEdit');
            const select = document.getElementById('worker-' + id);
            const projectsArray = select.querySelectorAll('option');

            for (let project of projects) {
                document.getElementById(project.id).checked = false;
            }

            for (let project of projects) {
                for (let option of projectsArray) {
                    if (project.id === option.value) {
                        document.getElementById(project.id).checked = true;
                    }
                }
            }

            idInput.value = id;
            forenameInput.value = forename;
            surnameInput.value = surname;
            dobInput.value = dateFormat(dob, ".", "-");
            specialityInput.value = speciality;
            positionInput.value = position;
        }

        formValidation(forenameInput, surnameInput, dobInput, modal);
    });
});

function dateFormat(old_date, old_separator, new_separator) {
    const [day, month, year] = old_date.split(old_separator);
    return year + new_separator + month + new_separator + day;
};

function getRandomInRange(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

function formatDate(year, month, day) {
    if (day < 10)
        day = '0' + day;
    if (month < 10)
        month = '0' + month;

    return year + '-' + month + '-' + day;
}

function formValidation(forenameInput, surnameInput, dobInput, modal) {
    if (forenameInput.value == '' || surnameInput.value == '' || dobInput.value == '') {
        modal.querySelector(".modalBtnAdd").setAttribute("disabled", "disabled");
    } else {
        modal.querySelector(".modalBtnAdd").removeAttribute("disabled");
    }
}