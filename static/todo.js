
var app = angular.module('myApp', []);
app.controller('myCtrl', function($scope, $http, $timeout) {
    $http.get("stocklist")
    .then(function(response) {
        $scope.stocklist = response.data.stocklist;
    });

    //update info and div per 5 sec
    setInterval(function() {
    	$http.get("price", {params:{stockNum:'2330'}})
    	.then(function(response) {
        	$scope.final_price = response.data.final_price;
    	});

        $scope.$apply() 
    }, 5000);
    
});
