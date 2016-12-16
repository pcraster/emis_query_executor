import sys
import time
from flask import Config
import pika
import requests
from .configuration import configuration


class QueryExecutor(object):

    def __init__(self):
        self.config = Config(__name__)


    # def properties_uri(self,
    #         route):
    #     return "http://{}:{}/{}".format(
    #         self.config["EMIS_PROPERTY_HOST"],
    #         self.config["EMIS_PROPERTY_PORT"],
    #         route)


    def on_message(self,
            channel,
            method_frame,
            header_frame,
            body):

        # Message passed in is the uri to the query to execute.

        sys.stdout.write("received message: {}".format(body))
        sys.stdout.flush()


        try:
            # Get the query.
            uri = body
            response = requests.get(uri)

            assert response.status_code == 200, response.text

            query = response.json()["aggregate_query"]

            assert query["edit_status"] == "final", query["edit_status"]
            assert query["execute_status"] == "queued", query["execute_status"]

            # Mark executing query as 'executing'.
            payload = {
                "execute_status": "executing"
            }
            response = requests.patch(uri, json=payload)

            assert response.status_code == 200, response.text

            query = response.json()["aggregate_query"]


            # Mark executing query as 'executing'.
            # print(type)
            # print(body)
            # print(dir(body))
            # assert(False)


            # uri = self.properties_uri("properties")
            # response = requests.post(uri, json={"property": payload})


            time.sleep(5)

            # # For now, post an example to the property service.
            # payload = {
            #     "name": "my_name1",
            #     "pathname": "my_pathname1"
            # }
            # uri = self.properties_uri("properties")
            # response = requests.post(uri, json={"property": payload})

            # # TODO Handle errors.
            # assert response.status_code == 201, response.text


            # Mark executing query as 'succeeded'.
            payload = {
                "execute_status": "succeeded"
            }
            response = requests.patch(uri, json=payload)

            assert response.status_code == 200, response.text

        except Exception:

            # Mark executing query as 'failed'.
            payload = {
                "execute_status": "failed"
            }
            response = requests.patch(uri, json=payload)

            assert response.status_code == 200, response.text


        channel.basic_ack(delivery_tag=method_frame.delivery_tag)


    def run(self,
            host):

        self.credentials = pika.PlainCredentials(
            self.config["EMIS_RABBITMQ_DEFAULT_USER"],
            self.config["EMIS_RABBITMQ_DEFAULT_PASS"]
        )
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host="rabbitmq",
            virtual_host=self.config["EMIS_RABBITMQ_DEFAULT_VHOST"],
            credentials=self.credentials,
            # Keep trying for 8 minutes.
            connection_attempts=100,
            retry_delay=5  # Seconds
        ))
        self.channel = self.connection.channel()
        self.channel.queue_declare(
            queue="execute_query")
        self.channel.basic_consume(
            self.on_message,
            queue="execute_query")

        try:
            sys.stdout.write("Start consuming...")
            sys.stdout.flush()
            self.channel.start_consuming()
        except KeyboardInterrupt:
            self.channel.stop_consuming()

        sys.stdout.write("Close connection...")
        sys.stdout.flush()
        self.connection.close()


def create_app(
        configuration_name):

    app = QueryExecutor()

    configuration_ = configuration[configuration_name]
    app.config.from_object(configuration_)
    configuration_.init_app(app)

    return app
