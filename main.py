from threading import Thread

from Web.web import Web
from Function.Core.command_manager import CommandManager
from Function.Core.core_controller import CoreController

CREATE_WEB_SERVER = True

if __name__ == '__main__':
    command_manager = CommandManager()
    core_controller = CoreController(command_manager)
    command_manager.initialize_core_controller(core_controller)
    web = Web(command_manager, core_controller)
    web_process = Thread(target=web.run)
    if CREATE_WEB_SERVER:
        web_process.start()
    core_controller.run()
    web_process.join()
