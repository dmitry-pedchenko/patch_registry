function message(msg, container_id, display_return, alarm_class) {
    var main = document.createElement("div");
    main.id = 'messager';
    main.classList.add('container');
    main.classList.add('align-items-center');
    main.style.zIndex = '10000';

    var row = document.createElement("div");
    row.classList.add('row');
    row.classList.add('align-items-center');

    var colunm = document.createElement("div");
    colunm.classList.add('col-md-4');
    colunm.classList.add('offset-md-4');
    colunm.classList.add('col-centered');

    var box = document.createElement("div");
    box.setAttribute('role','alert');
    box.classList.add('alert');
    box.classList.add(alarm_class);

    var textNode = document.createTextNode(msg);

    box.appendChild(textNode);
    colunm.appendChild(box);
    row.appendChild(colunm);
    main.appendChild(row);
    document.body.appendChild(main);
    setTimeout(function(container_id, display_return) {
        document.body.removeChild(document.getElementById('messager'));

        var name = "#" + container_id + " *";
        var container = document.getElementById(container_id);
        var style = container.style;
        style.display = display_return;
        $(name).prop('disabled',false);
    }, 5000, container_id, display_return);
}

function uploadPatch(url, form_id, container_id) {
    var display;
    var form = document.getElementById(form_id);
    var formData = new FormData(form);
    $.ajax({
        url: url,
        type: 'POST',
        data: formData,
        contentType: false,
        processData: false,
        error: function() {
            message("Error!",container_id, display, 'alert-danger');
        },
        success: function(result) {
            if ('status' in result && 'message' in result) {
                if (result['status'] == 200) {
                   message(result['message'],container_id, display, 'alert-success');
                   document.getElementById(form_id).reset();
                } else if (result['status'] == 500) {
                   message(result['message'],container_id, display, 'alert-danger');
                } else if (result['status'] == 201) {
                   message(result['message'],container_id, display, 'alert-warning');
                   document.getElementById(form_id).reset();
                } else {
                   message("Undocumented error. Contact to administrator.",container_id, display, 'alert-danger');
                }
            } else {
                message("Undocumented error. Contact to administrator.",container_id, display, 'alert-danger');
            }
        },
        beforeSend: function() {
            var name = "#" + container_id + " *";
            var container = document.getElementById(container_id);
            var style = container.style;
            display = style.display;
            style.display = 'none';
            $(name).prop('disabled',true);
        }
    });
}