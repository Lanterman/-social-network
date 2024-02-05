// home page

const homeSocket = new WebSocket('ws://' + window.location.host + '/ws/home/');

homeSocket.onopen = function(e) {
    console.log("Ok");
};

homeSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
};

homeSocket.onclose = function(e) {
    console.error('Home socket closed unexpectedly');
};


function confirm_follower(follower_id) {
    const request = new Request(`/home/${follower_id}/confirm_follower/`);
    fetch(request);

    document.getElementById(`follower_${follower_id}`).remove();

    console.log("Добавить вывод в блок старых фоловеров")
};

function cancel_follower(follower_id) {
    const request = new Request(`/home/${follower_id}/cancel_follower/`);
    fetch(request);
    
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
