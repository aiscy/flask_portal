app.controller('MainController', ['$scope', 'foods', function ($scope, foods) {
	foods.success(function (data) {
		$scope.foodMenu = data;
	});
}]);