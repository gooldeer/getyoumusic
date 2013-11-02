$(document).ready(function() {

    var popover = $("[rel=popover]");

    if (popover.length) {

        popover.popover({

            html: true,
            content: getPopoverWrapperHtml

        });

    }
});

function getPopoverWrapperHtml() {
    return $('#popover_content_wrapper').html();
}

function changeColor(url) {
    window.setTimeout(getColorChagesFromServer(url), 1000);
}

function changeName(url) {
    form = $("#changeNameForm");
    modal = $("#changeNameModal");

    form.attr('action', url);
    modal.modal('show');
}

function changeMediaName(url) {
    form = $("#changeNameForm");
    modal = $("#changeNameModal");

    form.ajaxForm({
        url: url,
        dataType: 'json',
        beforeSubmit: function () {
            modal.modal('hide');
        },
        success: function (response) {
            $("#name" + response.id).text(response.name);
        }
    });

    // form.attr('action', url);
    modal.modal('show');
}

function getColorChagesFromServer(url) {

    $.get(url)

    .done(function(data) {

        if (data) {
            $("#color").attr("src", "/static/img/" + data.color + ".png");
        }

    })
    
    .fail(function() {
        alert("Can't change color");
    });

}