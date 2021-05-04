function show_message(text, type, delay, callback) {
    var alerts = {primary: ["alert-primary"],
                  secondary: ["alert-secondary"],
                  success: ["alert-success"],
                  danger: ["alert-danger"],
                  warning: ["alert-warning"],
                  info: ["alert-info"],
                  light: ["alert-light"],
                  dark: ["alert-dark"]}
    var main = document.getElementById('messager_container');

    if (!type) type = 'primary';
    var row = create_div('alert',alerts[type],{role:'alert'});

    if (typeof(text) == "string") {
        text = document.createTextNode(text);
    }

    add_element(row,text);
    add_element(main,row);

    if (!delay) delay = 5000;
    setTimeout(function (m,s) {
            remove_element(m,s);
            if (callback) callback();
        }, delay, main, row);
}