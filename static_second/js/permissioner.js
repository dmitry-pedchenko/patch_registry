function change_permission(uid,username,level,num,target,patchname,callback_url) {
    var tr_id = "tr_" + uid + '_' + username;
    var tr_element = document.getElementById(tr_id);

    var form = document.getElementById('set_permission');
    var formData = new FormData(form);
    formData.append("username",username);
    formData.append("level", level);
    $.ajax({
        url: '/patches/list/' + uid + '/permission/',
        type: 'POST',
        data: formData,
        contentType: false,
        processData: false,
        error: function() {
            while (tr_element.firstChild) {
                tr_element.removeChild(tr_element.firstChild);
            }

            var td_element = document.createElement("td");
            td_element.colSpan = 4;
            td_element.innerText = 'Ошибка... Попробуйте обновить страницу.'
            tr_element.appendChild(td_element);
        },
        success: function(result) {
            while (tr_element.firstChild) {
                tr_element.removeChild(tr_element.firstChild);
            }
            tr_element.className = result['class'];

            var td_element1 = document.createElement("th");
            var td_element2 = document.createElement("td");
            var td_element3 = document.createElement("td");
            var td_element4 = document.createElement("td");

            td_element1.classList.add('align-middle');
            td_element2.classList.add('align-middle');
            td_element3.classList.add('align-middle');
            td_element4.classList.add('align-middle');

            td_element1.scope = 'row';
            td_element1.innerText = num;

            td_element3.innerText = result['premission'];

            var button1 = document.createElement("a");
            var button2 = document.createElement("a");

            button1.role = 'button';
            button2.role = 'button';

            button1.className = "btn btn-link btn-block text-white";
            button2.className = "btn btn-link btn-block text-white";

            button1.href = callback_url;
            button2.href = "#";

            if (target == 'user') {
                 button1.innerText = patchname;
            }
            if (target == 'patch') {
                 button1.innerText = username;
            }
            button2.innerText = result['action'];

            button2.onclick = function() { change_permission(uid,username,result['newlevel'],num,target,patchname,callback_url); }

            td_element2.appendChild(button1);
            td_element4.appendChild(button2);

            tr_element.appendChild(td_element1);
            tr_element.appendChild(td_element2);
            tr_element.appendChild(td_element3);
            tr_element.appendChild(td_element4);
        },
        beforeSend: function() {
            while (tr_element.firstChild) {
                tr_element.removeChild(tr_element.firstChild);
            }

            var td_element = document.createElement("td");
            td_element.colSpan = 4;
            td_element.innerText = 'Ожидайте...'
            tr_element.appendChild(td_element);
        }
    });
}