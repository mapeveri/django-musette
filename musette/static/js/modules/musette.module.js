(function() {
    'use strict';
    angular.module('MusetteApp', [])
        .filter('htmlToPlaintext', function() {
            return function(text) {
              return String(text).replace(/<[^>]+>/gm, '');
            };
        })
        .directive('ngEnter', function () {
            return function (scope, element, attrs) {
                element.bind("keydown keypress", function (event) {
                    if(event.which === 13) {
                        scope.$apply(function () {
                            scope.$eval(attrs.ngEnter);
                        });

                        event.preventDefault();
                    }
                });
            };
        })
        .factory('ConnWS',function() {
            return {
                connectionWs: function(url) {
                    var protocol;
                    if (window.location.protocol === "https:") {
                        protocol = "wss:";
                    } else {
                        protocol = "ws:";
                    }
                    return new WebSocket(protocol + "//" + window.location.host + "/ws/");
                }
            }
        })
        .controller("TopicController", function ($scope, $http, ConnWS) {
            //For csrf forms
            $http.defaults.xsrfHeaderName = 'X-CSRFToken';
            $http.defaults.xsrfCookieName = 'csrftoken';

            $scope.comments_socket = [];

            //For manipulate the model description
            window.onload = function () {
                var el = tinyMCE.get('id_description');
                if(typeof(el) !== "undefined") {
                    el.on('keyup',function(e){
                        var content = el.getContent();
                        if(!content) {
                            $scope.$apply(function() {
                              $scope.description = "";
                            });
                        }else {
                            $scope.$apply(function() {
                              $scope.description = content;
                            });
                        }
                    });
                }
            };

            //Execute the loading ajax.gif
            $scope.loading = function() {
                angular.element(document.querySelector(".hide")).removeAttr('class');
            }

            /**
            * Open topic 
            */
            $scope.open_topic = function(idtopic, userid) {
                $http({method: "POST",
                       url: '/open_close_topic/',
                       data: $.param({"idtopic": idtopic, "userid": userid, is_close: 0}),
                       headers: {'Content-Type': 'application/x-www-form-urlencoded'}
                    })
                .success(function(data, status, headers, config) {
                    if(status == 200) {
                        angular.element(document.querySelector("#close_topic")).hide("slow");
                        angular.element(document.querySelector("#close_topic_button")).show("slow");
                        angular.element(document.querySelector("#open_topic_button")).hide("slow");
                    } else {
                        toastr.error("Error");
                    }
                })
                .error(function(data, status, headers, config) {
                    console.log("Error.");
                });
            }

            /**
            * Close topic 
            */
            $scope.close_topic = function(idtopic, userid) {
                $http({method: "POST",
                       url: '/open_close_topic/',
                       data: $.param({"idtopic": idtopic, "userid": userid, is_close: 1}),
                       headers: {'Content-Type': 'application/x-www-form-urlencoded'}
                    })
                .success(function(data, status, headers, config) {
                    if(status == 200) {
                        angular.element(document.querySelector("#close_topic")).show("slow");
                        angular.element(document.querySelector("#open_topic_button")).show("slow");
                        angular.element(document.querySelector("#close_topic_button")).hide("slow");
                    } else {
                        toastr.error("Error");
                    }
                })
                .error(function(data, status, headers, config) {
                    console.log("Error.");
                });
            }

            var ws = ConnWS.connectionWs();
            ws.onmessage = function (evt) {

                $scope.topic_id_ws = parseInt(angular.element(document.querySelector("#topic_musette")).val());

                //Only add message when scroll end
                var length = angular.element("a.endless_more").length;
                if(length == 0) {
                    var json = evt.data;
                    var obj = angular.fromJson(json);
                    var idtopic = parseInt(obj.idtopic);

                    //Verify if the message is of topic
                    if (idtopic == $scope.topic_id_ws) {
                        $scope.$apply(function() {
                            $scope.comments_socket.push(obj);
                        });
                    }
                }
            };

        })
        //Topics of forum controlller
        .controller("ForumTopicController", function($scope) {
            // Function that redirect to url for search topic of one forum
            $scope.search = function(forum) {
                var search = $scope.search_text;
                window.location = "/search_topic/" + forum + "/?q=" + search;
            }
        })
        //Notification controller
        .controller("NotificationController", function($scope, $http, ConnWS) {
            $scope.notifications_socket = [];
            $scope.user = parseInt(angular.element(document.querySelector("#user_musette")).val());
            $scope.tot_notifications = 0;

            //Set in true all notifications
            $scope.view_all = function() {
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
                if (lista_us.indexOf($scope.user) > -1) {
                    $scope.notifications_socket.unshift(obj);
                    $scope.tot_notifications++;

                    //Remove class hide
                    angular.element(document.querySelector("#badge_notifications")).removeClass("hide").html($scope.tot_notifications);

                    //Not notification hide
                    try {
                        angular.element(document.querySelector("#no_notifications")).addClass("hide");
                    }catch(e){}
                }
            };
        });
})();
