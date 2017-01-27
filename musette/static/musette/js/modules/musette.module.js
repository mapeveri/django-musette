(function() {
    'use strict';
    //Get params from server
    try{
        var params = JSON.parse($('#musette_module_js').html());
        var user_auth = params.user_auth;
    }catch(e) {
        var user_auth = null;
    }
    
    //Base musette Methods
    var MusetteApp = Vue.extend({
        methods: {
            //Connection to websockets
            connectionWs: function (is_user, id) {
                var protocol;
                if (window.location.protocol === "https:") {
                    protocol = "wss:";
                } else {
                    protocol = "ws:";
                }

                if(is_user) {
                    var url = protocol + "//" + window.location.hostname + ":8888/ws/?user=" + user_auth;
                } else {
                    var url = protocol + "//" + window.location.hostname + ":8888/ws/?topic=" + id;
                }
                return new WebSocket(url);
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
            search: function(category, forum) {
                // Function that redirect to url for search topic of one forum
                var search = this.search_text;
                window.location = "/search_topic/" + category + "/" + forum + "/?q=" + search;
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
        methods: {
            //Like comment
            like_comment: function(idcomment) {
                var csrf_token = $("[name='csrfmiddlewaretoken']").first().val();
                var params = {
                    "idcomment": idcomment, is_like: 1, 
                    csrfmiddlewaretoken: csrf_token
                };

                $.ajax({
                    url : "/like_unlike_comment/",
                    type: "POST",
                    data : params,
                    success: function( data ){
                        var total = parseInt($("#like_comment_button_" + idcomment).find("span").text()) + 1;
                        $("#like_comment_button_" + idcomment).find("span").text(total);
                        $("#unlike_comment_button_" + idcomment).find("span").text(total);

                        $("#like_comment_button_" + idcomment).hide();
                        $("#unlike_comment_button_" + idcomment).show();
                    },
                    error: function (xhr, ajaxOptions, thrownError) {
                        toastr.error("Error");
                    }
                });
            },
            //Un-Like comment
            unlike_comment: function(idcomment) {
                var csrf_token = $("[name='csrfmiddlewaretoken']").first().val();
                var params = {
                    "idcomment": idcomment, is_like: 0, 
                    csrfmiddlewaretoken: csrf_token
                };

                $.ajax({
                    url : "/like_unlike_comment/",
                    type: "POST",
                    data : params,
                    success: function( data ){
                        var total = parseInt($("#unlike_comment_button_" + idcomment).find("span").text()) - 1;
                        $("#unlike_comment_button_" + idcomment).find("span").text(total);
                        $("#like_comment_button_" + idcomment).find("span").text(total);

                        $("#unlike_comment_button_" + idcomment).hide();
                        $("#like_comment_button_" + idcomment).show();
                    },
                    error: function (xhr, ajaxOptions, thrownError) {
                        toastr.error("Error");
                    }
                });
            },
        }
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

            //Check if is a topic
            var idtopic = parseInt($("#topic_musette").val());
            if (!isNaN(idtopic)) {
                //Connection to websockets
                var ws = this.connectionWs(false, idtopic);
                ws.onmessage = function (evt) {
                    //Only add message when scroll end
                    var length = $("a.endless_more").length;
                    if (length == 0) {
                        var json = evt.data;
                        var obj = JSON.parse(json);
                        //Add new comment to model
                        $that.comments_socket.push(obj);

                        //Add new total comment
                        var total = parseInt($("#total_comments_topic").text()) + 1;
                        $("#total_comments_topic").text(total);
                    }
                };    
            }
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
            delete_topic: function(category, forum, idtopic) {
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
                            window.location.href = "/forum/" + category + "/" + forum;
                        }else {
                            toastr.error("Error");
                        }
                    },
                    error: function (xhr, ajaxOptions, thrownError) {
                        toastr.error("Error");
                    }
                });
            },
            //Like topic
            like_topic: function(idtopic) {
                var csrf_token = $("[name='csrfmiddlewaretoken']").first().val();
                var params = {
                    "idtopic": idtopic, is_like: 1, 
                    csrfmiddlewaretoken: csrf_token
                };

                $.ajax({
                    url : "/like_unlike_topic/",
                    type: "POST",
                    data : params,
                    success: function( data ){
                        var total = parseInt($("#like_topic_button").find("span").text()) + 1;
                        $("#like_topic_button").find("span").text(total);
                        $("#unlike_topic_button").find("span").text(total);

                        $("#like_topic_button").hide();
                        $("#unlike_topic_button").show();
                    },
                    error: function (xhr, ajaxOptions, thrownError) {
                        toastr.error("Error");
                    }
                });
            },
            //Un-Like topic
            unlike_topic: function(idtopic) {
                var csrf_token = $("[name='csrfmiddlewaretoken']").first().val();
                var params = {
                    "idtopic": idtopic, is_like: 0, 
                    csrfmiddlewaretoken: csrf_token
                };

                $.ajax({
                    url : "/like_unlike_topic/",
                    type: "POST",
                    data : params,
                    success: function( data ){
                        var total = parseInt($("#unlike_topic_button").find("span").text()) - 1;
                        $("#unlike_topic_button").find("span").text(total);
                        $("#like_topic_button").find("span").text(total);

                        $("#unlike_topic_button").hide();
                        $("#like_topic_button").show();
                    },
                    error: function (xhr, ajaxOptions, thrownError) {
                        toastr.error("Error");
                    }
                });
            },
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
            //Context
            var $that = this;

            //Socket for notifications
            var ws = this.connectionWs(true);
            ws.onmessage = function (evt) {
                //Get object json message
                var json = evt.data;
                var obj = JSON.parse(json);

                //Add new notification to model
                $that.notifications_socket.unshift(obj);
                $that.tot_notifications++;

                //Remove class hide
                $("#badge_notifications").text("0").removeClass("hide").html($that.tot_notifications);

                //Not notification hide
                try {
                    $("#no_notifications").addClass("hide");
                }catch(e){}
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