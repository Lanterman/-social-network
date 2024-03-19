// comments, use websocket

const user_id = JSON.parse(document.getElementById('user_id').textContent);
const publication_id = JSON.parse(document.getElementById('publication_id').textContent);
const commentsSocket = new WebSocket('ws://' + window.location.host + '/ws/publication/' + publication_id + '/comments/');



// WS methods
commentsSocket.onopen = function(e) {
    console.log("Comment socket opened!");
};

commentsSocket.onclose = function(e) {
    console.error('Comments socket closed unexpectedly');
};

commentsSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);

    if (data.type == 'like_activity') {
        const html_comment = document.querySelector(`.com_like_${data.data.comment_id}`);
        html_comment.innerHTML = `<i class="fas fa-heart"></i> ${data.data.likes_count}`;
        data.data.like_from_me ? 
            html_comment.style.color = "red" : 
            html_comment.style.color = "blue";

    }else if (data["type"] === "send_comment") {
        // remove 'no comments' if it exists
        document.querySelector('#no-comments')?.remove();

        // add a new comment
        const comments_html = document.querySelector('#comments');        
        comments_html.innerHTML = drawComments(data.comment) + comments_html.innerHTML;
    };
};


// onmessage function
function drawComments(comment) {
    return (`
        <div>
            <p class="p4"><a href="${comment.users.url}">${comment.users.username}</a> Just</p>
            <p id="p2"><i>${comment.biography}</i></p>
            <p id="p3">
                <a class="like_comment"  title="Лайки" onclick="action_with_like(${comment.id})">
                    <span class="com_like_${comment.id}"><i class="fas fa-heart"></i> 0</span>
                </a>
            </p>
        </div>
`);
};


// events
function action_with_like(comment_id) {
    if (!user_id) {
        window.location.pathname = '/users/login/';
    } else {
        commentsSocket.send(JSON.stringify({
            'event_type': 'like_comment',
            'comment_id': comment_id,
        }));
    };
};

function create_comment() {
    if (!user_id) {
        window.location.pathname = '/users/login/';

    } else {
        const message = document.querySelector("#comment_input");
        message.reportValidity()

        if (message.value) {
            commentsSocket.send(JSON.stringify({
                'event_type': 'send_comment',
                'user_id': user_id,
                'comment_value': message.value,
                'publication_id': publication_id,
            }));

            message.value = '';
        };
    };
};
