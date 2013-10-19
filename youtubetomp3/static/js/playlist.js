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

function getColorChagesFromServer(url) {

    $.get(url)

    .done(function(data) {

        if (data) {
            //TODO change url to {% static '...' %}
            $("#color").attr("src", "/static/img/" + data + ".png");
        }

    })
    
    .fail(function() {
        alert("Can't change color");
    });

}