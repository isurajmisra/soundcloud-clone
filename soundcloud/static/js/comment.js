const link = document.querySelectorAll(".link")
let audio = document.querySelector(".audio-player")
link.forEach(e => {
    e.addEventListener('click', updateTime)

    function updateTime() {
        let time = e.innerHTML
        let time_floor = Math.floor(time)
        audio.currentTime = time_floor * 60 + (time - time_floor) * 60
    }
})