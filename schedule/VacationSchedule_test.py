import unittest
import os
from .vacation_schedule import VacationFileParser

ownDir = os.path.dirname(os.path.abspath(__file__))

class VacationParserTest(unittest.TestCase):
    def test_parseFile(self):
        filepath = os.path.join(ownDir, 'fixtures', 'vac to import to switches.xls')
        parser = VacationFileParser(filepath)
        schedule = parser.getSchedule()

        parentDir = os.path.dirname(os.path.join(ownDir))
        csvPath = os.path.join(parentDir, 'csv_outputs', 'test3.csv')
        schedule.writeCsv(csvPath)

    def test_toSql(self):
        filepath = os.path.join(ownDir, 'fixtures', 'vac to import to switches.xls')
        parser = VacationFileParser(filepath)
        schedule = parser.getSchedule()
        import pdb; pdb.set_trace()
        schedule

