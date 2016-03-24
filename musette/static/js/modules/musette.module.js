(function(){
	'use strict';
	angular.module('MusetteApp', ['EndlessPagination'])
		.filter('htmlToPlaintext', function() {
		    return function(text) {
		      return String(text).replace(/<[^>]+>/gm, '');
		    };
		})
		.directive('ngEnter', function () {
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
		})
		.factory('ConnWS',function(){
		    return {
		        connectionWs: function(url){
		            return new WebSocket("ws://127.0.0.1:8888/ws/");
		        }
		    }
		})
		.controller("TopicController", function ($scope, ConnWS) {

			$scope.comments_socket = [];

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

			var ws = ConnWS.connectionWs();
			ws.onmessage = function (evt){

				$scope.topic_id_ws = parseInt(angular.element(document.querySelector("#topic_musette")).val());

				//Only add message when scroll end
				var length = angular.element("a.endless_more").length;
				if(length == 0){
					var json = evt.data;
				    var obj = angular.fromJson(json);
				    var idtopic = parseInt(obj.idtopic);

				    //Verify if the message is of topic
				    if (idtopic == $scope.topic_id_ws){
				    	$scope.$apply(function(){
				    		$scope.comments_socket.push(obj);
				    	});
				    }
			    }
			};

		})
		//Topics of forum controlller
		.controller("ForumTopicController", function ($scope) {
			// Function that redirect to url for search topic of one forum
			$scope.search = function(forum){
				var search = $scope.search_text;
				window.location = "/search_topic/" + forum + "/?q=" + search;
			}
		})
		//Notification controller
		.controller("NotificationController", function ($scope, $http, ConnWS) {
			$scope.notifications_socket = [];
			$scope.user = parseInt(angular.element(document.querySelector("#user_musette")).val());
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
			var ws = ConnWS.connectionWs();

			ws.onmessage = function (evt) {
			    var json = evt.data;
			    var obj = angular.fromJson(json);
			    var lista_us = obj.lista_us;

			    //Verify if the message belongs to me
			    if (lista_us.indexOf($scope.user) > -1){
		    		$scope.notifications_socket.unshift(obj);
		    		$scope.tot_notifications++;

		    		//Remove class hide
		    		angular.element(document.querySelector("#badge_notifications")).removeClass("hide").html($scope.tot_notifications);

		    		//Not notification hide
		    		try{
		    			angular.element(document.querySelector("#no_notifications")).addClass("hide");
		    		}catch(e){}
			    }
			};
		});
})();
