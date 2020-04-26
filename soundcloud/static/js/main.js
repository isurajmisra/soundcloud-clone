let comment = document.querySelectorAll(".comment-btn")
comment.forEach(element => {

    element.addEventListener('click', showCommentBox)



    function showCommentBox(event) {
        event.preventDefault();
        element.style.display = "none"
        const comment_div = element.nextElementSibling
        const form_field = document.createElement("form")
        const text_field = document.createElement("textarea")
        text_field.setAttribute('id', 'comment-area')
        const submit = document.createElement("button")
        submit.addEventListener('click', postForm)
        submit.setAttribute('class', submit)
        submit.appendChild(document.createTextNode("Post"))
        const cancel = document.createElement("button")
        cancel.addEventListener('click', cancelPost)
        cancel.setAttribute('class', cancel)
        cancel.appendChild(document.createTextNode("cancel"))
        form_field.appendChild(text_field)
        form_field.appendChild(submit)
        form_field.appendChild(cancel)
        comment_div.appendChild(form_field)
    }

    function postForm(event) {
        event.preventDefault();
        let audio = element.previousElementSibling
        let timestamp = audio.currentTime
        if (timestamp > 60) {
            upper = timestamp / 60;
            lower = timestamp - 60
            timestamp = Math.floor(upper) + (lower / 100);
        }
        let text = document.querySelector("#comment-area").value
        let div = element.parentElement
        let song_id = div.firstElementChild.value
        console.log(timestamp)
        let jobj = {
            'song_id': song_id,
            'timestamp': timestamp,
            'text': text
        }
       
	$.ajax({
        type: 'POST',
        url: '/home/post_comment',
        contentType: 'application/json;charset=UTF-8',
        data: JSON.stringify(jobj),
	});
        let comment_div = element.nextElementSibling
        comment_div.innerHTML = ""
        document.location.reload(true)
    }

    function cancelPost(event) {
        event.preventDefault();
        element.style.display = ""
        const comment_div = element.nextElementSibling
        comment_div.innerHTML = ""
    }

})
