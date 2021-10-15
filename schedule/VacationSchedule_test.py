import unittest
import os
from .vacation_schedule import VacationFileParser

ownDir = os.path.dirname(os.path.abspath(__file__))

class VacationParserTest(unittest.TestCase):
    def test_parseFile(self):
        filepath = os.path.join(ownDir, 'fixtures', 'vac to import to switches.xls')
        parser = VacationFileParser(filepath)
        schedule = parser.getSchedule()
        schedule.toCsv('test2.csv')
