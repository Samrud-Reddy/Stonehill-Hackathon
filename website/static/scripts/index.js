$("#mic").hide()
$("#touchpad").hide()

$(".start").on('click', start)


function start() {
    open_touch_pad()
    $(".start").hide()
    var playPromise = play("audio/generate_choose.webm");
}

function balance() {
    fetch('/balance')
        .then(response => response.json())
        .then(data => {
            file = data["file"];
            play("audio/"+file)
            how_many_times_run = 0
            open_touch_pad()
        });
}

function pay() {
    console.log(Date.now())
    play("audio/how_to_use_mic.webm")
    
    $("#mic").on("mousedown", mic_down)
    $("#mic").on("mouseup", mic_up)

}


function confirm_payment() {
    open_touch_pad()

    play("audio/upi_instructions.webm") 
}
    
