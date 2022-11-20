import eel


def launch_web():
    eel.init('web')
    eel.test_access()
    eel.start('menu.html', size=(1500, 900))  # Start the web.


def send_error(error):
    eel.show_error(error)


def hide_error():
    eel.show_error("")


def switch_to_console():
    eel.switch_to_console()