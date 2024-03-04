// subscriptions page, use websocket

const subscriptionSocket = new WebSocket('ws://' + window.location.host + '/ws/subscriptions/');


subscriptionSocket.onopen = function(e) {
    console.log("Subscriptions socket opened");
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

        responseToSearch(data["my_subs"], followersBlock, "subs");
        followersBlock.innerHTML += '<p class="global_search">Global search</p>';
        
        if (data["global_users"].length) {
            responseToSearch(data["global_users"], followersBlock, "global");
        } else {
            noResponseToSearch(followersBlock);
        };
    
    } else if (data["event_type"] === "subscribe") {
        const followersBlock = document.getElementsByClassName("followers-block")[0];
        followersBlock.innerHTML = drawUser(data["new_sub"]) + followersBlock.innerHTML;
    };
};


// event types logic of onmessage
function responseToSearch(users, followersBlock, typeOfSearch) {
    Object.values(users).forEach((user) => {
        followersBlock.innerHTML += drawUser(user, typeOfSearch)
    });
};

function noResponseToSearch(followersBlock) {
    followersBlock.innerHTML += '<p id="foo" class="foo"><i class="fas fa-ban"></i>No users!</p>';
};


// extra function
function drawUser(user, typeOfSearch=null) {
    return (`
        <div class="follower-block" id="sub_${user.id}">
            <a id='follower-url' href="${user.user_url}">
                ${user.photo ?
                    `<img src="${user.photo}">` :
                    `<div class="photo_frame" id="no-photo"><p>No image</p></div>`
                }
            </a>
        
            <p class="follower-name">
                <a class="follower-url" href="${user.user_url}">
                    <i>${user.user_full_name}</i>
                </a>
            </p>

            <a class="follower-send-message" href="/messages/check/${user.id}">Send message</a>

            ${typeOfSearch === "global" ?
                (user.my_sub ?
                    (`<a id="del-user" class="follower-block-user" onclick="unsubscribe('${user.id}')">
                        Unsubscribe from user
                    </a>`) :
                    (`<a id="subscribe" onclick="subscribe('${user.id}')">
                        Subscribe from user
                    </a>`))
                :
                (`<a id="del-user" class="follower-block-user" onclick="unsubscribe('${user.id}')">
                    Unsubscribe from user
                </a>`)
            }
        </div>
    `);
};


// events
// unsubscribe - event
function unsubscribe(subscription_id) {
    document.getElementById(`sub_${subscription_id}`).remove();
    document.getElementById(`sub_${subscription_id}`)?.remove();

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

// subscribe - event
function subscribe(subscription_id) {
    const newSub = document.getElementById(`sub_${subscription_id}`);
    newSub.remove();

    subscriptionSocket.send(JSON.stringify({
        'event_type': "subscribe",
        'subscription_id': subscription_id,
    }));
};

// search user - event 
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
