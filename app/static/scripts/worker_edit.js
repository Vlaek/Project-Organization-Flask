function modal_data(id, surname, forename, dob, speciality, position) {

    var a = document.getElementById("id02").style.display='block';

    document.getElementById("Forename2").value = forename;
    document.getElementById("Surname2").value = surname;
    document.getElementById("DOB2").value = dateFormat(dob, ".", "-");
    document.getElementById("Speciality2").value = speciality;
    document.getElementById("Position2").value = position;
    document.getElementById("Worker2").value = id;
};

function dateFormat(old_date, old_separator, new_separator) {

    var new_date = old_date.split(old_separator);

    return new_date[2] + new_separator + new_date[1] + new_separator + new_date[0];
};