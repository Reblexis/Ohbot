from multiprocessing import Process

from Web.web import Web
from Function.Core.core_controller import CoreController

if __name__ == '__main__':
    core_controller = CoreController()
    web = Web(core_controller)
    web_process = Process(target=web.run)
    web_process.start()
    core_controller.run()
    web_process.join()
