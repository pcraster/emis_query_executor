import os


class Configuration:

    # Flask
    SECRET_KEY = os.environ.get("EMIS_QUERY_EXECUTOR_SECRET_KEY") or \
        "yabbadabbadoo!"
    JSON_AS_ASCII = False


    @staticmethod
    def init_app(
            app):
        pass


class DevelopmentConfiguration(Configuration):

    DEBUG = True
    DEBUG_TOOLBAR_ENABLED = True
    FLASK_DEBUG_DISABLE_STRICT = True


    @staticmethod
    def init_app(
            app):
        Configuration.init_app(app)

        from flask_debug import Debug
        Debug(app)


class TestingConfiguration(Configuration):

    TESTING = True


class ProductionConfiguration(Configuration):

    pass


configuration = {
    "development": DevelopmentConfiguration,
    "testing": TestingConfiguration,
    "production": ProductionConfiguration
}
