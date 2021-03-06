
var intervalArrayStocklist = [];
var intervalArrayAddTargetPrice = [];
var intervalArrayAddTargetAvg = [];
var wait_msec = 5000;

function check_open_time(){
    var d = new Date();
    var hours = d.getHours();
    var min = d.getMinutes();
    if( (hours >= 9 && hours <= 13) ){
        if( hours != 13 ){
            return true;
        }else{
            if( min <= 30 ){
                return true;
            }
            else{
                return false;
            }
        }
    }
    else{
        return false;
    }
}

function stopIntervalArray(intervalarray,interval){
    for(var i=0;i<intervalarray.length;i++){
        if (angular.isDefined(intervalarray[i])) {
            interval.cancel(intervalarray[i]);
            intervalarray[i] = undefined;
        }
    }
    intervalarray = []
}

var app = angular.module('myApp', []);

app.controller('topController', function($scope, $http, $interval, $timeout) {
    $scope.type = 'stocklist';

    $scope.changeType = function(type){
        $scope.type = type;
        if( check_open_time() ){
            stopIntervalArray(intervalArrayStocklist,$interval);
            stopIntervalArray(intervalArrayAddTargetPrice,$interval);
            stopIntervalArray(intervalArrayAddTargetAvg,$interval);
        }
    };

    var tick = function() {
        $scope.clock = Date.now() // get the current time
        $timeout(tick, 1000); // reset the timer
    }
    $timeout(tick, $scope.tickInterval);
});

app.controller('stocklistController', function($scope, $http, $interval) {
    $scope.final_price = {};

    $http.get("setting")
    .then(function(response) {
        $scope.stocklist = response.data.stocklist;
        for(var i=0;i<$scope.stocklist.length;i++){
            intervalArrayStocklist[i] = handlePrice($scope.stocklist[i],intervalArrayStocklist[i]);
            handleDiv($scope.stocklist[i]);
        }
        wait_msec = parseInt(response.data.wait_sec) * 1000;
    });

    function handlePrice(num,intervaltmp){
        if( check_open_time() ){
            if( angular.isDefined(intervaltmp) )
                return;
            intervaltmp = $interval(function(){
                $http.get("price", {params:{stockNum:num.toString()}})
                .then(function(response) {
                    $scope.final_price[num] = response.data.final_price;
                });
            },wait_msec);
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

    $scope.$on('$destroy', function() {
        // Make sure that the interval is destroyed too
        stopIntervalArray(intervalArrayStocklist,$interval);
    });
    
});

app.controller('addTargetController', function($scope, $http, $interval) {
    $scope.final_price = {};
    $scope.avg = {};
    $scope.showAvg = [];
    $scope.showAvgDelicate = [];

    $http.get("setting")
    .then(function(response) {
        $scope.config = response.data;
        for(var i=0;i<$scope.config.add_target.length;i++){
            intervalArrayAddTargetPrice[i] = handlePrice($scope.config.add_target[i].stock_number,intervalArrayAddTargetPrice[i]);
            intervalArrayAddTargetAvg[i] = handleAvg($scope.config.add_target[i].stock_number,$scope.config.add_target[i].avg_number,intervalArrayAddTargetAvg[i]);
        
            if( $scope.config.add_target[i].type == 'avg' )
                $scope.showAvg.push($scope.config.add_target[i]);
            else if( $scope.config.add_target[i].type == 'avg_delicate' )
                $scope.showAvgDelicate.push($scope.config.add_target[i]);
        }
    });

    function handlePrice(num,intervaltmp){
        if( check_open_time() ){
            if( angular.isDefined(intervaltmp) )
                return;
            intervaltmp = $interval(function(){
                $http.get("price", {params:{stockNum:num.toString()}})
                .then(function(response) {
                    $scope.final_price[num] = response.data.final_price;
                });
            },wait_msec);
        }else{
            $http.get("price", {params:{stockNum:num.toString()}})
            .then(function(response) {
                $scope.final_price[num] = response.data.final_price;
            });
        }
        return intervaltmp;
    }

    function handleAvg(num,day,intervaltmp) {
        if( check_open_time() ){
            if( angular.isDefined(intervaltmp) )
                return;
            intervaltmp = $interval(function(){
                $http.get("avg", {params:{stockNum:num.toString(),days:day.toString()}})
                .then(function(response) {
                    $scope.avg[num] = response.data.avg;
                });
            }, wait_msec);
        }else{
            $http.get("avg", {params:{stockNum:num.toString(),days:day.toString()}})
            .then(function(response) {
                $scope.avg[num] = response.data.avg;
            });
        }
        return intervaltmp;
    }

    $scope.$on('$destroy', function() {
        // Make sure that the interval is destroyed too
        stopIntervalArray(intervalArrayAddTargetPrice,$interval);
        stopIntervalArray(intervalArrayAddTargetAvg,$interval);
    });

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

    $scope.add_target_type = 'avg'
    $scope.add_target_btn = function(){
        var tmpdict = {};
        tmpdict = 
        {
            'stock_number': $scope.add_target_stock_number,
            'type': $scope.add_target_type,
            'avg_number': $scope.add_target_avg_number,
            'avg_delicate': $scope.add_target_avg_delicate
        };
        $scope.config.add_target.push(tmpdict);
    };
    $scope.add_target_del = function(index){
        //console.log("index=",index);
        $scope.config.add_target.splice(index, 1);
    };
});
