const close = document.getElementsByClassName('close');
const openBtn = document.getElementsByClassName('btn-open');

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
        const nameInput = dataArray[1];
        const clientInput = dataArray[2];
        const projects = modal.querySelectorAll('.projectsEdit');

        window.addEventListener('click', (e) => {
            const target = e.target;
            if (!target.closest('.modal__content') && !target.closest('.btn-open')) {
                document.getElementById(modalId).style.display = 'none';
            }
        });

        modal.addEventListener('change', () => {
            formValidation(nameInput, clientInput, projects, modal);
        });

        if (modalId === 'modalEdit') {
            const dataArray = e.target.getAttribute('data-info').split(', ');
            const [id, name, client] = dataArray;
            console.log(projects)
            const select = document.getElementById('contract-' + id);
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
            nameInput.value = name;
            clientInput.value = client;
        }

        formValidation(nameInput, clientInput, projects, modal);
    });
});

function dateFormat(old_date, old_separator, new_separator) {
    const [day, month, year] = old_date.split(old_separator);
    return year + new_separator + month + new_separator + day;
};

function formValidation(nameInput, clientInput, projects, modal) {
    let checked = modal.querySelector('.projectsEdit:checked') || 0;
    if (nameInput.value == '' || clientInput.value == '' || checked === 0) {
        modal.querySelector(".modalBtnAdd").setAttribute("disabled", "disabled");
    } else {
        modal.querySelector(".modalBtnAdd").removeAttribute("disabled");
    }
}