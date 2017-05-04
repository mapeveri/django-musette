//Topic controller
const topicMixin = {
    data: {
        //Topod id for web socket
        topic_id_ws: 0,
        //Comments array for websockets
        comments_socket: [],
    },
    mounted() {
        //Context
        let $that = this;

        setTimeout(() => {
            //For manipulate the model description in new and edit topic
            try{
                let el = tinyMCE.get('id_description');
                if (typeof (el) !== "undefined") {
                    el.on('keyup', (e) => {
                        let content = el.getContent();
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
        let idtopic = parseInt($("#topic_musette").val());
        if (!isNaN(idtopic)) {
            //Connection to websockets
            let ws = this.connectionWs(false, idtopic);
            ws.onmessage = (evt) => {
                //Only add message when scroll end
                let length = $("a.endless_more").length;
                if (length == 0) {
                    let json = evt.data;
                    let obj = JSON.parse(json);
                    //Add new comment to model
                    $that.comments_socket.push(obj);

                    //Add new total comment
                    let total = parseInt($("#total_comments_topic").text()) + 1;
                    $("#total_comments_topic").text(total);
                }
            };    
        }
    },
    methods: {
        //Open a topic close
        open_topic(idtopic, userid) {
            let csrf_token = $("[name='csrfmiddlewaretoken']").first().val();
            let params = {
                "idtopic": idtopic, "userid": userid, is_close: 0, 
                csrfmiddlewaretoken: csrf_token
            };

            $.ajax({
                url : "/open_close_topic/",
                type: "POST",
                data : params,
                success: (data) => {
                    $("#close_topic").hide("slow");
                    $("#close_topic_button").show("slow");
                    $("#open_topic_button").hide("slow");
                },
                error: (xhr, ajaxOptions, thrownError) => {
                    toastr.error("Error");
                }
            });
        },
        //Close a topic
        close_topic(idtopic, userid) {
            let csrf_token = $("[name='csrfmiddlewaretoken']").first().val();
            let params = {
                "idtopic": idtopic, "userid": userid, is_close: 1, 
                csrfmiddlewaretoken: csrf_token
            };

            $.ajax({
                url : "/open_close_topic/",
                type: "POST",
                data : params,
                success: ( data ) => {
                    $("#close_topic").show("slow");
                    $("#open_topic_button").show("slow");
                    $("#close_topic_button").hide("slow");
                },
                error: (xhr, ajaxOptions, thrownError) => {
                    toastr.error("Error");
                }
            });
        },
        //Delete a topic
        delete_topic(category, forum, idtopic) {
            let csrf_token = $("[name='csrfmiddlewaretoken']").first().val();
            let params = {
                "idtopic": idtopic, "forum": forum, 
                csrfmiddlewaretoken: csrf_token
            };

            $.ajax({
                url : "/delete_topic/",
                type: "DELETE",
                data : params,
                success: (data, statusText, xhr) => {
                    let status = parseInt(xhr.status);
                    if(status==200) {
                        window.location.href = "/forum/" + category + "/" + forum;
                    }else {
                        toastr.error("Error");
                    }
                },
                error: (xhr, ajaxOptions, thrownError) => {
                    toastr.error("Error");
                }
            });
        },
        //Like topic
        like_topic(idtopic) {
            let csrf_token = $("[name='csrfmiddlewaretoken']").first().val();
            let params = {
                "idtopic": idtopic, is_like: 1, 
                csrfmiddlewaretoken: csrf_token
            };

            $.ajax({
                url : "/like_unlike_topic/",
                type: "POST",
                data : params,
                success: (data, textStatus, xhr) => {
                    if (xhr.status == 200) {
                        let total = parseInt($("#like_topic_button").find("span").text()) + 1;
                        $("#like_topic_button").find("span").text(total);
                        $("#unlike_topic_button").find("span").text(total);

                        $("#like_topic_button").hide();
                        $("#unlike_topic_button").show();
                    }
                },
                error: (xhr, ajaxOptions, thrownError) => {
                    toastr.error("Error");
                }
            });
        },
        //Un-Like topic
        unlike_topic(idtopic) {
            let csrf_token = $("[name='csrfmiddlewaretoken']").first().val();
            let params = {
                "idtopic": idtopic, is_like: 0, 
                csrfmiddlewaretoken: csrf_token
            };

            $.ajax({
                url : "/like_unlike_topic/",
                type: "POST",
                data : params,
                success: (data, textStatus, xhr) => {
                    if (xhr.status == 200) {
                        let total = parseInt($("#unlike_topic_button").find("span").text()) - 1;
                        $("#unlike_topic_button").find("span").text(total);
                        $("#like_topic_button").find("span").text(total);

                        $("#unlike_topic_button").hide();
                        $("#like_topic_button").show();
                    }
                },
                error: (xhr, ajaxOptions, thrownError) => {
                    toastr.error("Error");
                }
            });
        },
    }
};

export default topicMixin;