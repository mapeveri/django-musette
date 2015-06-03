
var forum = {

	//Setea en trua las notificationes para
    //un usuario del foro
    set_notifications: function() {

        $.ajax({
            url : '/forum_set_notifications/',
            type : 'GET',
            success: function (data){
                $("#badge_notifications").text("0");
            },
            error: function(XMLHttpRequest, textStatus, errorThrown) {
                console.log("Error: " + errorThrown);
            }
        });
    },

 };

 $("#notifications_dropdown").on('click', function(){
    forum.set_notifications();
})