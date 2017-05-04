//Topic Form controller
const topicFormMixin = {
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
    },
    watch: {
        title() {
            //Field title is touch
            this.touchTitle = true;
        },
        description() {
            //Field description is touch
            this.touchDescription = true
        }
    }
};

export default topicFormMixin;