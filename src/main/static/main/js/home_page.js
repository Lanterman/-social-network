// home page

const homeSocket = new WebSocket('ws://' + window.location.host + '/ws/home/');

homeSocket.onopen = function(e) {
    console.log("Ok");
};


homeSocket.onclose = function(e) {
    console.error('Home socket closed unexpectedly');
};


homeSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);

    console.log(data)

    if (data.event_type == "confirm_follower") {
        confirm_follower_onmessage(data);
    
    } else if (data.event_type == "remove_follower") {
        remove_follower_onmessage();
    
    } else if (data.event_type == "remove_subscription") {
        remove_subscription_onmessage();

    } else if (data.event_type == "sub_user") {
        sub_user_onmessage(data);

    } else if (data.event_type == "unsub_user") {
        unsub_user_onmessage(data);
    };

};


// events - response from WS
function confirm_follower_onmessage(data) {
    let oldFollowersBlock = document.getElementById("old_followers");
    const checkedUser = `
        <p class="users_subs" id="oldFollower_${data.follower.id}">
            ${data.follower.photo ?
                `<img src="${data.follower.photo}">` :
                '<span class="user_photo"><span>No image</span></span>'
            }

            <a class="group_name" href=${data.follower.user_url}>
                ${data.follower.user_full_name}
            </a><br><br><br>

            ${data.follower.id != data.user_id ?
                (`
                    <a class="button_home" href="/messages/check/${data.follower.id}">Send message</a>
                    <span class="check minus" onclick="remove_follower(${data.follower.id})">
                        <i class="fas fa-user-check"> Block</i>
                    </span>
                `) :
                ' <i>My profile</i>'
            }
            <br>
        </p>`
    
    oldFollowersBlock.innerHTML += checkedUser;
};

function remove_follower_onmessage() {
    let oldFollowersBlock = document.getElementById("old_followers");

    if (!oldFollowersBlock.getElementsByClassName("users_subs").length) {
        oldFollowersBlock.innerHTML = '<h4 id="no_followers">No followers</h4>';
    };
};

function remove_subscription_onmessage() {
    let subscriptionBlock = document.getElementById("subscriptionBlock");
    if (!subscriptionBlock.getElementsByClassName("users_subs").length) {
        subscriptionBlock.innerHTML = '<h4>No subscriptions</h4>';
    };
};

function sub_user_onmessage(data) {
    let buttonsBlock = document.getElementById("button_home");
    let buttonsBlockValue = buttonsBlock.innerHTML;
    buttonsBlock.innerHTML = `
        <p class="act_button" id="unsub_user" onclick="unsub_user('${data.user_id}')">
            <i>Unsubscribe</i>
        </p>
    ` + buttonsBlockValue;
};

function unsub_user_onmessage(data) {
    let buttonsBlock = document.getElementById("button_home");
    let buttonsBlockValue = buttonsBlock.innerHTML;
    buttonsBlock.innerHTML = `
        <p class="act_button" id="sub_user" onclick="sub_user('${data.user_id}')">
            <i class="fas fa-user-check" id="sub_user_icon"></i> 
            Subscribe
        </p>
    ` + buttonsBlockValue;
};


// events - request to WS
function confirm_follower(follower_id) {
    const noFollowersBlock = document.getElementById("no_followers");
    if (noFollowersBlock) noFollowersBlock.remove();

    let announcements = document.getElementById("announcements");
    announcements.getElementsByClassName("users_subs").length === 1 ?
        announcements.remove() :
        document.getElementById(`follower_${follower_id}`).remove();
    
    homeSocket.send(JSON.stringify({
        "event_type": "confirm_follower",
        "follower_id": follower_id,
    }));
};

function cancel_follower(follower_id) {
    let announcements = document.getElementById("announcements");
    announcements.getElementsByClassName("users_subs").length === 1 ?
        announcements.remove() :
        document.getElementById(`follower_${follower_id}`).remove();
    
    homeSocket.send(JSON.stringify({
        "event_type": "cancel_follower",
        "follower_id": follower_id,
    }));
};

function remove_follower(follower_id) {
    document.getElementById(`oldFollower_${follower_id}`).remove();

    homeSocket.send(JSON.stringify({
        "event_type": "remove_follower",
        "follower_id": follower_id,
    }));
    
};

function remove_subscription(subscription_id) {
    document.getElementById(`subscriptions_${subscription_id}`).remove();

    homeSocket.send(JSON.stringify({
        "event_type": "remove_subscription",
        "subscription_id": subscription_id,
    }));
    
};

function sub_user(user_id) {
    document.getElementById('sub_user').remove();

    homeSocket.send(JSON.stringify({
        "event_type": "sub_user",
        "user_id": user_id,
    }));
};

function unsub_user(user_id) {
    document.getElementById('unsub_user').remove();

    homeSocket.send(JSON.stringify({
        "event_type": "unsub_user",
        "user_id": user_id,
    }));
};

function block_user(user_id) {
    document.getElementById('block_user').remove();

    homeSocket.send(JSON.stringify({
        "event_type": "block_user",
        "user_id": user_id,
    }));
};
