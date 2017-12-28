import unittest

import os

from data.sqlite.RepairsDatabase import RepairsDatabase

DB_URL = 'sqlite:///test_db.db'


class TestsWithDb(unittest.TestCase):
    def setUp(self):
        self.db = RepairsDatabase(DB_URL)

    def testCreateDatabase_canExecuteMultipleTimes(self):
        RepairsDatabase(DB_URL)
        RepairsDatabase(DB_URL)

    def tearDown(self):
        os.remove("test_db.db")
