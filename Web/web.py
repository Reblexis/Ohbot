from flask import Flask, render_template, request, redirect, url_for, Response
from flask.views import MethodView
import sys

from Function.Core.command_manager import CommandManager
from Function.Core.core_controller import CoreController


class MenuPage(MethodView):
    CONNECT_TRIGGER = "connect"

    def __init__(self, core_controller: CoreController = None):
        self.core_controller = core_controller

    def get(self):
        return render_template('menu.html')

    def post(self):
        trigger = request.form.get('trigger')
        if trigger == self.CONNECT_TRIGGER:
            return self.connect()

        print(f"Unknown trigger value: {trigger}", file=sys.stderr)
        return self.get()

    def connect(self):
        if self.core_controller.physical_controller.search_connection():
            print("Found connection!")
            return redirect(url_for('main'))
        else:
            print("Could NOT find connection!")
            return render_template('menu.html', error="Tars not found!")


class MainPage(MethodView):
    COMMAND_TRIGGER = "command"

    COMMAND_INPUT = "command_input"

    def __init__(self, core_controller: CoreController = None, command_manager: CommandManager = None):
        self.core_controller = core_controller
        self.command_manager = command_manager

    def get(self):
        return render_template('main.html',
                               show_camera_feed=self.core_controller.vision_controller.show_camera)

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
    def __init__(self, core_controller: CoreController = None):
        self.core_controller = core_controller

    def get(self):
        return Response(self.core_controller.vision_controller.gen_frames(),
                        mimetype='multipart/x-mixed-replace; boundary=frame')


class Web:
    def __init__(self, command_manager: CommandManager, core_controller: CoreController):
        self.command_manager = command_manager
        self.core_controller = core_controller

        self.app = Flask(__name__)
        self.app.add_url_rule('/', view_func=MenuPage.as_view('menu', self.core_controller))
        self.app.add_url_rule('/main', view_func=MainPage.as_view('main', self.core_controller, self.command_manager))
        self.app.add_url_rule('/video_feed', view_func=CameraFeed.as_view('camera_feed', self.core_controller))

    def run(self, debug=False, port=5000, **options):
        self.app.run(debug=debug, port=port, use_reloader=False, **options)


if __name__ == '__main__':
    web = Web()
    web.run()
