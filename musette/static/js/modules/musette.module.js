(function() {
    'use strict';

    //Base musette Methods
    var MusetteApp = Vue.extend({
        methods: {
            //Connection to websockets
            connectionWs: function (url) {
                var protocol;
                if (window.location.protocol === "https:") {
                    protocol = "wss:";
                } else {
                    protocol = "ws:";
                }
                return new WebSocket(protocol + "//" + window.location.hostname + ":8888/ws/");
            },
            //Execute the loading ajax.gif
            loading: function() {
                $("#loading-img").removeAttr('class');
            }
        }
    });

    //Forum controller
    var forumMixin = {
        data: {
            search_text: '',
        },
        methods: {
            search: function(forum) {
                // Function that redirect to url for search topic of one forum
                var search = this.search_text;
                window.location = "/search_topic/" + forum + "/?q=" + search;
            }
        }
    };
    
    //Topic Form controller
    var topicFormMixin = {
        data() {
            return window.__FORM__ || {
                //Title model form add/edit topic
                title: '',
                //Touch title model form add/edit topic
                touchTitle: false,
                //Description model form add/edit topic
                description: '',
                //Touch description model form add/edit topic
                touchDescription: false,
            }
        },
        mounted () {
            //Context
            var $that = this;

            setTimeout(function() {
                //For manipulate the model description in new and edit topic
                try{
                    var el = tinyMCE.get('id_description');
                    if (typeof (el) !== "undefined") {
                        el.on('keyup', function (e) {
                            var content = el.getContent();
                            if (!content) {
                                $that.description = "";
                            } else {
                                $that.description = content;
                            }
                        });
                    }
                } catch(e) {}
            }, 1000);
        },
        watch: {
            title: function() {
                //Field title is touch
                this.touchTitle = true;
            },
            description: function() {
                //Field description is touch
                this.touchDescription = true
            }
        }
    };
     
    //Comment forms controller
    var commentMixim = {
        data() {
            return window.__FORM__ || {
                description: '',
                descrip_comments: [],
            }
        },
    };

    //Topic controller
    var topicMixin = {
        data: {
            //Topod id for web socket
            topic_id_ws: 0,
            //Comments array for websockets
            comments_socket: [],
        },
        mounted () {
            //Context
            var $that = this;

            setTimeout(function() {
                //For manipulate the model description in new and edit topic
                try{
                    var el = tinyMCE.get('id_description');
                    if (typeof (el) !== "undefined") {
                        el.on('keyup', function (e) {
                            var content = el.getContent();
                            if (!content) {
                                $that.description = "";
                            } else {
                                $that.description = content;
                            }
                        });
                    }
                } catch(e) {} 
            }, 1000);

            //Connection to websockets
            var ws = this.connectionWs();
            ws.onmessage = function (evt) {
                $that.topic_id_ws = parseInt($("#topic_musette").val());

                //Only add message when scroll end
                var length = $("a.endless_more").length;
                if (length == 0) {
                    var json = evt.data;
                    var obj = JSON.parse(json);
                    var idtopic = parseInt(obj.idtopic);

                    //Verify if the message is of topic
                    if (idtopic == $that.topic_id_ws) {
                        $that.comments_socket.push(obj);
                    }
                }
            };
        },
        methods: {
            //Open a topic close
            open_topic: function(idtopic, userid) {
                var csrf_token = $("[name='csrfmiddlewaretoken']").first().val();
                var params = {
                    "idtopic": idtopic, "userid": userid, is_close: 0, 
                    csrfmiddlewaretoken: csrf_token
                };

                $.ajax({
                    url : "/open_close_topic/",
                    type: "POST",
                    data : params,
                    success: function( data ){
                        $("#close_topic").hide("slow");
                        $("#close_topic_button").show("slow");
                        $("#open_topic_button").hide("slow");
                    },
                    error: function (xhr, ajaxOptions, thrownError) {
                        toastr.error("Error");
                    }
                });
            },
            //Close a topic
            close_topic: function(idtopic, userid) {
                var csrf_token = $("[name='csrfmiddlewaretoken']").first().val();
                var params = {
                    "idtopic": idtopic, "userid": userid, is_close: 1, 
                    csrfmiddlewaretoken: csrf_token
                };

                $.ajax({
                    url : "/open_close_topic/",
                    type: "POST",
                    data : params,
                    success: function( data ){
                        $("#close_topic").show("slow");
                        $("#open_topic_button").show("slow");
                        $("#close_topic_button").hide("slow");
                    },
                    error: function (xhr, ajaxOptions, thrownError) {
                        toastr.error("Error");
                    }
                });
            },
            //Delete a topic
            delete_topic: function(forum, idtopic) {
                var csrf_token = $("[name='csrfmiddlewaretoken']").first().val();
                var params = {
                    "idtopic": idtopic, "forum": forum, 
                    csrfmiddlewaretoken: csrf_token
                };

                $.ajax({
                    url : "/delete_topic/",
                    type: "DELETE",
                    data : params,
                    success: function( data, statusText, xhr){
                        var status = parseInt(xhr.status);
                        if(status==200) {
                            window.location.href = "/forum/" + forum;
                        }else {
                            toastr.error("Error");
                        }
                    },
                    error: function (xhr, ajaxOptions, thrownError) {
                        toastr.error("Error");
                    }
                });
            }
        }
    };

    //Notification controller
    var notificationMixin = {
        data: {
            user: '',
            tot_notifications: 0,
            notifications_socket: [],
        },
        mounted: function () {
            var $that = this;

            //Socket for notifications
            var ws = this.connectionWs();
            ws.onmessage = function (evt) {
                $that.user = parseInt($("#user_musette").val());

                var json = evt.data;
                var obj = JSON.parse(json);
                var lista_us = obj.lista_us;

                //Verify if the message belongs to me
                if (lista_us.indexOf($that.user) > -1) {
                    $that.notifications_socket.unshift(obj);
                    $that.tot_notifications++;

                    //Remove class hide
                    $("#badge_notifications").text("0").removeClass("hide").html($that.tot_notifications);

                    //Not notification hide
                    try {
                        $("#no_notifications").addClass("hide");
                    }catch(e){}
                }
            };
        },
        methods: {
            //Set in true all notifications
            view_all: function() {
                $.ajax({
                    url : "/forum_set_notifications/",
                    type: "GET",
                    success: function( data ){
                        $("#badge_notifications").text("0").addClass("hide");
                        this.tot_notifications = 0;
                    },
                    error: function (xhr, ajaxOptions, thrownError) {
                        toastr.error("Error");
                    }
                });
            }
        }
    };

    //Base app
    new MusetteApp({
        el: '#app-musette',
        mixins: [notificationMixin, topicFormMixin, topicMixin, forumMixin, commentMixim]
    });

})();