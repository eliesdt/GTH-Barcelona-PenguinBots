document.getElementById("play").onclick = function() {
    if(document.getElementById("play").innerHTML=='<i class="material-icons md-48">play_circle_filled</i>'){
        document.getElementById("play").innerHTML = '<i class="material-icons md-48">pause_circle_filled</i>'
    }else{
        document.getElementById("play").innerHTML = '<i class="material-icons md-48">play_circle_filled</i>'
    }
    chrome.runtime.sendMessage({command:"play"},function(response){});
}
document.getElementById("previous").onclick = function() {
    chrome.runtime.sendMessage({command:"previous"},function(response){});
    change_artist();
}
document.getElementById("next").onclick = function() {
    chrome.runtime.sendMessage({command:"next"},function(response){});
    change_artist();
}
document.getElementById("auth").onclick = function() {
    chrome.runtime.sendMessage({command:"auth"},function(response){});
}

function change_artist(){
    artists = ["Python is funny","I like javascript","I'm sleepy","God Save The Coffee"]
    songs = ["Random Hacker","Elies Delgado","Random Penguin","The Sunflowers"]
    images = ["https://picsum.photos/id/629/200/200","https://picsum.photos/id/329/200/200","https://picsum.photos/id/154/200/200","https://picsum.photos/id/155/200/200","https://picsum.photos/id/189/200/200","https://picsum.photos/id/198/200/200",]
    dates = ["15th of May","13th of September","18th of October", "25th of January","25th of April"];

    document.getElementById("artist_image").src = images[Math.floor(Math.random()*images.length)];
    document.getElementById("artist").innerHTML = artists[Math.floor(Math.random()*artists.length)];
    document.getElementById("song").innerHTML = songs[Math.floor(Math.random()*songs.length)];
    document.getElementById("date").innerHTML = dates[Math.floor(Math.random()*dates.length)];
}

chrome.runtime.onMessage.addListener(
    function(request, sender, sendResponse) {
    alert(sendResponse);
      console.log(sender.tab ?
                  "from a content script:" + sender.tab.url :
                  "from the extension");
      if (request.greeting == "hello")
        sendResponse({farewell: "goodbye"});
    });
