function field_reassignment(select_div_id,select_field_id,text_div_id,text_field_id,trigger) {
    var select_field = document.getElementById(select_field_id);
    var select_value = select_field.options[select_field.selectedIndex].text;
    if (select_value == trigger) {
        var text_row = document.getElementById(text_div_id);
        text_row.style.display = select_field.style.display;

        var text_field = document.getElementById(text_field_id);
        text_field.type = "text";
    } else {
        var text_row = document.getElementById(text_div_id);
        text_row.style.display = "none";

        var text_field = document.getElementById(text_field_id);
        text_field.type = "hidden";
    }
}