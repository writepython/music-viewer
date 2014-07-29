var musicApp = angular.module('musicApp', []);

musicApp.controller('MusicCtrl', ['$scope', '$http', '$templateCache',
  function($scope, $http, $templateCache) {
    $scope.method = 'GET';
    $scope.url = 'http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user=writepython&api_key=d44fcea4e2a564b4986245ed24796ca3';

      $scope.code = null;
      $scope.response = null;

      $http({method: $scope.method, url: $scope.url, cache: $templateCache}).
        success(function(data, status) {
          $scope.status = status;
          $scope.data = data;
        }).
        error(function(data, status) {
          $scope.data = data || "Request failed";
          $scope.status = status;
      });

    $scope.updateModel = function(method, url) {
      $scope.method = method;
      $scope.url = url;
    };
  }]);

