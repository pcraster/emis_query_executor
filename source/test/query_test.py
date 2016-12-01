import unittest
from flask import current_app, json
from query_executor import create_app


class QueryTest(unittest.TestCase):

    def setUp(self):
        self.app = create_app("testing")
        self.app_context = self.app.app_context()

        self.app_context.push()

        self.client = self.app.test_client()


    def tearDown(self):
        self.app_context.pop()


    def test_query(self):
        response = self.client.get("/queries")
        data = response.data.decode("utf8")

        self.assertEqual(response.status_code, 200, data)

        data = json.loads(data)

        self.assertTrue("queries" in data)

        queries = data["queries"]

        self.assertTrue("query_groups" in queries)

        query_groups = queries["query_groups"]

        self.assertTrue(isinstance(query_groups, list))

        for query_group in query_groups:
            print query_group




        self.assertTrue("aggregate_queries" in queries)

        aggregate_queries = queries["aggregate_queries"]

        self.assertTrue(isinstance(aggregate_queries, list))
        self.assertEqual(len(aggregate_queries), 0)


        self.assertTrue("subset_queries" in queries)

        subset_queries = queries["subset_queries"]

        self.assertTrue(isinstance(subset_queries, list))
        self.assertEqual(len(subset_queries), 0)


if __name__ == "__main__":
    unittest.main()
