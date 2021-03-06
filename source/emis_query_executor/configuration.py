import os
import tempfile


class Configuration:

    # EMIS_HOST = "emis"
    EMIS_AGGREGATE_QUERY_HOST = "emis_aggregate_query"
    EMIS_DOMAIN_HOST = "emis_domain"
    EMIS_PROPERTY_HOST = "emis_property"
    EMIS_RESULT_DATA = \
        os.environ.get("EMIS_RESULT_DATA") or \
        tempfile.gettempdir()
    EMIS_RABBITMQ_DEFAULT_USER = os.environ.get("EMIS_RABBITMQ_DEFAULT_USER")
    EMIS_RABBITMQ_DEFAULT_PASS = os.environ.get("EMIS_RABBITMQ_DEFAULT_PASS")
    EMIS_RABBITMQ_DEFAULT_VHOST = os.environ.get("EMIS_RABBITMQ_DEFAULT_VHOST")


    @staticmethod
    def init_app(
            app):
        pass


class DevelopmentConfiguration(Configuration):

    # EMIS_PORT = 5000
    EMIS_AGGREGATE_QUERY_PORT = 5000
    EMIS_DOMAIN_PORT = 5000
    EMIS_PROPERTY_PORT = 5000


class TestConfiguration(Configuration):

    # EMIS_PORT = 5000
    EMIS_AGGREGATE_QUERY_PORT = 5000
    EMIS_DOMAIN_PORT = 5000
    EMIS_PROPERTY_PORT = 5000


class ProductionConfiguration(Configuration):

    # EMIS_PORT = 3031
    EMIS_AGGREGATE_QUERY_PORT = 3031
    EMIS_DOMAIN_PORT = 3031
    EMIS_PROPERTY_PORT = 3031


configuration = {
    "development": DevelopmentConfiguration,
    "test": TestConfiguration,
    "acceptance": ProductionConfiguration,
    "production": ProductionConfiguration
}
