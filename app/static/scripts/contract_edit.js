function modal_data(id, name, client, project) {

    var a = document.getElementById("id02").style.display='block';

    var select = document.getElementsByName(String(id))[0];

    var options = select.getElementsByTagName('option');

    let arr = [];

    for (var i = 0; i < options.length; i++)  {

        arr[i] = options[i].value;

    }

    document.getElementById("idContract2").value = id;
    document.getElementById("Name2").value = name;
    document.getElementById("Client2").value = client;

    for (var i = 1 in project)
    {
        document.getElementById(String(project[i])).checked = false;
    }


    for (var i = 1 in project)
    {
        for (var j = 0 in arr)
        {
            if (project[i] == arr[j])
            {
                document.getElementById(String(project[i])).checked = true;
            }
        }
    }
};