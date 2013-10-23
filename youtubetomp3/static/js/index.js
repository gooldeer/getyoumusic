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
