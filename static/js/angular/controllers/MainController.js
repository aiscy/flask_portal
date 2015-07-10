app.controller('MainController', ['$scope', 'foods', function ($scope, foods) {
	'use strict';
	foods.success(function (data) {
		$scope.menus = data;

	});
	
	
		$scope.minus = function (parentIndex, index) {
			if ($scope.menus.menu[parentIndex].content[index].count > 0) {
				//				$scope.cartform.$setDirty();
				$scope.menus.menu[parentIndex].content[index].count--;
			}
		};
		$scope.plus = function (parentIndex, index) {
			//			$scope.cartform.$setDirty();
			$scope.menus.menu[parentIndex].content[index].count++;
		};
		$scope.complexMinus = function () {
			if ($scope.menus.menu_complex.count > 0) {
				$scope.menus.menu_complex.count--;
			}
		};
		$scope.complexPlus = function () {
			$scope.menus.menu_complex.count++;
		};

	// подсчет итоговой суммы

	$scope.total = function () {
		var total = 0;
		angular.forEach($scope.menus.menu, function (menuObj,index) {
			angular.forEach(menuObj.content, function (value) {
				total += value.count * value.price;
			});
		});
		console.log($scope.menus)
		total += $scope.menus.menu_complex.count * $scope.menus.menu_complex.price;
		return total;
	};

	// содержимое корзины

	$scope.items_cart = function () {
		var items = [];
		angular.forEach($scope.menus.menu, function (menuObj, index) {
			angular.forEach(menuObj.content, function (value) {
				if (value.count > 0) {
					items.push({
						id: value.name,
						count: value.count,
						idTotal: value.count * value.price
					});
				}
			});
		});
		if ($scope.menus.menu_complex.count > 0) {
			items.push({
				id: $scope.menus.menu_complex.category,
				count: $scope.menus.menu_complex.count,
				idTotal: $scope.menus.menu_complex.count * $scope.menus.menu_complex.price
			});
		}
		return items;
	};
}]);