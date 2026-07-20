import duckdb


class Database:

    def __init__(self):

        self.connection = duckdb.connect(
            "data/flights.duckdb"
        )

    def create_tables(self):

        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS flights (

                searched_at TIMESTAMP,

                search_id TEXT,

                airline TEXT,
                departure TEXT,
                arrival TEXT,

                duration TEXT,
                route TEXT,
                stops TEXT,

                price INTEGER
            )
        """)

    def execute(self, query, params=None):

        if params:
            return self.connection.execute(query, params)

        return self.connection.execute(query)