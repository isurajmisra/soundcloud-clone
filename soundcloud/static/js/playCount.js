function countfn(song_id) {
    console.log(song_id)

    let jobj = {

        'song_id': song_id
    }
     $.ajax({
	url:'/songs/play_count',
	type:'POST',
	contentType: 'application/json;charset=UTF-8',
        data: JSON.stringify(jobj),
		});
}
