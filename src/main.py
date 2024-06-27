import json, os, time
import logging.config
from helpers.WatcherConfig import WatcherConfig
from handlers.WatchDog import WatchDog
from watchdog import observers
from helpers.Logger import LOGGING_CONFIG
from handlers.RmqHandler import Rmq


logging.config.dictConfig(LOGGING_CONFIG)

class Watcher():

    def __init__(self, config_path: str) -> None:
        self.config_path = config_path
        self.logger = logging.getLogger("xmlc-watcher")

    def watch(self, observer) -> None:
        try:
            while True:
                time.sleep(0.25)
        except SystemExit:
            observer.stop()
        except KeyboardInterrupt:
            observer.stop()
        finally:
            observer.join()
            self.logger.info("Stoped XMLC central folder watcher")

    def initiate_watcher(self, watcher_config):

        logging.getLogger("watchdog.observers.inotify_buffer").setLevel("WARN") 

        watch_path = watcher_config.get_config("fileConfig")
        
        rmq_cls = Rmq(watcher_config.get_config("queueConfig"))
        is_connected = rmq_cls.connect()

        if is_connected:
            event_handler = WatchDog(watcher_config, rmq_cls)
            observer = observers.Observer()
            observer.schedule(event_handler, path=watch_path["watchPath"], recursive=True)
            observer.start()

            self.logger.info("Started watching the folder path %s", watch_path["watchPath"])

            return observer

    def main(self):
        self.logger.info("Initiating XML Central XMLC Folder watcher...")
        with open(self.config_path) as f:
            config_data = json.loads(f.read())

        watcher_config = WatcherConfig(config_data)
        watcher_config.validate()

        return self.initiate_watcher(watcher_config)

if __name__ == "__main__":
    config_path = "../config/watcher.json"

    if not os.path.exists(config_path):
        raise Exception("Watcher config file not found in the path %s ."%(config_path))
    
    watcher_obj = Watcher(config_path)
    observer = watcher_obj.main()
    watcher_obj.watch(observer)
    
