// groups page, use websocket

const groupsPageSocket = new WebSocket('ws://' + window.location.host + '/ws/groups/');


groupsPageSocket.onopen = function(e) {
    console.log("Groups page socket opened");
};

groupsPageSocket.onclose = function(e) {
    console.error('Groups page socket closed unexpectedly');
};

groupsPageSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    console.log(data);

    if (data["event_type"] === "search") {
        const groupsBlock = document.getElementsByClassName("block-group-list")[0];
        groupsBlock.innerHTML = "";

        responseToSearch(data["user_id"], data["my_groups"], groupsBlock);
        groupsBlock.innerHTML += '<p class="global-search"><span id="global-search-name">Global search</span></p>';
        
        if (data["global_groups"].length) {
            responseToSearch(data["user_id"], data["global_groups"], groupsBlock);
        } else {
            noResponseToSearch(groupsBlock);
        };
    };
};


// event types logic of onmessage
function responseToSearch(user_id, groups, groupsBlock) {
    Object.values(groups).forEach((group) => {
        groupsBlock.innerHTML += drawGroup(group, user_id)
    });
};

function noResponseToSearch(publicationsBlock) {
    publicationsBlock.innerHTML = (`
        <p id="no-instances">
            <i class="fas fa-ban"></i> 
            You do not have your own groups or groups that you are subscribed to!
        </p>
    `);
};


// extra function
function drawGroup(group, user_id) {

    return (`
        <div class="block-include-group" id="groupBlock_${group.id}">
            <a href="${group.group_url}"><img src="${group.photo}"></a>
            
            <p class="group_margin">
                <a href="${group.group_url}">
                    <i>${group.name}</i>
                </a>
            </p>

            <a class="del" id="leave_the_group" onclick="leave_the_group(${group.id})">
                ${group.followers.includes(user_id) ? '<i class="fas fa-backspace"></i>' : ''}
            </a>

            <p class="group_us">
                <span>Followers: ${group.followers.length}</span>
                ${user_id === group.owner ? '<span class="block-my-group">My group</span>' : ""}
            </p>
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

        groupsPageSocket.send(JSON.stringify({
            'event_type': "search",
            'search_value': html_message.value,
        }));
    };
};
