//Forum controller
const forumMixin = {
    data: {
        search_text: '',
    },
    methods: {
        search(category, forum) {
            // Function that redirect to url for search topic of one forum
            let search = this.search_text;
            window.location = "/search_topic/" + category + "/" + forum + "/?q=" + search;
        }
    }
};

export default forumMixin;