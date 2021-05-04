function createComment(url, form_id) {
    var form = document.getElementById(form_id);
    var formData = new FormData(form);
    formData.set('csrfmiddlewaretoken', getCookie('csrftoken'));
    $.ajax({
        url: url,
        type: 'PUT',
        data: formData,
        contentType: false,
        processData: false,
        error: function() {
            show_message('Ошибка... Комментарий не был добавлен.','danger');
        },
        success: function(result) {
            document.location.reload(true);
        }
    });
}