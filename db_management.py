import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DBNAME = os.path.join(BASE_DIR, 'asude.sqlite3')

class DataManagement():
    def __init__(self, dbname=DBNAME):
        print(dbname)
        self.db = sqlite3.connect(dbname)
        self.cursor = self.db.cursor()

    def __del__(self):
        self.db.close()

    def check(self, url, source):
        query = 'select * from urls where url="{url}" and source="{source}"'.format(url=url, source=source)
        one = self.cursor.execute(query)
        return one.fetchone()

    def add_new_url(self, url, source):
        query = 'INSERT INTO urls (url, source) values ("{url}", "{source}")'.format(url=url, source=source)
        self.cursor.execute(query)
        self.db.commit()

        return True

    def get_statistics(self):
        query = 'select source, count(*) from urls group by source'
        statistics = self.cursor.execute(query)

        counts = {}

        for source, count in statistics.fetchall():
            counts[source] = count

        return counts

