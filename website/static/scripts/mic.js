let audio = null
let recorder = null

navigator.mediaDevices.getUserMedia({ audio: true })
    .then(stream => {
        recorder = new MediaRecorder(stream);

        let audioChunks = [];
        recorder.addEventListener("dataavailable", event => {
            audioChunks.push(event.data);
        });

        recorder.addEventListener("stop", () => {
            const audioBlob = new Blob(audioChunks);
            audioChunks = []
            const audioUrl = URL.createObjectURL(audioBlob);
            audio = new Audio(audioUrl);
        });
    });

let is_recording = false


function start(){
    is_recording = true
    recorder.start()
}
function stop(){
    is_recording = false
    recorder.stop()
}

let player = null

function play(){
     player = audio.play()
    player.finally(() => console.log("Done"))
}
