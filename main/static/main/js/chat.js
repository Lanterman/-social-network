// chat, use websocket

const chat_id = JSON.parse(document.getElementById('chat_id').textContent);
const user_pk = JSON.parse(document.getElementById('user_pk').textContent);
const chatSocket = new WebSocket('ws://' + window.location.host + '/ws/messages/chat/' + chat_id + '/');

document.querySelector('#chat-message-input').focus();
document.querySelector('#chat-message-input').onkeyup = function(e) {
    if (e.keyCode === 13) {  // enter, return
        document.querySelector('#chat-message-submit').click();
    }
};

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    let all_messages = document.querySelector('.messages');
    let mes_html = `<div class="${data.message_info.is_readed}">
                        <a href="${data.message_info.author_url}">
                            <img class="avatar" src="${data.message_info.author_photo}">
                        </a>
                        <div class="reply-body">
                            <strong>
                                <a class="username" href="${data.message_info.author_url}">
                                    ${data.message_info.author_name}
                                </a>
                            </strong>
                             <span class="pub_date">${data.message_info.pub_date}</span>
                             <p class="text">${data.message_info.message}</p>
                        </div>
                    </div>`;
    all_messages.innerHTML += mes_html;
};

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

document.querySelector('#chat-message-submit').onclick = function(e) {
    const html_message = document.querySelector('#chat-message-input');
    const no_messages = document.querySelector('.no_messages');
    chatSocket.send(JSON.stringify({
        'message': html_message.value,
        'chat_id': chat_id,
        'user_pk': user_pk,
    }));
    if (no_messages) {
        no_messages.remove();
    }
    html_message.value = '';
};
