$(document).ready(function() {

    var colorsPopover = $("#colorsPopover");

    if (colorsPopover.length) {

        colorsPopover.popover({

            html: true,
            content: getPopoverColorsWrapperHtml

        });

    }

    var mediasPopover = $("#mediasPopover");

    if (mediasPopover.length) {

        mediasPopover.popover({

            html: true,
            content: getPopoverMediasWrapperHtml

        });

    }
});

function getPopoverColorsWrapperHtml() {
    return $('#popover_colors_wrapper').html();
}

function getPopoverMediasWrapperHtml() {
    return $('#popover_medias_wrapper').html();
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

function add_to_playlist(playlist, media) {
    event.preventDefault();
    var link = "/playlists/" + playlist + "/add/media=" + media + "/";

    $.get(link)
    
    .done(function(data) {
        // alert(data);
    })
}