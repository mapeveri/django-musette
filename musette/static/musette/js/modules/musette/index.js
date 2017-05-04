import notificationMixin from './notification';
import topicFormMixin from './topicForm';
import topicMixin from './topic';
import forumMixin from './forum';
import commentMixim from './comment';

//Get params from server
try{
    let params = JSON.parse($('#musette_module_js').html());
    var user_auth = params.user_auth;
}catch(e) {
    var user_auth = null;
}

//Base musette Methods
const MusetteApp = Vue.extend({
    methods: {
        //Connection to websockets
        connectionWs: (is_user, id) => {
            let protocol;
            if (window.location.protocol === "https:") {
                protocol = "wss:";
            } else {
                protocol = "ws:";
            }

            let url;
            if(is_user) {
                 url = protocol + "//" + window.location.hostname + ":8888/ws/?user=" + user_auth;
            } else {
                url = protocol + "//" + window.location.hostname + ":8888/ws/?topic=" + id;
            }
            return new WebSocket(url);
        },
        //Execute the loading ajax.gif
        loading: () => {
            $("#loading-img").removeAttr('class');
        }
    }
});

//Base app
new MusetteApp({
    el: '#app-musette',
    mixins: [notificationMixin, topicFormMixin, topicMixin, forumMixin, commentMixim]
});