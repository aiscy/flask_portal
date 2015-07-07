app.factory('foods', ['$http', function ($http) {

	return $http.get('/api/v1/service/foodmenu').success(function (data) {return data; }).error(function (err) {return error; });
}]);