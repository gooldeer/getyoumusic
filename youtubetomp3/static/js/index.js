function getPopoverWrapperHtml() {
    return $('#popover_content_wrapper').html();
}

function add_to_playlist(playlist) {
    var media = $("#medialink").val();
    var link = "/playlists/" + playlist + "/add/media=" + media + "/";

    $.get(link)
    
    .done(function() {
        $("#progress-container").hide('slow');
    })
    .fail(function() {
        alert("FUCK!");
    });
}

$(document).ready(function() {

    var popover = $("[rel=popover]");

    if (popover.length) {

        popover.popover({

            html: true,
            content: getPopoverWrapperHtml

        });

    }
});
