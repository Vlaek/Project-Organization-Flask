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
        console.log(dataArray);
        const idInput = dataArray[0];
        const nameInput = dataArray[1];
        const clientInput = dataArray[2];

        window.addEventListener('click', (e) => {
            const target = e.target;
            if (!target.closest('.modal__content') && !target.closest('.btn-open')) {
                document.getElementById(modalId).style.display = 'none';
            }
        });

        modal.addEventListener('change', () => {
            formValidation(nameInput, clientInput, modal);
        });

        if (modalId === 'modalEdit') {
//            const dataArray = e.target.getAttribute('data-info').split(', ');
//            const [id, name, client, other] = dataArray;
//            console.log(other);
//            const options = document.querySelectorAll('.leadersEdit');

//            for (let option of options) {
//                option.selected = false;
//                if (option.value === ('leader-' + leader)) {
//                    option.selected = true;
//                }
//            }

            idInput.value = id;
            nameInput.value = name;
            clientInput.value = cost;
        }

        formValidation(nameInput, clientInput, modal);
    });
});

function dateFormat(old_date, old_separator, new_separator) {
    const [day, month, year] = old_date.split(old_separator);
    return year + new_separator + month + new_separator + day;
};

function formValidation(nameInput, clientInput, modal) {
    if (nameInput.value == '' || clientInput.value == '') {
        modal.querySelector(".modalBtnAdd").setAttribute("disabled", "disabled");
    } else {
        modal.querySelector(".modalBtnAdd").removeAttribute("disabled");
    }
}