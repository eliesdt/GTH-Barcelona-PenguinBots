chrome.tabs.onUpdated.addListener(function(tabId, changeInfo, tab) {
    if(tab.url.startsWith("https://www.kiwi.com")){
        var url = "http://localhost:8888/kiwi_detected?url="+tab.url;
        var xmlHttp = new XMLHttpRequest();
        xmlHttp.open( "GET", url, false );
        xmlHttp.send(null);

        artist = xmlHttp.responseText;
        // alert(artist);
    }
});

chrome.runtime.onMessage.addListener(function(sendResponse) {
    if(sendResponse['command'] == "play"){
        var url = "http://localhost:8888/play";
        var xmlHttp = new XMLHttpRequest();
        xmlHttp.open( "GET", url, false );
        xmlHttp.send(null);

        artist = xmlHttp.responseText;

        chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
            chrome.tabs.sendMessage(tabs[0].id, {command: "hello"}, function(response) {
              console.log("holaa",response.farewell);
            });
          });
        // alert(artist);
    }
    if(sendResponse['command'] == "previous"){
        var url = "http://localhost:8888/previous";
        var xmlHttp = new XMLHttpRequest();
        xmlHttp.open( "GET", url, false );
        xmlHttp.send(null);

        artist = xmlHttp.responseText;
        chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
            chrome.tabs.sendMessage(tabs[0].id, {command: "hello"}, function(response) {
              console.log("holaa",response.farewell);
            });
          });
        // alert(artist);
    }
    if(sendResponse['command'] == "next"){
        var url = "http://localhost:8888/next";
        var xmlHttp = new XMLHttpRequest();
        xmlHttp.open( "GET", url, false );
        xmlHttp.send(null);

        artist = xmlHttp.responseText;
        chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
            chrome.tabs.sendMessage(tabs[0].id, {command: "hello"}, function(response) {
              console.log("holaa",response.farewell);
            });
          });
        // alert(artist);
    }
    if(sendResponse['command'] == "auth"){
        var url = "https://accounts.spotify.com/authorize?client_id=db2be1573ba146aa92d752709b9d7240&response_type=code&redirect_uri=http%3A%2F%2Flocalhost%3A8888%2Fcallback&scope=playlist-modify-public+user-modify-playback-state+user-read-currently-playing+user-read-playback-state+user-read-recently-played+user-top-read";
        var xmlHttp = new XMLHttpRequest();
        xmlHttp.open( "GET", url, false );
        xmlHttp.send(null);

        artist = xmlHttp.responseText;
        chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
            chrome.tabs.sendMessage(tabs[0].id, {command: "hello"}, function(response) {
              console.log("holaa",response.farewell);
            });
          });
        // alert(artist);
    }


});
