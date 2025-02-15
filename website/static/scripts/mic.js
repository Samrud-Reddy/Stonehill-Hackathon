let audio = null
let recorder = null
let blob = null
let payment = {}

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
            audio = new Audio(audioUrl);
        });
    });

let is_recording = false


function start_recording(){
    is_recording = true
    recorder.start()
}
function stop(){
    is_recording = false
    recorder.stop()
}

function play(url){
    const sound = new Audio(url);
    return sound.play()
}

async function uploadAudio(filename = "audio.webm") {
    let formData = new FormData();
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

function mic_down(){
    start_recording()
}
function mic_up(){
    stop()
    setTimeout(() => {
        uploadAudio("payments.webm");
        fetch('/payment-audio')
            .then(response => response.json())
            .then(data => {
                console.log(data);
                payment = data
                play("audio/"+data["audio_file"])
                open_touch_pad()
            }); 
    }, 500);
}
