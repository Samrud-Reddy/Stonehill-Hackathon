let number_of_clicks = 0
let last_touch;
let time_to_die = 1000
let upi = ""

let how_many_times_run = 0

let closing = false

function open_touch_pad() {
    number_of_clicks = 0
    how_many_times_run += 1
    let touchpad = $("#touchpad");
    $("#mic").hide() 
    touchpad.show()
    closing = false
    last_touch = 0
}


$("#touchpad").on( "mousedown", function() {
    number_of_clicks += 1
});

$("#touchpad").on( "mouseup", function() {
    last_touch = Date.now();
    const myTimeout = setTimeout(handle_death, time_to_die);
});

function handle_death() {
    now = Date.now(); 
    if ((now - last_touch) > time_to_die*0.8) {
        closing = false
        close_touch_pad()
        last_touch = 0
        closing = true
    } else {
        console.log("fail")
    }
}

function close_touch_pad() {
    if ( !closing ) {
        let touchpad = $("#touchpad");
        $("#mic").show() 
        touchpad.hide()
        if (how_many_times_run == 1) {
            if (number_of_clicks == 1) {
                balance()
            } else if (number_of_clicks == 2){
                pay()
            }
        } else if (how_many_times_run == 2) {
            if (number_of_clicks == 1) {
                confirm_payment()
            } else if (number_of_clicks == 2){
                how_many_times_run -= 1
            }
        } else if (how_many_times_run > 2 && how_many_times_run < 7) {
            upi += String(number_of_clicks)
            closing = false
            play("https://media.geeksforgeeks.org/wp-content/uploads/20190531135120/beep.mp3")
            open_touch_pad()
        } else if (how_many_times_run == 7){
            play("audio/payment_complete.webm")
        }
        closing = false
    }
}




