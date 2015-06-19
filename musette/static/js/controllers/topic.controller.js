'use strict';
var Topic = angular.module('TopicApp', []);

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

//Notification controller
Topic.controller("NotificationController", function ($scope, $http) {

	//Set in true all notifications
	$scope.view_all = function(){

		$http({method: "GET",
			   url: '/forum_set_notifications/',
    		   headers: {'Content-Type': 'application/x-www-form-urlencoded'}
    		})
	    .success(function(data, status, headers, config) {
	        angular.element(document.querySelector("#badge_notifications")).text("0");
	    })
	    .error(function(data, status, headers, config) {
	        console.log("Error.");
	    });

	}

});
