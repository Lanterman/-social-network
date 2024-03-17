// chat, use websocket

const chat_id = JSON.parse(document.getElementById('chat_id').textContent);
const chatSocket = new WebSocket('ws://' + window.location.host + '/ws/messages/chat/' + chat_id + '/');

document.querySelector('#chat-message-input').focus();


// WS methods
chatSocket.onopen = function(e) {
    console.log("Chat socket opened!");
};

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    console.log(data);

    if (data.type === "send_message") {
        // remove block 'no_message' if it exists
        document.querySelector('.no_messages')?.remove();

        // add new message into block 'messages'
        let all_messages = document.querySelector('.messages');
        all_messages.innerHTML += drawMessage(data.message);

        // read unread message another user(-s)
        read_message(data.message.author.id);
    };
};


// onmessage functions
function drawMessage(message) {
    return (`
        <div class="unreaded"><input type="hidden" value="${message.author.id}">
            <div class="dialogue">
                <a href="${message.author.url}">
                    ${message.author.photo ?
                        `<img class="avatar" src="${message.author.photo}">` :
                        (`<div class="photo_frame_mes_user" id="no-photo">
                            <p class="user-no-photo">No image</p>
                        </div>`)
                    }
                </a>
            </div>

            <div class="reply-body">
                <strong>
                    <a class="username" href="${message.author.url}">
                        ${message.author.name}
                    </a>
                </strong>
                <span class="pub_date">Just</span>
                <p class="text">${message.message}</p>
            </div>
        </div>
    `);
};

function read_message(author_id) {
    let messages = document.querySelectorAll(".unreaded");
        for (let message of messages) {
            if (message.firstChild.value != author_id) {
                message.style.backgroundColor = "#FFFFF0";
        };
    };
};


// events
document.querySelector('#chat-message-submit').onclick = function(e) {
    const html_message = document.querySelector('#chat-message-input');
    html_message.reportValidity()
    if (html_message.value) {
        chatSocket.send(JSON.stringify({
            'event_type': "send_message",
            'message': html_message.value,
            'chat_id': chat_id,
        }));

        const csrf_token = document.querySelector('[name=csrfmiddlewaretoken]').value;
        const request = new Request(`/chat/${chat_id}/`, {headers: {'X-CSRFToken': csrf_token}});
        let data = new FormData();
        data.append("message", html_message.value)
        fetch(request, {method: 'POST', body: data})

        html_message.value = '';
    };
};
