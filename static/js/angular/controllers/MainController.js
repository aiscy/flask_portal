app.controller('MainController', ['$scope', '$http', function ($scope, $http) {
	'use strict';
	$scope.loading = true;
	var promise = $http.get('/api/v1/service/foodmenu').success(function (data) {
		return $scope.menus = data;
	})
    .catch(function (err) {
      // Log error somehow.
    })
    .finally(function () {
      // Hide loading spinner whether our call succeeded or failed.
      $scope.loading = false;
		$scope.myStyle={'opacity': '1'}
    });


	promise.then(function (data) {
		$scope.minus = function (parentIndex, index) {
			if ($scope.menus.menu[parentIndex].content[index].count > 0) {
				//				$scope.cartform.$setDirty();
				$scope.menus.menu[parentIndex].content[index].count--;
				items_cart();
			}
		};
		$scope.plus = function (parentIndex, index) {
			//			$scope.cartform.$setDirty();
			$scope.menus.menu[parentIndex].content[index].count++;
			items_cart();
		};
		$scope.complexMinus = function () {
			if ($scope.menus.menu_complex.count > 0) {
				$scope.menus.menu_complex.count--;
				items_cart();
			}
		};
		$scope.complexPlus = function () {
			$scope.menus.menu_complex.count++;
			items_cart();
		};

		// подсчет итоговой суммы

		$scope.total = function () {
			var total = 0;
			angular.forEach($scope.menus.menu, function (menuObj, index) {
				angular.forEach(menuObj.content, function (value) {
					total += value.count * value.price;
				});
			});
			total += $scope.menus.menu_complex.count * $scope.menus.menu_complex.price;
			return total;
		};

		// содержимое корзины


		function items_cart() {
			$scope.items = [];
			angular.forEach($scope.menus.menu, function (menuObj, index) {
				angular.forEach(menuObj.content, function (value) {
					if (value.count > 0) {
						$scope.items.push({
							id: value.name,
							count: value.count,
							idTotal: value.count * value.price
						});
					}
				});
			});
			if ($scope.menus.menu_complex.count > 0) {
				$scope.items.push({
					id: $scope.menus.menu_complex.category,
					count: $scope.menus.menu_complex.count,
					idTotal: $scope.menus.menu_complex.count * $scope.menus.menu_complex.price
				});
			}
		};
	});


}]);