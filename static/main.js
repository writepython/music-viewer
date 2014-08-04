var musicApp = angular.module( 'musicApp', [] );

musicApp.controller( 'MusicCtrl', ['$scope', '$http', '$timeout', function($scope, $http, $timeout) {

$scope.username = localStorage.getItem("username");
$scope.realname = localStorage.getItem("realname");

if ($scope.username) { getLastfmData() }
else {
    $scope.track_name = 'Song'
    $scope.track_artist = 'Artist'
    $scope.track_album = 'Album'
    $scope.image_src = 'placeholder.jpg'
    $scope.image_title = ''
}

function getBestImageFromArray(images) {
    var image_large = '';
    var image_medium = '';
    var image_small = '';

    for (i = 0; i < images.length; i++) {
	var current_image = images[i];
	var size = current_image.size;
	var image_url = current_image["#text"];
	if (image_url) {
	    if (size == "extralarge") { return image_url }
	    else if (size == "large") { image_large = image_url }
	    else if (size == "medium") { image_medium = image_url }
	    else if (size == "small") { image_small = image_url }
	}
    }  
    if (image_large) { return image_large } 
    else if (image_medium) { return image_medium } 
    else if (image_small) { return image_small } 
    return false;
};

function getConcertData(mbid, track_name) {
/*    $.ajax({
        type: "POST", 
        url:  "/trash/record-geolocation-error/", 
        data: {error_message: msg},
        cache: false
    });
*/
    var setlist_params = {'mbid': mbid, 'track_name': track_name};
    $http({method: 'POST', url: '/py/setlist/', data: setlist_params}).
	success(function(data, status) {
	    //$scope.concert_artist_url = data //artist_url;
	    var setlist_artist_url = data; //.artist.url;
	    $scope.x = setlist_artist_url;
	}).
        error(function(data, status) {
            //$scope.data = 
            $scope.x = data || "Request failed";
	});	    
};

function getLastfmUserInfo() {
    var user_info_url_template = 'http://ws.audioscrobbler.com/2.0/?method=user.getinfo&api_key=d44fcea4e2a564b4986245ed24796ca3&format=json&user=';
    var username_trimmed = $scope.username.trim()
    var user_info_url = user_info_url_template + username_trimmed
    $http({method: 'GET', url: user_info_url}).
	success(function(data, status) {
	    var realname = data.user.realname;
	    var name = data.user.name;
	    if (realname) { 
		$scope.realname = realname;
		localStorage.setItem("realname", realname);
	    }
	    else if (name) { 
		$scope.realname = name;
		localStorage.setItem("realname", name);
	    }
	});
};

function getLastfmData() {
    var recent_tracks_url_template = 'http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&api_key=d44fcea4e2a564b4986245ed24796ca3&limit=2&extended=1&format=json&user=';
    var username_trimmed = $scope.username.trim()
    var recent_tracks_url = recent_tracks_url_template + username_trimmed
    $http({method: 'GET', url: recent_tracks_url}).
	success(function(data, status) {
            $scope.status = status;
            $scope.time = new Date().toLocaleString();
	    var last_played = data.recenttracks.track[0];
	    var artist = last_played.artist;
	    var track_name = last_played.name;
	    $scope.track_name = track_name;
	    $scope.track_artist = artist.name;
	    $scope.track_album = last_played.album["#text"] || "Unknown";
	    var images = last_played.image; // Try track images first.
	    var image_source = getBestImageFromArray(images);
	    if (image_source) { 
		$scope.image_src = image_source;
		$scope.image_title = $scope.track_name;
	    }
	    else { 
		var images = artist.image; // Otherwise try artist images.
		var image_source = getBestImageFromArray(images);
		if (image_source) { 
		    $scope.image_src = image_source;
		    $scope.image_title = $scope.track_artist;
		}
		else { 
		    $scope.image_src = 'placeholder.jpg'; 
		    $scope.image_title = '';
		}
	    }
	    var mbid = artist.mbid
	    getConcertData(mbid, track_name);
	    $timeout(getLastfmData, 10000);
	}).
        error(function(data, status) {
            //$scope.data = data || "Request failed";
            $scope.status = status;
            $scope.time = new Date().toLocaleString();
	});
};

$scope.updateUsername = function() {
    getLastfmData();
    localStorage.setItem("username", $scope.username);
    $scope.realname = $scope.username;
    localStorage.setItem("realname", $scope.username);
    getLastfmUserInfo();
};

}]);

