//function modal_data(id, surname, forename, dob, speciality, position, project) {
//    let a = document.getElementById("id02").style.display='block';
//    let select = document.getElementsByName(String(id))[0];
//    let options = select.getElementsByTagName('option');
//    let arr = [];
//
//    for (let i = 0; i < options.length; i++)  {
//        arr[i] = options[i].value;
//    }
//
//    document.getElementById("Forename2").value = forename;
//    document.getElementById("Surname2").value = surname;
//    document.getElementById("DOB2").value = dateFormat(dob, ".", "-");
//    document.getElementById("Speciality2").value = speciality;
//    document.getElementById("Position2").value = position;
//    document.getElementById("Worker2").value = id;
//
//    for (let i = 0 in project) {
//        document.getElementById(String(project[i])).checked = false;
//    }
//
//    for (let i = 1 in project) {
//        for (let j = 0 in arr) {
//            if (project[i] == arr[j]) {
//                document.getElementById(String(project[i])).checked = true;
//            }
//        }
//    }
//
//};
//
//function dateFormat(old_date, old_separator, new_separator) {
//    let new_date = old_date.split(old_separator);
//    return new_date[2] + new_separator + new_date[1] + new_separator + new_date[0];
//};