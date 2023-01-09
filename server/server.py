import time
import ev3
import web_sockets
import moves

KEYBOARD_INPUT = False

def keyboard_input(move_queue, color):
    from sshkeyboard import listen_keyboard

    def press(key):
        print(f"{key} pressed")
        move_queue[moves.KEYBINDINGS[key]] = True

    def release(key):
        print(f"{key} released")
        move_queue[moves.KEYBINDINGS[key]] = False

    listen_keyboard(
        on_press=press,
        on_release=release,
    )

def msleep(t):
    time.sleep(t / 1000)

def main():
    move_state = {
        "forward": False,
        "back": False,
        "left": False,
        "right": False,
        "camera_up": False,
        "camera_down": False,
    }

    color = {
        "rgb":
        {
            "r": 0,
            "g": 0,
            "b": 0,
        }
    }

    ev3_server = ev3.EV3Connection("0.0.0.0", 5555, move_state, color)
    ev3_server.daemon = True
    ev3_server.start()

    if KEYBOARD_INPUT:
        keyboard_input(move_state, color)

    else:
        websockets_server = web_sockets.WebsocketsServer(8001, move_state, color)
        websockets_server.start()

if __name__ == "__main__":
    main()
