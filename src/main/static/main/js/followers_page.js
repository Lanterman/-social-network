// followerSocket page, use websocket

const followerSocket = new WebSocket('ws://' + window.location.host + '/ws/followers/');


followerSocket.onopen = function(e) {
    console.log("Followers socket opened");
};

followerSocket.onclose = function(e) {
    console.error('Followers socket closed unexpectedly');
};

followerSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    console.log(data);

    if (data["event_type"] === "search") {
        const followersBlock = document.getElementsByClassName("followers-block")[0];
        followersBlock.innerHTML = "";

        responseToSearch(data["my_followers"], followersBlock);
        followersBlock.innerHTML += '<p class="global_search">Global search</p>';
        
        if (data["global_users"].length) {
            responseToSearch(data["global_users"], followersBlock, "global");
        } else {
            noResponseToSearch(followersBlock);
        };
    };
};


// event types logic of onmessage
function responseToSearch(users, followersBlock, typeOfSearch=null) {
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
                !user.my_follower ?
                    (user.my_sub ?
                        (`<a id="del-user" class="follower-block-user" onclick="unsubscribe('${user.id}')">
                            Unubscribe from user
                        </a>`) :
                        (`<a id="subscribe" onclick="subscribe('${user.id}')">
                            Subscribe from user
                        </a>`))
                    :
                    (`<a id="del-user" class="follower-block-user" onclick="blockUser('${user.id}')">
                        Block user
                    </a>`) :
                (`<a id="del-user" class="follower-block-user" onclick="blockUser('${user.id}')">
                    Block user
                </a>`)
            }
        </div>
    `);
};  


// events
// unsubscribe - event
function unsubscribe(user_id) {
    document.getElementById(`sub_${user_id}`).remove();

    followerSocket.send(JSON.stringify({
        'event_type': "unsubscribe",
        'user_id': user_id,
    }));
};

// block user -event
function blockUser(user_id) {
    document.getElementById(`sub_${user_id}`).remove();
    document.getElementById(`sub_${user_id}`)?.remove();

    if (!document.getElementsByClassName('follower-block').length) {
        document.getElementsByClassName('followers-block')[0].innerHTML = (
            '<p id="foo" class="foo"><i class="fas fa-ban"></i> No users!</p>'
        );
    };

    followerSocket.send(JSON.stringify({
        'event_type': "block_user",
        'user_id': user_id,
    }));
};

// subscribe - event
function subscribe(user_id) {
    const newSub = document.getElementById(`sub_${user_id}`);
    newSub.remove();

    followerSocket.send(JSON.stringify({
        'event_type': "subscribe",
        'user_id': user_id,
    }));
};

// search user - event 
function search() {
    const html_message = document.getElementById("search-input");
    html_message.reportValidity();

    if (html_message.value) {
        const baseURL = window.location.protocol + "//" + window.location.host + window.location.pathname;
        history.pushState(null, null, `${baseURL}?search=${html_message.value}`);

        followerSocket.send(JSON.stringify({
            'event_type': "search",
            'search_value': html_message.value,
        }));
    };
};
