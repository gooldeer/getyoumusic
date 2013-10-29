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
                 
                var progress = 100;
                $("#upload-progress-bar").attr('aria-valuenow', progress);
                $("#upload-progress-bar").attr('style', "width: " + progress + "%");
                
                $("#medialink").val(data);
                $("#afterDownloading").show('slow');
            } 
    })
    .fail(
        function () {
            // $("#progress-container").hide('slow');
    });
};

function updateConvertInfo(audio) {
    var uuid = $("#progress-id").val();
    var progress_url = "/poll_state/?job=" + uuid; // ajax view serving progress info

    $.getJSON(progress_url,
        function(data, status) {
            if (data == "PROGRESS" || data == "PENDING") {
                window.setTimeout(
                    function() {
                        updateConvertInfo(audio);
                    }, 1000);
            }
            else if (data) {
                $("#medialink").val(data);
                hideAllChildrens($("#afterDownloading"));

                if (audio) {
                    $("#audioPlaylistsLabel").show('slow');
                } else {
                    $("#videoPlaylistsLabel").show('slow');
                }
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
    return true;
};

// post-submit callback
function successHandler(responseText, statusText, xhr, $form) {

    $("#progress-id").val(responseText);
    return true;
};

// post-submit callback
function successAudioHandler(responseText, statusText, xhr, $form) {
    $("#progress-id").val(responseText);
    window.setTimeout(
        function() {
            updateConvertInfo(true);
        }, 1000);
    return true;
};

// post-submit callback
function successVideoHandler(responseText, statusText, xhr, $form) {
    $("#progress-id").val(responseText);
    window.setTimeout(
        function() {
            updateConvertInfo(false);
        }, 1000);
    return true;
};

function hideAllChildrens(parent) {
    parent.children().hide();    
}

// on page load
$(document).ready(function() {

    buttonSubmit = $("#button-submit");
    buttonConvert = $("#button-convert");
    saveAsVideo = $("#saveAsVideo");
    // uploadFileForm = $("#upload-file-form");

    buttonSubmit.click(function () {

        var options = {

            url: "/download/",
            beforeSubmit: beforeSubmitHandler,
            success: successHandler
        };

        $("#upload-file-form").ajaxForm(options);
    });

    buttonConvert.click(function() {

        $("#buttonConvertText").text("Converting...");
        $("#saveAsVideoContainer").hide('slow');
        $("#convertSpinner").show('slow');

        var options = {

            url: "/convert/audio/",
            beforeSubmit: beforeConvertHandler,
            success: successAudioHandler
        };

        $("#upload-file-form").ajaxForm(options);
        this.attr('disabled', 'disabled');

    });

    saveAsVideo.click(function() {

        savingLabel = $("#savingLabel");
        

        var options = {

            url: "/convert/video/",
            beforeSubmit: beforeConvertHandler,
            success: successVideoHandler
        };

        $("#upload-file-form").ajaxForm(options);

        hideAllChildrens($("#afterDownloading"));
        savingLabel.show('slow');
    });
});