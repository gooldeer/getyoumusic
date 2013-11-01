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
    window.setTimeout(getNameChangesFromServer(url), 1000);
}

function getNameChangesFromServer(url) {
    $.get(url)

    .done(function(data) {

        if (data) {
            //TODO change playlist name
        };
    })

    .fail(function() {
        alert("Can't change name");
    });
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