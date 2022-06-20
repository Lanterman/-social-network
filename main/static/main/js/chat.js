// chat, use websocket

const chat_id = JSON.parse(document.getElementById('chat_id').textContent);
const user_pk = JSON.parse(document.getElementById('user_pk').textContent);
const chatSocket = new WebSocket('ws://' + window.location.host + '/ws/messages/chat/' + chat_id + '/');

document.querySelector('#chat-message-input').focus();

chatSocket.onopen = function(e) {
    console.log("Ok");
    chatSocket.send(JSON.stringify({
        'chat_id': chat_id,
        'user_pk': user_pk,
    }));
};

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    let all_messages = document.querySelector('.messages');
    const no_messages = document.querySelector('.no_messages');
    if (data.message_info != "connect") {
        if (no_messages) {
            no_messages.remove();
        };
        let mes_html = `<div class="unreaded"><input type="hidden" value="${data.user_id}">
                            <a href="${data.message_info.author_url}">
                                <img class="avatar" src="${data.message_info.author_photo}">
                            </a>
                            <div class="reply-body">
                                <strong>
                                    <a class="username" href="${data.message_info.author_url}">
                                        ${data.message_info.author_name}
                                    </a>
                                </strong>
                                 <span class="pub_date">Только что</span>
                                 <p class="text">${data.message_info.message}</p>
                            </div>
                        </div>`;
        all_messages.innerHTML += mes_html;
    };
    let messages = document.querySelectorAll(".unreaded")
    for (let message of messages) {
        if (message.firstChild.value != data.user_id) {
            message.style.backgroundColor = "#FFFFF0";
        };
    }
};

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

document.querySelector('#chat-message-submit').onclick = function(e) {
    const html_message = document.querySelector('#chat-message-input');
    html_message.reportValidity()
    if (html_message.value) {
        chatSocket.send(JSON.stringify({
            'message': html_message.value,
            'chat_id': chat_id,
            'user_pk': user_pk,
        }));
    };
    html_message.value = '';
};
