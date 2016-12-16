import os


class Configuration:

    @staticmethod
    def init_app(
            app):
        pass


class DevelopmentConfiguration(Configuration):

    pass


class TestingConfiguration(Configuration):

    pass


class ProductionConfiguration(Configuration):

    pass


configuration = {
    "development": DevelopmentConfiguration,
    "testing": TestingConfiguration,
    "production": ProductionConfiguration
}
