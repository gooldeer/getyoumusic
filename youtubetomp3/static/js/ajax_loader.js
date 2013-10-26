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

function updateConvertInfo() {
    var uuid = $("#progress-id").val();
    var progress_url = "/poll_state/?job=" + uuid; // ajax view serving progress info

    $.getJSON(progress_url,
        function(data, status) {
            if (data == "PROGRESS" || data == "PENDING") {
                window.setTimeout(updateConvertInfo, 1000);
            }
            else if (data) {
                $("#medialink").val(data);
                alert(data);
            }   
        });
}

// pre-submit callback
function beforeSubmitHandler(formData, jqForm, options) {
    window.setTimeout(updateProgressInfo, 1000);
    $("#progress-container").show('slow');
    return true;
};

// pre-convert callback
function beforeConvertHandler(formData, jqForm, options) {
    window.setTimeout(updateConvertInfo, 1000);
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

            url: "/init_work/",
            beforeSubmit: beforeSubmitHandler,
            success: successHandler
        };

        $("#upload-file-form").ajaxForm(options);
    });

    $("#button-convert").click(function() {

        var options = {

            url: "/init_work/",
            beforeSubmit: beforeConvertHandler,
            success: successHandler
        };

        $("#upload-file-form").ajaxForm(options);
    });
});