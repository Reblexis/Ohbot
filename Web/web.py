from flask import Flask, render_template, request, redirect, url_for, Response
from flask.views import MethodView
import sys

from Web.Controls.command_manager import CommandManager
from Function.general_controller import ControlManager


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
            print("connected")
            return redirect(url_for('main'))
        else:
            print("not connected")
            return render_template('menu.html', error="Tars not found!")


class MainPage(MethodView):
    COMMAND_TRIGGER = "command"

    COMMAND_INPUT = "command_input"

    def __init__(self, control_manager: ControlManager = None, command_manager: CommandManager = None):
        self.control_manager = control_manager
        self.command_manager = command_manager

    def get(self):
        return render_template('main.html',
                               show_camera_feed=self.control_manager.core_controller.vision_controller.show_camera)

    def post(self):
        trigger = request.form.get('trigger')
        if trigger == self.COMMAND_TRIGGER:
            return self.command()

    def command(self):
        command = request.form.get(self.COMMAND_INPUT)
        if not self.command_manager.execute_command(command):
            return render_template('main.html', error="Invalid command")

        return self.get()


class CameraFeed(MethodView):
    def __init__(self, control_manager: ControlManager = None):
        self.control_manager = control_manager

    def get(self):
        return Response(self.control_manager.get_camera_feed(), mimetype='multipart/x-mixed-replace; boundary=frame')


class Web:
    def __init__(self):
        self.control_manager = ControlManager()
        self.command_manager = CommandManager(self.control_manager.core_controller)
        self.app = Flask(__name__)
        self.app.add_url_rule('/', view_func=MenuPage.as_view('menu', self.control_manager))
        self.app.add_url_rule('/main', view_func=MainPage.as_viFew('main', self.control_manager, self.command_manager))
        self.app.add_url_rule('/video_feed', view_func=CameraFeed.as_view('camera_feed', self.control_manager))

    def run(self, debug=False, port=5000, **options):
        self.app.run(debug=debug, port=port, use_reloader=False, **options)


if __name__ == '__main__':
    web = Web()
    web.run(debug=True)
