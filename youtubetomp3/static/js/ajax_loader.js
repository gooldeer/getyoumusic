// to update progress info
function updateProgressInfo() {
    var uuid = $("#progress-id").val();
    var progress_url = "/poll_state/?job=" + uuid; // ajax view serving progress info

    $.getJSON(progress_url, 
        function(data, status){

            if (data == "PENDING" || data.current) {
                
                var progress = parseFloat(data.current);
                $("#upload-progress-bar").attr('aria-valuenow', progress);
                $("#upload-progress-bar").attr('style', "width: " + progress + "%");
                window.setTimeout(updateProgressInfo, 1000);

            } else if (data) {
                 
                // alert(data.url);
                var progress = 100;
                $("#upload-progress-bar").attr('aria-valuenow', progress);
                $("#upload-progress-bar").attr('style', "width: " + progress + "%");
                
                $("#medialink").val(data);
            } 
    })
    .fail(
        function () {
            // $("#progress-container").hide('slow');
    });
};

// pre-submit callback
function beforeSubmitHandler(formData, jqForm, options) {
    window.setTimeout(updateProgressInfo, 1000);
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

            url: "/init_work/?youtubeLink="+$("#youtubeLink").val(),
            beforeSubmit: beforeSubmitHandler,
            success: successHandler
        };

        $("#upload-file-form").ajaxForm(options);
    });
});