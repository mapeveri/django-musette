//Notification controller
const notificationMixin = {
    data: {
        user: '',
        tot_notifications: 0,
        notifications_socket: [],
    },
    mounted() {
        //Context
        let $that = this;

        //Socket for notifications
        let ws = this.connectionWs(true);
        ws.onmessage = (evt) => {
            //Get object json message
            let json = evt.data;
            let obj = JSON.parse(json);

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
        view_all() {
            $.ajax({
                url : "/forum_set_notifications/",
                type: "GET",
                success: ( data ) => {
                    $("#badge_notifications").text("0").addClass("hide");
                    this.tot_notifications = 0;
                },
                error: (xhr, ajaxOptions, thrownError) => {
                    toastr.error("Error");
                }
            });
        }
    }
};

export default notificationMixin;