from threading import Thread

from Web.web import Web
from Function.Core.core_controller import CoreController

CREATE_WEB_SERVER = True

if __name__ == '__main__':
    core_controller = CoreController()
    web = Web(core_controller)
    web_process = Thread(target=web.run)
    if CREATE_WEB_SERVER:
        web_process.start()
    core_controller.run()
    web_process.join()
