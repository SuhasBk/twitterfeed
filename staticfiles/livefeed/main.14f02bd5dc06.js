window.addEventListener('load', function(e) {
    try {
        document.getElementById('id_handles').addEventListener('keypress', (event) => {
            if (event.target.value.length > 2) {
                document.getElementById('search-users').removeAttribute('disabled');
            }
        });
    } catch (error) {}
})

var getCookie = (name) => {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

setTimeout(() => {
    let statusElements = document.getElementsByClassName('alert');
    if(statusElements.length > 0) {
        statusElements[0].remove()
    }
}, 3000)

var confirmRemoveHandle = (e) => {
    let handle = e.innerText;
    if(confirm(`Are you sure you want to remove '${handle}' from your handles?`)) {
        // window.location.href = `/removeHandle/${handle}`
        fetch(`/removeHandle/${handle}`).then((response) => {
            document.getElementById(handle).remove();
            document.querySelector(`[data-widget-id='profile:${handle}']`).remove();
        });
    } 
}

var searchUsers = () => {
    let query = document.getElementById('id_handles').value;
    if(query.length >= 3) {
        console.log("searching users...")
        fetch('/api/searchUsers/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie("csrftoken"),
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                'query': query
            })
        }).then(response => {
            return response.json();
        }).then(jsonData => {
            displayUsers(jsonData.results);
        });
    }
}

var displayUsers = (data) => {
    document.getElementById('results').style.visibility = 'visible';
    let container = document.getElementById('userResults');
    container.innerHTML = "";
    for(let i=0;i<data.length;i++) {
        let user = JSON.parse(data[i]);
        let userHTML = 
        `<div style="text-align: center;">
            <img src='${user.profile_image_url}'></img><br><br>
            ${user.name} #VERIFIED#<br>
            ${user.screen_name}<br>
            ${user.description}<br>
            ${user.location}<br>`;

        if(user.following) {
            userHTML += `<button id='add-${user.screen_name}' class="btn" onclick="addHandle('${user.screen_name}')" disabled>✅</button></div>`;
        } else {
            userHTML += `<button id='add-${user.screen_name}' class="btn btn-outline-info" onclick="addHandle('${user.screen_name}')">➕</button></div>`;
        }

        if(user.verified) {
            userHTML.replace('#VERIFIED#', '🤙')
        } else {
            userHTML.replace('#VERIFIED#', '👎')
        }
        container.innerHTML += userHTML;
    }
}

var addHandle = (handle) => {
    console.log(handle)
    fetch('/api/addUsers/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie("csrftoken"),
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'handle': handle
        })
    }).then(response => {
        return response.json();
    }).then(jsonData => {
        let handleElement = document.getElementById(`add-${handle}`);
        handleElement.innerText = '✅';
        handleElement.setAttribute('disabled', true)
    });
}