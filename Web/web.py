from flask import Flask, render_template, request, redirect, url_for
from flask.views import MethodView
import sys

from Web.Controls.control_manager import ControlManager


class MenuPage(MethodView):
    CONNECT_TRIGGER = "connect"

    def __init__(self, control_manager: ControlManager = None):
        self.control_manager = control_manager

    def get(self):
        return render_template('menu.html')

    def post(self):
        trigger = request.form.get('trigger')
        if trigger == self.CONNECT_TRIGGER:
            return self.connect()

        print(f"Unknown trigger value: {trigger}", file=sys.stderr)
        return self.get()

    def connect(self):
        if self.control_manager.connect():
            return redirect(url_for('main'))
        else:
            return render_template('menu.html', error="Tars not found!")


class MainPage(MethodView):
    COMMAND_TRIGGER = "command"

    COMMAND_INPUT = "command_input"

    def __init__(self, control_manager: ControlManager = None):
        self.control_manager = control_manager

    def get(self):
        return render_template('main.html')

    def post(self):
        trigger = request.form.get('trigger')
        if trigger == self.COMMAND_TRIGGER:
            return self.command()

    def command(self):
        command = request.form.get(self.COMMAND_INPUT)
        if not self.control_manager.send_command(command):
            return render_template('main.html', error="Invalid command")

        return self.get()


class Web:
    def __init__(self):
        self.control_manager = ControlManager()
        self.app = Flask(__name__)
        self.app.add_url_rule('/', view_func=MenuPage.as_view('menu', self.control_manager))
        self.app.add_url_rule('/main', view_func=MainPage.as_view('main', self.control_manager))

    def run(self, debug=True, port=5000, **options):
        self.app.run(debug=debug, port=port, **options)


if __name__ == '__main__':
    web = Web()
    web.run()
