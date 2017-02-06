
function check_open_time(){
    var d = new Date();
    var hours = d.getHours();
    var min = d.getMinutes();
    if( (hours >= 9 && hours <= 13) || (hours == 13 && min <= 30) )
        return true;
    else
        return false;
}

var app = angular.module('myApp', []);

app.controller('topController', function($scope, $http, $timeout) {
    $scope.type = 'stocklist';

    $scope.changeType = function(type){
        $scope.type = type;
        if( $scope.type != "stocklist" ){
            if( check_open_time() ){
                for(var i=0;i<intervalArray.length;i++){
                   clearInterval(intervalArray[i]);
                }
            }
        }
    };
});

var intervalArray = [];
var intervaltmp;
var wait_msec = 5000;
app.controller('stocklistController', function($scope, $http, $timeout) {
    $http.get("setting")
    .then(function(response) {
        $scope.stocklist = response.data.stocklist;
        for(var i=0;i<$scope.stocklist.length;i++){
            intervalArray[i] = handlePrice($scope.stocklist[i]);
            handleDiv($scope.stocklist[i]);
        }
        wait_msec = parseInt(response.data.wait_sec) * 1000;
    });

    $scope.final_price = {};
    function handlePrice(num){
        var intervaltmp;
        if( check_open_time() ){
            intervaltmp = setInterval(function() {
                $http.get("price", {params:{stockNum:num.toString()}})
                .then(function(response) {
                    $scope.final_price[num] = response.data.final_price;
                });

                $scope.$apply() 
            }, wait_msec);
        }else{
            $http.get("price", {params:{stockNum:num.toString()}})
            .then(function(response) {
                $scope.final_price[num] = response.data.final_price;
            });
        }
        
        return intervaltmp;
    }

    $scope.perdiv = {};
    function handleDiv(num){
        $http.get("perdiv", {params:{stockNum:num.toString()}})
        .then(function(response) {
            $scope.perdiv[num] = response.data.perdiv;
        });
    }
    
});

app.controller('settingController', function($scope, $http, $timeout) {
    $http.get("setting")
    .then(function(response) {
        $scope.config = response.data;
        $scope.del_one_stock = $scope.config.stocklist[0];
    });

    $scope.add_stock_num = function(){
        $scope.config.stocklist.push($scope.add_one_stock);
        $scope.add_one_stock = '';
    };

    $scope.savestock = function(){
        //var indata = {username:'truedano'};
        $http.post("setting", $scope.config).
        then(function (data, status, headers, config) { alert("success") },
             function (data, status, headers, config) { alert("error") });
    };

    $scope.pre_del_stock_num = function(){
        $scope.del_one_stock = $('#stocklist_select').val();
    };

    $scope.del_stock_num = function(){
        Array.prototype.deleteOf = function(a) {  
            for(var i=this.length; i-- && this[i] !== a;);  
                if (i >= 0) this.splice(i,1); 
        };
        $scope.config.stocklist.deleteOf($scope.del_one_stock);
    };
});
