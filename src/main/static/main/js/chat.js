// chat, use websocket

const chat_id = JSON.parse(document.getElementById('chat_id').textContent);
const chatSocket = new WebSocket('ws://' + window.location.host + '/ws/messages/chat/' + chat_id + '/');

document.querySelector('#chat-message-input').focus();

chatSocket.onopen = function(e) {
    console.log("Ok");
};

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    let all_messages = document.querySelector('.messages');
    if (data.message_info != "connect") {
        const no_messages = document.querySelector('.no_messages');
        if (no_messages) {
            no_messages.remove();
        };

        let mes_html = `<div class="unreaded"><input type="hidden" value="${data.user_id}">
                            <div class="dialogue">
                                <a href="${data.message_info.author_url}">
                                    ${data.message_info.author_photo ?
                                        `<img class="avatar" src="${data.message_info.author_photo}">` :
                                        '<div class="photo_frame_mes_user" id="no-photo"><p class="user-no-photo">No image</p></div>'
                                    }
                                </a>
                            </div>

                            <div class="reply-body">
                                <strong>
                                    <a class="username" href="${data.message_info.author_url}">
                                        ${data.message_info.author_name}
                                    </a>
                                </strong>
                                 <span class="pub_date">Just</span>
                                 <p class="text">${data.message_info.message}</p>
                            </div>
                        </div>`;
        all_messages.innerHTML += mes_html;
    }else {
        let messages = document.querySelectorAll(".unreaded")
        for (let message of messages) {
            if (message.firstChild.value != data.user_id) {
                message.style.backgroundColor = "#FFFFF0";
            };
        };
    };
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
        }));

        const csrf_token = document.querySelector('[name=csrfmiddlewaretoken]').value;
        const request = new Request(`/chat/${chat_id}/`, {headers: {'X-CSRFToken': csrf_token}});
        let data = new FormData();
        data.append("message", html_message.value)
        fetch(request, {method: 'POST', body: data})

        html_message.value = '';
    };
};
