
class WatcherConfig():

    def __init__(self, config_data) -> None:
        self.config_data = config_data

    def get_config(self, key):
            return self.config_data[key]

    def is_valid_file_config(self, file_config):
        return True if "watchPath" in file_config and "destinationPath" in file_config else False

    def is_valid_queue_config(self, queue_config):
        if ("notifyCreate" in queue_config and "connnectionConfig" in queue_config) and ("exchangeName" in queue_config["notifyCreate"] and "routingKey" in queue_config["notifyCreate"]):
            return True
        
        return False

    def validate(self):
        if not isinstance(self.config_data, dict):
            raise Exception("Given config data is not valid json. Please provide valid json data.")
        
        if "fileConfig" not in self.config_data or "queueConfig" not in self.config_data or not self.is_valid_file_config(self.config_data["fileConfig"]) or not self.is_valid_queue_config(self.config_data["queueConfig"]):
            raise Exception("Invalid watcher config.")