// messengers page, use websocket

const messengersPageSocket = new WebSocket('ws://' + window.location.host + '/ws/messengers/');


messengersPageSocket.onopen = function(e) {
    console.log("Messengers page socket opened");
};

messengersPageSocket.onclose = function(e) {
    console.error('Messengers page socket closed unexpectedly');
};

messengersPageSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);

    if (data["event_type"] === "search") {
        const messengersBlock = document.getElementsByClassName("messengersBlock")[0];
        messengersBlock.innerHTML = "";
        
        if (data["chats"].length) {
            responseToSearch(data["user_id"], data["chats"], messengersBlock);
        } else {
            noResponseToSearch(messengersBlock);
        };
    };
};


// event types logic of onmessage
function responseToSearch(user_id, chats, messengersBlock) {
    Object.values(chats).forEach((chat) => {
        messengersBlock.innerHTML += drawChat(chat, user_id)
    });
};

function noResponseToSearch(messengersBlock) {
    messengersBlock.innerHTML = `<p id="no-messages"><i class="fas fa-ban"></i> You don't have open chats!"</p>`;
};


// extra function
function drawChat(chat, user_id) {
    return (`
        <div class="chat">
            ${chat.last_message ?
                (`
                <a class="chat-url" href="${chat.chat_url}">
                    <pre id="pub_date">${chat.last_message.pub_date}</pre>

                    <p class="aside-block-image">
                        ${chat.members[0].photo ?
                            `<img src="${chat.members[0].photo}">` :
                            (
                                `<div class="photo_frame_mes_user" id="no-photo">
                                    <p class="user-no-photo">No image</p>
                                </div>
                            `)
                        }
                    </p>

                    <p class="user_name">
                        <i>${chat.members[0].user_full_name}</i>
                    </p>

                    <p class='${!chat.last_message.is_readed ? "unreaded" : "block-last_messages"}' id="last_messages">

                    ${chat.last_message.author_id === user_id ?
                        `<i class="last_messages"><span class="my-message">Вы:</span> ${chat.last_message.message}</i>` :
                        `<i class="last_messages">${chat.last_message.message}</i>`
                    }
                     </p>
                </a>
                `) : ""
            }
            </div>
    `);
};


// search user - event 
function search() {
    const html_message = document.getElementById("search-input");
    html_message.reportValidity();

    if (html_message.value) {
        const baseURL = window.location.protocol + "//" + window.location.host + window.location.pathname;
        history.pushState(null, null, `${baseURL}?search=${html_message.value}`);

        messengersPageSocket.send(JSON.stringify({
            'event_type': "search",
            'search_value': html_message.value,
        }));
    };
};
