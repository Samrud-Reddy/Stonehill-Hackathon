let number_of_clicks = 0
let last_touch;
let time_to_die = 1000

function open_touch_pad() {
    number_of_clicks = 0
    let touchpad = $("#touchpad");
    $("#mic").hide() 
    touchpad.show()
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
    console.log(last_touch)
    console.log(now)
    console.log(now - last_touch)
    console.log()
    if ((now - last_touch) > time_to_die*0.8) {
        close_touch_pad()
    } else {
        console.log("fail")
    }
}

function close_touch_pad() {
    let touchpad = $("#touchpad");
    $("#mic").show() 
    touchpad.hide()
}
open_touch_pad()


