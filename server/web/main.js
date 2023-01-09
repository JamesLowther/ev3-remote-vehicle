var keys = [];
var websocket = null;
window.addEventListener("keydown",
    function(e){
        keys[e.key] = true;
        document.getElementById(e.key).style.backgroundColor = "#aaaaaa";

        send_keys();
    },

false);

window.addEventListener('keyup',
    function(e){
        keys[e.key] = false;
        document.getElementById(e.key).style.backgroundColor = "#FFFFFF";

        send_keys();
    },
false);

window.addEventListener("DOMContentLoaded", () => {
    websocket = new WebSocket("ws://24.199.72.202:8001/");

    receiveMessage(websocket);
    init(websocket);
});

function init(websocket) {
    websocket.addEventListener("open", () => {
        const event = {type: "init"};
        websocket.send(JSON.stringify(event));
    });
}

function receiveMessage(websocket) {
    websocket.addEventListener("message", ({ data }) => {
        const event = JSON.parse(data)
        if (event.rgb) {
            var color = `rgb(${event.rgb.r},${event.rgb.g},${event.rgb.b})`

            console.log(color);

            document.getElementById("colorbox").style.backgroundColor = color;
        } else if (event.message) {
            window.setTimeout(() => window.alert(event.message), 50);
        }
    });
}

function send_keys() {
    var state = {
        "forward": Boolean(keys["w"]),
        "left": Boolean(keys["a"]),
        "back": Boolean(keys["s"]),
        "right": Boolean(keys["d"]),
        "camera_up": Boolean(keys["ArrowUp"]),
        "camera_down": Boolean(keys["ArrowDown"]),
    }

    console.log(state)

    websocket.send(JSON.stringify(state));
}
