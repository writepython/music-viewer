    $scope.updateUsername = function(username) {
	$scope.username = username;
    };

    if $scope.username == 'writepython' {
	$scope.rsp = 'ok';
    }
    else {
	$scope.rsp = 'not ok';
    }
musicApp.factory( 'User', function (username) {
    return {'name': username};
});

