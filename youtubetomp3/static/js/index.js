function getPopoverWrapperHtml(is_audio) {
    if (is_audio) 
        return $('#audio_popover_content_wrapper').html();
    else
        return $('#video_popover_content_wrapper').html();
}

function add_to_playlist(playlist) {
    var media = $("#medialink").val();
    var link = "/playlists/" + playlist + "/add/media=" + media + "/";

    $.get(link)
    
    .done(function() {
        $("#progress-container").hide('slow');
    })
}

$(document).ready(function() {

    var audioPopover = $("[rel=popover_audio]");
    var videoPopover = $("[rel=popover_video]");

    if (audioPopover.length && videoPopover.length) {

        audioPopover.popover({

            html: true,
            content: getPopoverWrapperHtml(true)

        });

        videoPopover.popover({

            html: true,
            content: getPopoverWrapperHtml(false)

        });

    }
});
