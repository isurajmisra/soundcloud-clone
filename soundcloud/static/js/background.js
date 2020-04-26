function startTask() {
    let user_id = document.querySelector("#user_id").value
    let username = document.querySelector("#username").innerHTML
    let email = document.querySelector("#email").innerHTML
    let songTitle = document.querySelectorAll(".song_title")
    let songList = []
    songTitle.forEach(e => {
        songList.push(e.innerHTML)
    })
    let body = {
        "id": user_id,
        "username": username,
        "email": email,
        "songList": songList

    }


    let di = document.querySelector("#progress")
    di.innerHTML = ""
    div = $('<div class="progress"><div></div><div>0%</div><div>...</div><div>&nbsp;</div></div><hr>');
    $('#progress').append(div);


    let nanobar = new Nanobar({
        bg: '#44f',
        target: div[0].childNodes[0]
    });

    $.ajax({
        type: 'POST',
        url: '/task',
        contentType: 'application/json;charset=UTF-8',
        data: JSON.stringify(body),
        success: function(data, status, request) {
            status_url = request.getResponseHeader('Location');
            update_progress(status_url, nanobar, div[0]);

        },
        error: function() {
            alert('Unexpected error');
        }
    });


}

function update_progress(status_url, nanobar, status_div) {
    let username = document.querySelector("#username").innerHTML
        // send GET request to status URL
    $.getJSON(status_url, function(data) {
        // update UI
        percent = parseInt(data['current'] * 100 / data['total']);
        nanobar.go(percent);
        if (percent == 100) {
            $.ajax({
                url: `/download/${username}`,
                success: function(data) {
                    var blob = new Blob([data]);
                    var link = document.createElement('a');
                    link.href = window.URL.createObjectURL(blob);
                    link.download = `user-info-${username}.txt`;
                    link.click();
                }
            });

        }
        $(status_div.childNodes[1]).text(percent + '%');
        $(status_div.childNodes[2]).text(data['status']);
        if (data['state'] != 'PENDING' && data['state'] != 'PROGRESS') {
            if ('result' in data) {
                // show result
                $(status_div.childNodes[3]).text('Result: ' + data['result']);

            } else {
                // something unexpected happened
                $(status_div.childNodes[3]).text('Result: ' + data['state']);

            }
        } else {
            // rerun in 2 seconds
            setTimeout(function() {
                update_progress(status_url, nanobar, status_div);
            }, 2000);
        }
    });
}
