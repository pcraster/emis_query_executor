import datetime
import json
import os
import sys
import traceback
from flask import Config
import pika
import requests
from emis.aggregate import coordinate_lookup
from .configuration import configuration


class QueryExecutor(object):

    def __init__(self):
        self.config = Config(__name__)


    def domains_uri(self,
            route):
        route = route.lstrip("/")
        return "http://{}:{}/{}".format(
            self.config["EMIS_DOMAIN_HOST"],
            self.config["EMIS_DOMAIN_PORT"],
            route)

    def properties_uri(self,
            route):
        route = route.lstrip("/")
        return "http://{}:{}/{}".format(
            self.config["EMIS_PROPERTY_HOST"],
            self.config["EMIS_PROPERTY_PORT"],
            route)


    # def emis_aggregate_query_results_uri(self,
    #         route):
    #     route = route.lstrip("/")
    #     return "https://{}:{}/aggregate_query_results/{}".format(
    #         self.config["EMIS_HOST"],
    #         self.config["EMIS_PORT"],
    #         route)


    def aggregate_queries_uri(self,
            route):
        route = route.lstrip("/")
        return "http://{}:{}/{}".format(
            self.config["EMIS_AGGREGATE_QUERY_HOST"],
            self.config["EMIS_AGGREGATE_QUERY_PORT"],
            route)


    def log(self,
            message,
            priority="low",
            severity="non_critical"):

        try:

            payload = {
                "timestamp": datetime.datetime.utcnow().isoformat(),
                "priority": priority,
                "severity": severity,
                "message": message
            }

            # Post message in rabbitmq and be done with it.
            credentials = pika.PlainCredentials(
                self.config["EMIS_RABBITMQ_DEFAULT_USER"],
                self.config["EMIS_RABBITMQ_DEFAULT_PASS"]
            )

            connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host="rabbitmq",
                    virtual_host=self.config[
                        "EMIS_RABBITMQ_DEFAULT_VHOST"],
                    credentials=credentials)
            )
            channel = connection.channel()

            properties = pika.BasicProperties()
            properties.content_type = "application/json"
            properties.durable = False

            channel.basic_publish(
                exchange="alerts",
                properties=properties,
                routing_key="{}.{}".format(priority, severity),
                body=json.dumps(payload)
            )
            connection.close()

        except Exception as exception:

            sys.stderr.write("Error while sending log message to broker\n")
            sys.stderr.write("Log message: {}\n".format(message))
            sys.stderr.write("Error message: {}\n".format(str(exception)))
            sys.stderr.write("{}\n".format(traceback.format_exc()))
            sys.stderr.flush()



    def relative_result_dataset_pathname(self,
            query):
        # TODO Format a nice name.
        return os.path.join(query["user"], query["id"], "query_result.csv")


    def result_dataset_pathname(self,
            query):
        dataset_pathname = os.path.join(
            self.config["EMIS_RESULT_DATA"],
            self.relative_result_dataset_pathname(query))

        # Make sure the path to the dataset exists.
        directory_pathname = os.path.split(dataset_pathname)[0]
        os.makedirs(directory_pathname)

        return dataset_pathname


    def handle_error(self,
            query_uri,
            query_id,
            message):

        self.log("calculation failed\n{}".format(
                traceback.format_exc()),
            priority="high", severity="critical")

        # Mark executing query as 'failed'.
        payload = {
            "execute_status": "failed"
        }
        response = requests.patch(query_uri, json=payload)

        assert response.status_code == 200, response.text


        # Post error message for the client.
        messages_uri = self.aggregate_queries_uri(
            "aggregate_query_messages")
        payload = {
            "id": query_id,
            "message": message,
        }

        response = requests.post(messages_uri,
            json={"aggregate_query_message": payload})

        assert response.status_code == 201, response.text


    def on_message(self,
            channel,
            method_frame,
            header_frame,
            body):

        # Message passed in is the uri to the query to execute.

        self.log("received message: {}\n".format(body))

        try:
            # Get the query.
            query_uri = body
            response = requests.get(query_uri)

            assert response.status_code == 200, response.text

            query = response.json()["aggregate_query"]
            skip_query = False

            if query["edit_status"] != "final":
                self.log(
                    "Skipping query because 'edit_status' is not 'final', "
                        "but '{}'".format(query["edit_status"]),
                    priority="high")
                skip_query = True
            elif query["execute_status"] != "queued":
                self.log(
                    "Skipping query because 'execute_status' is not 'queued', "
                        "but '{}'".format(query["execute_status"]),
                    priority="high")
                skip_query = True


            if not skip_query:
                assert query["edit_status"] == "final", query["edit_status"]
                assert query["execute_status"] == "queued", \
                    query["execute_status"]

                # Mark executing query as 'executing'.
                payload = {
                    "execute_status": "executing"
                }
                response = requests.patch(query_uri, json=payload)

                assert response.status_code == 200, response.text

                query = response.json()["aggregate_query"]
                model = query["model"]["aggregate_query"]
                domain_uri = self.domains_uri(model["domain"])
                property_uris = [self.properties_uri(uri) for uri in
                    model["properties"]]

                response = requests.get(domain_uri)
                assert response.status_code == 200, response.text
                domain_pathname = response.json()["domain"]["pathname"]

                property_pathnames = []
                for property_uri in property_uris:
                    response = requests.get(property_uri)
                    assert response.status_code == 200, response.text
                    property = response.json()["property"]
                    property_pathnames.append(
                        (property["pathname"], property["name"]))


                sys.stdout.write("{}\n".format(domain_pathname))
                sys.stdout.write("{}\n".format(property_pathnames))
                sys.stdout.flush()


                # Pathname of file to store result in.
                result_pathname = self.result_dataset_pathname(query)

                # Calculate the result.
                coordinate_lookup(
                    domain_pathname, result_pathname, property_pathnames)

                # Store information about the result in emis_result.
                results_uri = self.aggregate_queries_uri(
                    "aggregate_query_results")
                payload = {
                    "id": query["id"],
                    "uri": self.relative_result_dataset_pathname(query)
                        # self.emis_aggregate_query_results_uri(
                        # self.relative_result_dataset_pathname(query))
                }

                response = requests.post(results_uri,
                    json={"aggregate_query_result": payload})

                assert response.status_code == 201, response.text


                # Mark executing query as 'succeeded'.
                payload = {
                    "execute_status": "succeeded"
                }
                response = requests.patch(query_uri, json=payload)

                assert response.status_code == 200, response.text

                self.log("calculation succeeded")

        except RuntimeError as exception:
            error_message = str(exception)
            self.handle_error(query_uri, query["id"], error_message)

        except Exception as exception:
            error_message = "Something went wrong. Please try again later."
            self.handle_error(query_uri, query["id"], error_message)

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
            sys.stdout.write("Start consuming...\n")
            sys.stdout.flush()
            self.channel.start_consuming()
        except KeyboardInterrupt:
            self.channel.stop_consuming()

        sys.stdout.write("Close connection...\n")
        sys.stdout.flush()
        self.connection.close()


def create_app(
        configuration_name):

    app = QueryExecutor()

    configuration_ = configuration[configuration_name]
    app.config.from_object(configuration_)
    configuration_.init_app(app)

    return app
