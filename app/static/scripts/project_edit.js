function modal_data(id, name, leader, equipment, start_date, end_date, cost) {
    let a = document.getElementById("id02").style.display='block';
    document.getElementById("Name2").value = name;
    document.getElementById("Leader2").value = leader;
    document.getElementById("StartDate2").value = dateFormat(start_date, ".", "-");
    document.getElementById("EndDate2").value = dateFormat(end_date, ".", "-");
    document.getElementById("Equipment2").value = equipment;
    document.getElementById("Cost2").value = cost;
    document.getElementById("idProject2").value = id;
};

function dateFormat(old_date, old_separator, new_separator) {

    var new_date = old_date.split(old_separator);

  return new_date[2] + new_separator + new_date[1] + new_separator + new_date[0];
};