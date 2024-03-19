function delete_publication(publicationID) {
    document.getElementById(`publicationBlock_${publicationID}`).remove();

    if (!document.getElementsByClassName("publicationBlock").length) {
        document.getElementById("publicationsBlock").innerHTML = `
            <p id="no-publications">
                <i class="fas fa-poo"></i> No publications yet!
            </p>`;
    };

    const request = new Request(`/groups/${publicationID}/del_publication/`);
    fetch(request, {method: 'GET'});
};


function leave_the_group(groupID) {
    if (confirm('Do you really want to leave the group?')) {
        document.getElementById(`groupBlock_${groupID}`).remove();
        document.getElementById(`groupBlock_${groupID}`)?.remove();

        if (!document.getElementsByClassName("block-include-group").length) {
            document.getElementById("blockGroupList").innerHTML = `
                <p id="no-instances">
                    <i class="fas fa-ban"></i> You do not have your own groups or groups that you are subscribed to!
                </p>`;
        };
    
        const request = new Request(`/groups/${groupID}/group_activity/`);
        fetch(request, {method: 'GET'});
    };
};


function group_activity(groupID, typeAction, groupSlug) {
    let groupButton = document.getElementsByClassName("groupButton")[0];
    let followersCount = document.getElementById("followers_count");

    if (typeAction === "Subscribe") {
        groupButton.innerHTML = (
            `<p class="p1 group_activity"><a onclick="group_activity('${groupID}', 'Unsubscribe', '${groupSlug}')">Unsubscribe</a></p>
            <p id="p2"><a href="/groups/${groupSlug}/add_publication/"><i class="fas fa-plus"></i> Add publication</a></p>`
            );
        followersCount.textContent = Number(followersCount.textContent) + 1;

    }else {
        groupButton.innerHTML = (`
            <p class="p1 group_activity"><a onclick="group_activity('${groupID}', 'Subscribe', '${groupSlug}')">Subscribe</a></p>`
        );
        followersCount.textContent = followersCount.textContent - 1;
    };
    
    const request = new Request(`/groups/${groupID}/group_activity/`);
    fetch(request, {method: 'GET'});
};
