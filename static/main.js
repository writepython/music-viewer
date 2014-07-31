var musicApp = angular.module( 'musicApp', [] );

musicApp.controller( 'MusicCtrl', ['$scope', '$http', '$templateCache', function($scope, $http, $templateCache) {

$scope.track_name = 'Song'
$scope.track_artist = 'Artist'
$scope.track_album = 'Album'

function setImageSourceFromArray(images) {
    var image_large = '';
    var image_medium = '';
    var image_small = '';

    for (i = 0; i < images.length; i++) {
	var current_image = images[i];
	var size = current_image.size;
	var image_url = current_image["#text"];
	if (image_url) {
	    if (size == "extralarge") {
		$scope.image_src = image_url;
		break;
	    }
	    else if (size == "large") { image_large = image_url }
	    else if (size == "medium") { image_medium = image_url }
	    else if (size == "small") { image_small = image_url }
	}
    }  
    if ( !($scope.image_src) ) {
	if (image_large) { $scope.image_src = image_large } 
	else if (image_medium) { $scope.image_src = image_medium } 
	else if (image_small) { $scope.image_src = image_small } 
    }
};

function getLastfmData() {
    $scope.image_src = ''
    var recent_tracks_url_template = 'http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&api_key=d44fcea4e2a564b4986245ed24796ca3&format=json&user=';

    var username_trimmed = $scope.username.trim()
    var recent_tracks_url = recent_tracks_url_template + username_trimmed
    $http({method: 'GET', url: recent_tracks_url}).
	success(function(data, status) {
            //$scope.status = status;
            //$scope.data = data;
	    var images = data.recenttracks.track[0].image;
	    setImageSourceFromArray(images);
	}).
        error(function(data, status) {
            $scope.data = data || "Request failed";
            $scope.status = status;
	});
};

$scope.updateUsername = function() {
    getLastfmData();
};

}]);

