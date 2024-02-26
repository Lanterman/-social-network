// subscriptions page, use websocket

const subscriptionSocket = new WebSocket('ws://' + window.location.host + '/ws/subscriptions/');


subscriptionSocket.onopen = function(e) {
    console.log("Ok");
};

subscriptionSocket.onclose = function(e) {
    console.error('Subscriptions socket closed unexpectedly');
};

subscriptionSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    console.log(data);

    if (data["event_type"] === "search") {
        const followersBlock = document.getElementsByClassName("followers-block")[0];
        followersBlock.innerHTML = "";

        Object.values(data["my_subs"]).forEach((sub) => {
            followersBlock.innerHTML += (`
                <div class="follower-block" id="sub_${sub.user_pk}">
                    <a id='follower-url' href="${sub.user_url}">
                        ${sub.user_photo ?
                            `<img src="${sub.user_photo}">` :
                            `<div class="photo_frame" id="no-photo"><p>No image</p></div>`
                        }
                    </a>
                
                    <p class="follower-name">
                        <a class="follower-url" href="${sub.user_url}">
                            <i>${sub.user_full_name}</i>
                        </a>
                    </p>

                    <a class="follower-send-message" href="/messages/check/${sub.user_pk}">Send message</a>
                    <a id="del-user" class="follower-block-user" onclick="unsubscribe('${sub.user_pk}')">Unsubscribe from user</a>
                </div>
            `);
        });
    };
};



// unsubscribe
function unsubscribe(subscription_id) {
    document.getElementById(`sub_${subscription_id}`).remove();

    if (!document.getElementsByClassName('follower-block').length) {
        document.getElementsByClassName('followers-block')[0].innerHTML = (
            '<p id="foo" class="foo"><i class="fas fa-ban"></i> No users!</p>'
        );
    };

    subscriptionSocket.send(JSON.stringify({
        'event_type': "unsubscribe",
        'subscription_id': subscription_id,
    }));
};

// search user
function search() {
    const html_message = document.getElementById("search-input");
    html_message.reportValidity();

    if (html_message.value) {
        subscriptionSocket.send(JSON.stringify({
            'event_type': "search",
            'search_value': html_message.value,
        }));
    };
};