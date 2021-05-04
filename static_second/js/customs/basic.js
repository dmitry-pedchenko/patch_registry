function create_element(type, options, set_options) {
    var main = document.createElement(type);
    if (!options) options = [];
    for (i=0; i<options.length; i++) {
        main.classList.add(options[i])
    }

    if (!set_options) set_options = {};
    for (const [key, value] of Object.entries(set_options)) {
        main.setAttribute(key,value)
    }

    return main
}

function create_div(type, options, set_options) {
    var main = document.createElement("div");

    if (!type) type = 'row';
    main.classList.add(type)

    if (!options) options = [];
    for (i=0; i<options.length; i++) {
        main.classList.add(options[i])
    }

    if (!set_options) set_options = {};
    for (const [key, value] of Object.entries(set_options)) {
        main.setAttribute(key,value)
    }

    return main
}

function add_element(master,slave) {
    master.appendChild(slave);
}

function remove_element(master,slave) {
    master.removeChild(slave);
}

function remove_childs(master) {
     while (master.firstChild) {
        master.removeChild(master.firstChild);
    }
}