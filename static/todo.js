
var app = angular.module('myApp', []);
app.controller('myCtrl', function($scope, $http, $timeout) {
    $http.get("stocklist")
    .then(function(response) {
        $scope.stocklist = response.data.stocklist;
        for(var i=0;i<$scope.stocklist.length;i++){
            handlePrice($scope.stocklist[i]);
            handleDiv($scope.stocklist[i]);
        }
    });

    $scope.final_price = {};
    function handlePrice(num){
        setInterval(function() {
            $http.get("price", {params:{stockNum:num.toString()}})
            .then(function(response) {
                $scope.final_price[num] = response.data.final_price;
                //console.log('get :',$scope.final_price[num])
            });

            $scope.$apply() 
        }, 5000);
    }

    $scope.perdiv = {};
    function handleDiv(num){
        $http.get("perdiv", {params:{stockNum:num.toString()}})
        .then(function(response) {
            $scope.perdiv[num] = response.data.perdiv;
        });
    }
    
});
