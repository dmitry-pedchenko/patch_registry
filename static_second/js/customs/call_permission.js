function change_permission(uid,username,patchname,level,callback_text,callback_url) {
    var api_url = '/patches/list/' + uid + '/' + username + '/';

    var row_id = "tr_" + uid + '_' + username;
    var row_element = document.getElementById(row_id);
    var form_data = document.getElementById('set_permission');

    var sendForm = new FormData(form_data);
    sendForm.append("username",username);
    sendForm.append("level", level);
    $.ajax({
        url: api_url,
        type: 'POST',
        data: sendForm,
        contentType: false,
        processData: false,
        error: function() {
            remove_childs(row_element);
            var col_element = document.createElement("td");
            col_element.colSpan = 4;
            col_element.innerText = 'Ошибка... Попробуйте обновить страницу.';
            add_element(row_element, col_element);
            show_message('Ошибка... Попробуйте обновить страницу.','danger');
        },
        success: function(result) {
            remove_childs(row_element);
            build_table_row(row_element, result, uid, username, patchname, callback_text, callback_url);
        },
        beforeSend: function() {
            remove_childs(row_element);
            var td_element = document.createElement("td");
            td_element.colSpan = 4;
            td_element.innerText = 'Ожидайте...'
            row_element.appendChild(td_element);
        }
    })
}

function build_table_row(master, result, uid, username, patchname, callback_text, callback_url) {
    var status = {1:
                    { level: 1,
                      name: "Чтение",
                      action: "Запретить",
                      newClassName: "bg-secondary",
                      newLevel: 0},
                  0:
                    { level: 0,
                      name: "Запрещен",
                      action: "Разрешить",
                      newClassName: "bg-danger",
                      newLevel: 1}}

    var status_array;
    if ('level' in result) {
        status_array = status[result['level']];
    } else {
        show_message('Ошибка... Попробуйте обновить страницу.','danger');
        return
    }

    master.className = status_array['newClassName']
    var elem = create_element('th',['align-middle', 'text-white'],{'scope':'row'});
    elem.innerText = master.rowIndex;
    add_element(master,elem);

    var elem = create_element('td',['align-middle']);
    var button = create_element('a',['btn', 'btn-link', 'btn-block', 'text-white'],{'role':'button','href': callback_url});
    button.innerText = callback_text;
    add_element(elem,button);
    add_element(master,elem);

    var elem = create_element('td',['align-middle', 'text-white']);
    elem.innerText = status_array['name'];
    add_element(master,elem);

    var elem = create_element('td',['align-middle']);
    var button = create_element('a',['btn', 'btn-link', 'btn-block', 'text-white'],{'role':'button', 'href': '#'});
    button.innerText = status_array['action'];
    button.onclick = function () {
        change_permission(uid,username,patchname,status_array['newLevel'],callback_text,callback_url);
    }
    add_element(elem,button);
    add_element(master,elem);
}