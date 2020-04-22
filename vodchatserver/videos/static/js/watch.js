function initCommentFeed(commentFeedTemplate) {
    
    Vue.component('comment-feed', {

        data: function() {
            return {
                activeComments: [],
                comments: [],
                nextCommentIndex: 0,
                nextComment: null,
                numTopComments: 3,
                numBottomComments: 3,
                mouseOverComments: false,
                votes: [],
                username: username,
                video: video,
                video_id: video_id,
                ws: new WebSocket('ws://' + window.location.host + '/ws/feed/' + video_id + '/'),
                commentPlaceholder: `Commenting as ${username}...`
            };
        },

        computed: {
            activeComments: function() {
                return this.activeComments;
            },
            topComments: function() {
                const votes = this.comments.map(comment => comment);
                return votes.filter(comment => comment.upvotes > 0)
                    .sort((a, b) => (b.upvotes - b.downvotes) - (a.upvotes - a.downvotes))
                    .slice(0, this.numTopComments)
                    .map((comment, i) => { 
                        return {
                            comment: comment,
                            rank: i + 1
                        } 
                    });
            }
        },

        template: commentFeedTemplate,

        beforeMount: function() {
            let el = this;

            fetch("/videos/comment?video_id=" + el.video_id)
                .then(res => res.json())
                .then(json => json['comments'])
                .then(comments => {
                    console.log(comments);
                    el.comments = comments;
                    if (el.comments && el.comments.length > 0) {
                        el.nextComment = comments[0];
                    }
            });

            el.ws.onmessage = function(e) {
                const data = JSON.parse(e.data);
                const message = data['message'];
                const messageType = message['type'];
                switch(messageType) {
                    case "NEW_COMMENT":
                        el.newComment(message['comment']);
                        break;
                    case "UPVOTE":
                        el.upvote(message['comment_id']);
                        break;
                    case "DOWNVOTE":
                        el.downvote(message['comment_id']);
                        break;
                    default:
                        break;
                }
            };

            el.ws.onclose = function(e) {
                console.log("disconnected...");
            };

            el.video.ontimeupdate = function(event) {
                console.log("NEW TIME!");
                while (el.comments[el.nextCommentIndex] && el.comments[el.nextCommentIndex].timestamp <= el.video.currentTime) {
                    el.activeComments.push(el.comments[el.nextCommentIndex]);
                    el.nextCommentIndex++;
                }

                if (!el.mouseOverComments) {
                    el.$refs.comments.scrollTop = el.$refs.comments.scrollHeight;
                }
            };
        },

        methods: {

            toMMSS: function (timestamp) {
                    var sec_num = Math.trunc(timestamp); // don't forget the second param
                    var hours   = Math.floor(sec_num / 3600);
                    var minutes = Math.floor((sec_num - (hours * 3600)) / 60);
                    var seconds = sec_num - (hours * 3600) - (minutes * 60);

                    if (hours   < 10) {hours   = "0"+hours;}
                    if (minutes < 10) {minutes = "0"+minutes;}
                    if (seconds < 10) {seconds = "0"+seconds;}
                return minutes + ':' + seconds;
            },

            setMouseOverComments: function(trueOrFalse) {
                let el = this;
                el.mouseOverComments = trueOrFalse;
            },

            newComment: function(comment) {
                console.log("new comment!")
                console.log(comment);
                let el = this;

                el.comments.push(comment);
                el.comments.sort((a, b) => a.timestamp - b.timestamp);
            },

            upvote: function(commentId) {
                let el = this;
                el.comments.forEach(comment => {
                    if (comment.id === commentId) {
                        comment.upvotes++;
                    }
                });
            },

            downvote: function(commentId) {
                console.log("downvote!");
                let el = this;
                el.comments.forEach(comment => {
                    if (comment.id === commentId) {
                        comment.downvotes++;
                    }
                });
            },

            doUpvote: function(commentId, videoId) {
                this.submitVote(commentId, videoId, 1);
            },

            doDownvote: function(commentId, videoId) {
                this.submitVote(commentId, videoId, -1);
            },

            submitVote: function(commentId, videoId, vote) {
                let el = this;
                let form = el.$refs.voteForm;

                let formData = new FormData(form);
                formData.set("comment_id", commentId);
                formData.set("video_id", videoId);
                formData.set("vote", vote);

                fetch(form.action, {
                    method: form.method,
                    body: formData
                });
            },

            submit: function(e) {
                let el = this;
                e.preventDefault();
                let form = el.$refs.form;

                form.elements["timestamp"].value = el.video.currentTime;

                fetch(form.action, {
                    method: form.method,
                    body: new FormData(form)
                });

                form.text.value = "";
            },

            checkTop(id) {
                return topComments.filter(comment => comment.id === id).length > 0;
            },

            checkBottom(id) {
                return bottomComments.filter(comment => comment.id === id).length > 0;
            }
        }
    });

    new Vue({
        el: "#commentFeedContainer"
    });

}