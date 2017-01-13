import unittest
from emis_query_executor import create_app


class AppTest(unittest.TestCase):

    def setUp(self):
        self.app = create_app("testing")


    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()
