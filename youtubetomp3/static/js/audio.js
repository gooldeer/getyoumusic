var id;
var activeSong;
var container;
//Plays the song. Just pass the id of the audio element.
function play(id){
    //Sets the active song to the song being played.  All other functions depend on this.
    activeSong = document.getElementById(id);
    //Plays the song defined in the audio tag.
    activeSong.play();
    
    //Calculates the starting percentage of the song.
    var percentageOfVolume = activeSong.volume / 1;
    var percentageOfVolumeMeter = container.find('#volumeMeter').width * percentageOfVolume;
    
    //Fills out the volume status bar.
    container.find('#volumeStatus').width(Math.round(percentageOfVolumeSlider));
}
//Pauses the active song.
function pause(){
    activeSong.pause();
}
//Does a switch of the play/pause with one button.
function playPause(id){
    //stops playing song if it is
    var oldActiveSong = activeSong;
    var oldContainer = container;

    //Sets the active song since one of the functions could be play.
    container = $("#" + id);
    activeSong = document.getElementById("song" + id);
    playButton = container.find("#play-pause");
    playImageSource = $("#songPlayImage").val();
    pauseImageSource = $("#songPauseImage").val();

    //Checks to see if the song is paused, if it is, play it from where it left off otherwise pause it.
    if (activeSong.paused) {

         playButton.attr('src', pauseImageSource);
         activeSong.play();
    } else {

         activeSong.pause();
         playButton.attr('src', playImageSource);
    }

    if (oldActiveSong != activeSong && !oldActiveSong.paused) {
        oldActiveSong.pause();
        playButton = oldContainer.find("#play-pause");
        playButton.attr('src', playImageSource);
    }
}

//Updates the current time function so it reflects where the user is in the song.
//This function is called whenever the time is updated.  This keeps the visual in sync with the actual time.
function updateTime(){
    var currentSeconds = 
        (Math.floor(activeSong.currentTime % 60) < 10 ? '0' : '') + Math.floor(activeSong.currentTime % 60);
    var currentMinutes = Math.floor(activeSong.currentTime / 60);
    //Sets the current song location compared to the song duration.
    container.find("#songTime").html(currentMinutes + ":" + currentSeconds + ' / ' + 
        Math.floor(activeSong.duration / 60) + ":" + 
        (Math.floor(activeSong.duration % 60) < 10 ? '0' : '') + 
        Math.floor(activeSong.duration % 60));

    //Fills out the slider with the appropriate position.
    var percentageOfSong = (activeSong.currentTime/activeSong.duration);
    var percentageOfSlider = container.find("#songSlider").width() * percentageOfSong;
    
    //Updates the track progress div.
    container.find('#trackProgress').width(Math.round(percentageOfSlider));
}
function volumeUpdate(number){
    //Updates the volume of the track to a certain number.
    activeSong.volume = number / 100;
}
//Changes the volume up or down a specific number
function changeVolume(number, direction){
    //Checks to see if the volume is at zero, if so it doesn't go any further.
    if(activeSong.volume >= 0 && direction == "down"){
        activeSong.volume = activeSong.volume - (number / 100);
    }
    //Checks to see if the volume is at one, if so it doesn't go any higher.
    if(activeSong.volume <= 1 && direction == "up"){
        activeSong.volume = activeSong.volume + (number / 100);
    }
    
    //Finds the percentage of the volume and sets the volume meter accordingly.
    var percentageOfVolume = activeSong.volume / 1;
    var percentageOfVolumeSlider = container.find('#volumeMeter').width() * percentageOfVolume;
    
    document.getElementById('volumeStatus').width(Math.round(percentageOfVolumeSlider));
}
//Sets the location of the song based off of the percentage of the slider clicked.
function setLocation(percentage){
    activeSong.currentTime = activeSong.duration * percentage;
}
/*
Gets the percentage of the click on the slider to set the song position accordingly.
Source for Object event and offset: http://website-engineering.blogspot.com/2011/04/get-x-y-coordinates-relative-to-div-on.html
*/
function setSongPosition(obj,e){
    //Gets the offset from the left so it gets the exact location.
    var songSliderWidth = obj.offsetWidth;
    var evtobj=window.event? event : e;
    clickLocation =  evtobj.layerX - $(obj).offset().left;
    
    var percentage = (clickLocation/songSliderWidth);
    //Sets the song location with the percentage.
    setLocation(percentage);
}

//Set's volume as a percentage of total volume based off of user click.
function setVolume(percentage,container){
    activeSong.volume =  percentage;
    
    var percentageOfVolume = activeSong.volume / 1;
    var percentageOfVolumeSlider = container.find('#volumeMeter').width() * percentageOfVolume;
    
    container.find('#volumeStatus').width(Math.round(percentageOfVolumeSlider));
}

//Set's new volume id based off of the click on the volume bar.
function setNewVolume(obj,e,id){
    var container = $("#" + id);
    var volumeSliderWidth = obj.offsetWidth;
    var evtobj = window.event? event: e;
    clickLocation = evtobj.layerX - $(obj).offset().left;
    
    var percentage = (clickLocation/volumeSliderWidth);
    setVolume(percentage,container);
}
//Stop song by setting the current time to 0 and pausing the song.
function stopSong(){
    activeSong.currentTime = 0;
    activeSong.pause();
}