// comments, use websocket

const publish_slug = JSON.parse(document.getElementById('publish_slug').textContent);
const publish_id = JSON.parse(document.getElementById('publish_id').textContent);
const user_id = JSON.parse(document.getElementById('user_id').textContent);
const commentsSocket = new WebSocket('ws://' + window.location.host + '/ws/publish/' + publish_slug + '/comments/');

commentsSocket.onopen = function(e) {
    console.log("Ok");
};

commentsSocket.onclose = function(e) {
    console.error('Comments socket closed unexpectedly');
};

commentsSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    if (data.action_type == 'action_like') {
        const html_comment = document.querySelector(`.com_like_${data.likes_info.comment_id}`);
        html_comment.innerHTML = `<i class="fas fa-heart"></i> ${data.likes_info.likes_count}`;
        if (data.likes_info.like_from_me) {
            html_comment.style.color = "red";
        }else{
            html_comment.style.color = "blue";
        };
    }else{
        const no_comment = document.querySelector('#p5');
        if (no_comment) {
            no_comment.remove();
        };
        const comments_html = document.querySelector('#comments');
        const all = comments_html.innerHTML;
        const comment_html = `<div>
                                <p class="p4"><a href="${data.comment_info.author_url}">${data.comment_info.author_username}</a> Только что</p>
                                <p id="p2"><i>${data.comment_info.message}</i></p>
                                <p id="p3">
                                    <a class="like_comment"  title="Лайки" onclick="action_with_like(${data.comment_info.comment_id})">
                                        <span class="com_like_${data.comment_info.comment_id}"><i class="fas fa-heart"></i> 0</span>
                                    </a>
                                </p>
                            </div>`;
        comments_html.innerHTML = comment_html;
        comments_html.innerHTML += all;
    };
};

function action_with_like(comment_id) {
    if (!user_id) {
        window.location.pathname = '/users/login/';
    }
    commentsSocket.send(JSON.stringify({
        'comment_id': comment_id,
        'type': 'like',
    }));
};

function create_comment() {
    if (!user_id) {
        window.location.pathname = '/users/login/';
    }
    const message = document.querySelector("#comment_input");
    message.reportValidity()
    if (message.value) {
        commentsSocket.send(JSON.stringify({
            'publish_id': publish_id,
            'user_id': user_id,
            'message': message.value,
            'type': 'comment',
        }));
        message.value = '';
    };
};
