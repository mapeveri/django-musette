//Comment forms controller
const commentMixim = {
    data() {
        return window.__FORM__ || {
            description: '',
            descrip_comments: [],
        }
    },
    methods: {
        //Like comment
        like_comment(idcomment) {
            let csrf_token = $("[name='csrfmiddlewaretoken']").first().val();
            let params = {
                "idcomment": idcomment, is_like: 1, 
                csrfmiddlewaretoken: csrf_token
            };

            $.ajax({
                url : "/like_unlike_comment/",
                type: "POST",
                data : params,
                success: (data, textStatus, xhr) => {
                    if (xhr.status == 200) {
                        let total = parseInt($("#like_comment_button_" + idcomment).find("span").text()) + 1;
                        $("#like_comment_button_" + idcomment).find("span").text(total);
                        $("#unlike_comment_button_" + idcomment).find("span").text(total);

                        $("#like_comment_button_" + idcomment).hide();
                        $("#unlike_comment_button_" + idcomment).show();
                    }
                },
                error: (xhr, ajaxOptions, thrownError) => {
                    toastr.error("Error");
                }
            });
        },
        //Un-Like comment
        unlike_comment(idcomment) {
            let csrf_token = $("[name='csrfmiddlewaretoken']").first().val();
            let params = {
                "idcomment": idcomment, is_like: 0, 
                csrfmiddlewaretoken: csrf_token
            };

            $.ajax({
                url : "/like_unlike_comment/",
                type: "POST",
                data : params,
                success: (data, textStatus, xhr) => {
                    if (xhr.status == 200) {
                        let total = parseInt($("#unlike_comment_button_" + idcomment).find("span").text()) - 1;
                        $("#unlike_comment_button_" + idcomment).find("span").text(total);
                        $("#like_comment_button_" + idcomment).find("span").text(total);

                        $("#unlike_comment_button_" + idcomment).hide();
                        $("#like_comment_button_" + idcomment).show();
                    }
                },
                error: (xhr, ajaxOptions, thrownError) => {
                    toastr.error("Error");
                }
            });
        },
    }
};

export default commentMixim;