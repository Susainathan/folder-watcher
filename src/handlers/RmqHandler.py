import pika, logging, json
from datetime import datetime


class Rmq():

    channel = None
    connection = None

    def __init__(self, queue_config) -> None:
        self.logger = logging.getLogger("xmlc-watcher.%s" % (__name__))
        self.host = queue_config["connnectionConfig"]["host"]
        self.username = queue_config["connnectionConfig"]["username"]
        self.password = queue_config["connnectionConfig"]["password"]
        self.port = queue_config["connnectionConfig"]["port"]
        self.vhost = queue_config["connnectionConfig"]["vhost"]
        self.queue_detail_to_publish = queue_config["notifyCreate"]

    def connect(self):
        self.logger.info("Invoking RMQ connection...")
        try:
            if not self.connection :
                credentials = pika.PlainCredentials(self.username, self.password)
                parameters = pika.ConnectionParameters(self.host, self.port, self.vhost, credentials)
                self.connection = pika.BlockingConnection(parameters)
                self.channel = self.connection.channel()
            else:
                self.channel = self.connection.channel()
            return True
        except Exception as e:
            self.logger.error("Unable to connected with RMQ. RMQ Connection not establised!", stack_info=True)
            return False
        finally:
            self.logger.info("RMQ connection established!")

    def publish_message(self, body_msg):
        try:
            self.channel.basic_publish(exchange=self.queue_detail_to_publish["exchangeName"],
                        routing_key=self.queue_detail_to_publish["routingKey"],
                        body=json.dumps(body_msg))
            
            self.logger.info("Message published to Nimble")
        except Exception as e:
            self.logger.error("Unable to publish message to RMQ :%s",e, stack_info=True)

    
    def close_rmq(self):
        if self.connection and self.connection.is_open:
            self.connection.close()