var app = angular.module('passbrain.app.dashboard', ['ngCookies']).
	config([
	'$httpProvider',
	function($httpProvider) {
		// Change content type for POST so Django gets correct request object
		$httpProvider.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
		// 2 reasons: Allows request.is_ajax() method to work in Django
		// Also, so 500 errors are returned in responses (for debugging)
		$httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
	}]).
	run([
	'$http',
	'$cookies',
	function($http, $cookies) {
		// Handles the CSRF token for POST
		$http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
	}]);

app.controller('DashboardController', function($scope, $http) {
    $scope.devices = [];
    $http(
        {method: 'GET',
        url: '/api/userdevices',
    }).
    success(function(data, status, headers, config) {
        $scope.devices = data.results;
    }).
    error(function(data, status, headers, config) {
        // called asynchronously if an error occurs
        // or server returns response with an error status.
        alert("Status: " + status + ", Data: " + data);
    });
    $scope.add = function(formdata) {
        // Add requesttype to data object
        formdata['requesttype'] = 'ADD';
        $http(
            {method: 'POST',
            url: '',
            data: $.param(formdata)
        }).
        success(function(data, status, headers, config) {
            // this callback will be called asynchronously
            // when the response is available
            $scope.dbconns = data['current_conns'];
        }).
        error(function(data, status, headers, config) {
            // called asynchronously if an error occurs
            // or server returns response with an error status.
            alert("Status: " + status + ", Data: " + data);
        });
    };
});
