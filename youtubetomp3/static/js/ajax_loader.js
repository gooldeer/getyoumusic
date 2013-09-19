// to update progress info
function updateProgressInfo() {
    var uuid = $("#progress-id").val();
    var progress_url = "/youtubetomp3/poll_state/?job=" + uuid; // ajax view serving progress info

    $.get(progress_url, 
        function(data){

            if (data == "PENDING" || data.current) {
                
                var progress = parseFloat(data.current);
                $("#upload-progress-bar").attr('aria-valuenow', progress);
                $("#upload-progress-bar").attr('style', "width: " + progress + "%");
                window.setTimeout(updateProgressInfo, 2000);

            } else {
                if (data == "SUCCESS") {
                    var progress = 100;
                    $("#upload-progress-bar").attr('aria-valuenow', progress);
                    $("#upload-progress-bar").attr('style', "width: " + progress + "%");
                }
                $("#progress-container").hide('slow');
            }
    })
    .fail(
        function () {
            $("#progress-container").hide('slow');
    });
};

// pre-submit callback
function beforeSubmitHandler(formData, jqForm, options) {
    window.setTimeout(updateProgressInfo, 2000);
    $("#progress-container").show('slow');
    return true;
};

// post-submit callback
function successHandler(responseText, statusText, xhr, $form) {

    $("#progress-id").val(responseText);
    return true;
};

// on page load
$(document).ready(function() {

    $("#button-submit").click(function () {

        var options = {

            url: "/youtubetomp3/init_work/?youtubeLink="+$("#youtubeLink").val(),
            beforeSubmit: beforeSubmitHandler,
            success: successHandler
        };

        $("#upload-file-form").ajaxForm(options);
    });
});