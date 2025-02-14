let audio = null
let recorder = null
let blob = null

navigator.mediaDevices.getUserMedia({ audio: true })
    .then(stream => {
        recorder = new MediaRecorder(stream);

        let audioChunks = [];
        recorder.addEventListener("dataavailable", event => {
            audioChunks.push(event.data);
        });

        recorder.addEventListener("stop", () => {
            blob = new Blob(audioChunks);
            audioChunks = []
            const audioUrl = URL.createObjectURL(blob);
            audio = new Audio(audioUrl,);
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

function play(url){
    const sound = new Audio(url);
    sound.play()
}

async function uploadAudio(filename = "audio.webm") {
    const formData = new FormData();
    formData.append("file", blob, filename);

    try {
        const response = await fetch("/upload", {
            method: "POST",
            body: formData,
        });

        const result = await response.json();
        console.log("Upload response:", result);
    } catch (error) {
        console.error("Upload error:", error);
    }
}

