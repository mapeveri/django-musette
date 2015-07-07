'use strict';
var Topic = angular.module('TopicApp', []);

Topic.filter('htmlToPlaintext', function() {
    return function(text) {
      return String(text).replace(/<[^>]+>/gm, '');
    };
});

Topic.directive('ngEnter', function () {
    return function (scope, element, attrs) {
        element.bind("keydown keypress", function (event) {
            if(event.which === 13) {
                scope.$apply(function (){
                    scope.$eval(attrs.ngEnter);
                });

                event.preventDefault();
            }
        });
    };
});

Topic.controller("TopicController", function ($scope) {

	//For manipulate the model description
	window.onload = function () {

		tinyMCE.get('id_description').onKeyUp.add(function(ed, l) {

			var content = tinyMCE.get('id_description').getContent();
			if(!content){
				$scope.$apply(function(){
				  $scope.description = "";
				});

			}else{
				$scope.$apply(function(){
				  $scope.description = content;
				});
			}

		});

	};

	//Execute the loading ajax.gif
	$scope.loading = function(){

		angular.element(document.querySelector(".hide")).removeAttr('class');

	}



});


//Topics of forum controlller
Topic.controller("ForumTopicController", function ($scope) {

	// Function that redirect to url for search topic of one forum
	$scope.search = function(forum){

		var search = $scope.search_text;
		window.location = "/search_topic/" + forum + "/?q=" + search;

	}

});

//Notification controller
Topic.controller("NotificationController", function ($scope, $http) {

	$scope.notifications_socket = [];
	$scope.user = parseInt(angular.element(document.querySelector("#user_musette")).val());
	$scope.arr_idnotification = [];
	$scope.arr_idobject = [];
	$scope.tot_notifications = 0;

	//Set in true all notifications
	$scope.view_all = function(){

		$http({method: "GET",
			   url: '/forum_set_notifications/',
    		   headers: {'Content-Type': 'application/x-www-form-urlencoded'}
    		})
	    .success(function(data, status, headers, config) {
	        angular.element(document.querySelector("#badge_notifications")).text("0").addClass("hide");
	        $scope.tot_notifications = 0;
	    })
	    .error(function(data, status, headers, config) {
	        console.log("Error.");
	    });

	}

	//Socket for notifications
	var ws = new WebSocket("ws://127.0.0.1:8888/ws/");

	ws.onmessage = function (evt) {
	    var json = evt.data;
	    var obj = angular.fromJson(json);
	    var lista_us = obj.lista_us;
	    var idnotification = parseInt(obj.idnotification);
	    var idobject = parseInt(obj.idobject);

	    //Verify if the message belongs to me
	    if (lista_us.indexOf($scope.user) !== -1){
	    	//Verify if notification exists previusly
	    	if ($scope.arr_idnotification.indexOf(idnotification) === -1 && $scope.arr_idobject.indexOf(idobject) === -1){
	    		$scope.notifications_socket.unshift(obj);
	    		$scope.arr_idnotification.push(idnotification);
	    		$scope.arr_idobject.push(idobject);
	    		$scope.tot_notifications++;

	    		//Remove class hide
	    		angular.element(document.querySelector("#badge_notifications")).removeClass("hide").html($scope.tot_notifications);

	    		//If not notification hide
	    		try{
	    			angular.element(document.querySelector("#no_notifications")).addClass("hide");
	    		}catch(e){}
	    	}
	    }

	};

});


