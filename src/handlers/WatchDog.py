import logging
from watchdog.events import PatternMatchingEventHandler
from handlers.FileHandler import FileHandler
from handlers.RmqHandler import Rmq
from datetime import datetime

 
class WatchDog(PatternMatchingEventHandler):
    def __init__(self, watcher_config_cls, rmq_cls):
        PatternMatchingEventHandler.__init__(self, patterns=['*.txt'], ignore_directories=True, case_sensitive=False)
        self.logger = logging.getLogger("xmlc-watcher.%s" % (__name__))
        self.file_handler_obj = FileHandler(watcher_config_cls.get_config("fileConfig"))
        self.rmq_cls = rmq_cls
        self.workflows = watcher_config_cls.get_config("workFlows")


    def on_created(self, event):
        self.logger.info("Watchdog received created event - % s" % event.src_path)

        is_file_copied, article_info = self.file_handler_obj.validate_and_process(event.src_path)

        if is_file_copied:
            body_msg = {
                    "jobFlow": {
                        "name": self.workflows
                    },
                    "journal": {
                        "jid": [article_info["jid"]]
                    },
                    "articleId": [article_info["aid"].upper()],
                    "receivedDate": str(datetime.now())
                }
            self.rmq_cls.publish_message(body_msg)

 
    # def on_modified(self, event):
    #     print("Watchdog received modified event - % s" % event.src_path)
 