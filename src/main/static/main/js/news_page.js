// news page, use websocket

const newsPageSocket = new WebSocket('ws://' + window.location.host + '/ws/news/');


newsPageSocket.onopen = function(e) {
    console.log("News page socket opened");
};

newsPageSocket.onclose = function(e) {
    console.error('News page socket closed unexpectedly');
};

newsPageSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);

    if (data["event_type"] === "search") {
        document.getElementsByClassName("nav")[0]?.remove();
        const publicationsBlock = document.getElementsByClassName("publications-block")[0];
        publicationsBlock.innerHTML = "";
        
        if (data["publications"].length) {
            responseToSearch(data["user_id"], data["publications"], publicationsBlock);
            console.log("ok")
        } else {
            noResponseToSearch(publicationsBlock);
        };
    };
};


// event types logic of onmessage
function responseToSearch(user_id, publications, publicationsBlock) {
    Object.values(publications).forEach((publication) => {
        publicationsBlock.innerHTML += drawPublication(publication, user_id)
    });
};

function noResponseToSearch(publicationsBlock) {
    publicationsBlock.innerHTML = `<p id="no-publications"><i class="fas fa-poo"></i> No publications yet!</p>`;
};


// extra function
function drawPublication(publication, user_id) {

    return (`
        <div class="p publicationBlock" id="publicationBlock_${publication.id}">
            <a class="a1" href="${publication.publication_url}">${publication.name}</a>

            ${publication.owner.id === user_id ?
                (`<a class="pub_menu" id="del" onclick="delete_publication(${publication.id})">
                    <i class="fas fa-backspace"></i>
                </a>
                <a class="pub_menu" href="/groups/${publication.slug}/update_pub/">
                    <i class="fas fa-pen"></i>
                </a>`) :
                ""
            }
            
            <pre>${publication.date}</pre>

            <safescript>
            <p id="ap">${publication.biography}</p>
            </safescript>

            ${publication.photo ? `<img src="${publication.photo}" alt="photo"><br><br>` : ""}

            <p id="pub-bottom-info">
                <span class="pub-bottom-item">
                    <b class="rating-label">User rating:</b>
                    ${publication.rating ?
                        `<span class="editContent">${publication.rating} / 5.0</span>` :
                        `<span class="editContent">None</span>`
                    }
                </span>

                <span class="pub-bottom-item">
                    <i>
                        <a class="pub-comments" href="/publish/${publication.slug}/comments/">
                        <i class="fas fa-comments"></i> Comments</a>
                    </i>
                </span>

                <span id="block-owner" class="pub-bottom-item">Author:
                    <a class="pub-owner" href="${publication.owner.user_url}" title="Owner">
                        <i>${publication.owner.username}</i>
                    </a>
                </span>
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

        newsPageSocket.send(JSON.stringify({
            'event_type': "search",
            'search_value': html_message.value,
        }));
    };
};
