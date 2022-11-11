import eel

eel.init('web')


@eel.expose  # Expose this function to Javascript
def python_log(x):
    print(x)


@eel.expose
def pass_buffer(buffer):
    print(type(buffer))


@eel.expose
def send_command(command):
    print(command)


@eel.expose
def answer_key_press(key):
    if key == 13:
        print("Enter")


def launch_web():
    eel.test_access()
    eel.start('main.html', size=(1500, 900))  # Start the web.


"""

say_hello_py('Python World!')
eel.next_picture('Python World!')   # Call a Javascript function
"""
