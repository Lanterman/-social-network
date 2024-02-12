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
        let oldFollowersBlock = document.getElementById("old_followers");
        const checkedUser = `<p class="users_subs">
                            ${data.follower.follower_photo ?
                                `<img src="${data.follower.follower_photo}">` :
                                '<span class="user_photo"><span>No image</span></span>'
                            }

                            <a class="group_name" href=${data.follower.follower_url}>
                                ${data.follower.follower_full_name}
                            </a><br><br><br>

                            ${data.follower.follower_id != data.user_id ?
                                `<a class="button_home" href="/messages/check/${data.follower.follower_id}">Send message</a>` :
                                ' <i>My profile</i>'
                            }
                        </p><br>`

        oldFollowersBlock.innerHTML += checkedUser;
    };

};


function confirm_follower(follower_id) {
    homeSocket.send(JSON.stringify({
        "event_type": "confirm_follower",
        "follower_id": follower_id,
    }));

    const noFollowersBlock = document.getElementById("no_followers");
    if (noFollowersBlock) noFollowersBlock.remove();

    let announcements = document.getElementById("announcements");
    announcements.getElementsByClassName("users_subs").length === 1 ?
        announcements.remove() :
        document.getElementById(`follower_${follower_id}`).remove();
};

function cancel_follower(follower_id) {
    homeSocket.send(JSON.stringify({
        "event_type": "cancel_follower",
        "follower_id": follower_id,
    }));
    
    let announcements = document.getElementById("announcements");
    announcements.getElementsByClassName("users_subs").length === 1 ?
        announcements.remove() :
        document.getElementById(`follower_${follower_id}`).remove();
};

// function remove() {
//     if (!confirm('Удалить из друзей?')) {
//         rem_fr.href = '';
//     }
// }

// function agree() {
//     if (!confirm('Добавить в друзья?')) {
//         agr_fr.href = '';
//     }
// }

// function cancel() {
//     if (!confirm('Отменить заявку?')) {
//         can_fr.href = '';
//     }
// }
