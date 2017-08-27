import notificationMixin from './notification';
import topicFormMixin from './topicForm';
import topicMixin from './topic';
import forumMixin from './forum';
import commentMixim from './comment';

//Get params from server
try{
    var user_auth = user_auth_musette['user_auth'];
}catch(e) {
    var user_auth = null;
}

//Base musette Methods
const MusetteApp = Vue.extend({
    methods: {
        //Get data for connection to websockets
        getDataConnectionWs: () => {
            let protocol;
            if (window.location.protocol === "https:") {
                protocol = "wss:";
            } else {
                protocol = "ws:";
            }

            let url = protocol + "//" + window.location.hostname + ":8000/ws/";

            return {
                'url': url,
                'user_auth': user_auth
            }
        },
        //Execute the loading ajax.gif
        loading: () => {
            $("#loading-img").removeAttr('class');
        }
    }
});

//Base app
const vm = new MusetteApp({
    el: '#app-musette',
    mixins: [notificationMixin, topicFormMixin, topicMixin, forumMixin, commentMixim]
});

window.vm = vm;