import unittest
import tempfile
import os

from .VacationSchedule import VacationSchedule

ownDir = os.path.dirname(os.path.abspath(__file__))

class VacationParserTest(unittest.TestCase):
    def test_toCsvSimpleAndFromCsvSimple(self):
        filepath = os.path.join(ownDir, 'fixtures', 'vac to import to switches.xls')
        schedule = VacationSchedule.fromGibberishFile(filepath)

        csvSimpleFile= tempfile.NamedTemporaryFile()
        schedule.toCsvSimple(csvSimpleFile.name)

        schedule2 = VacationSchedule.fromCsvSimple(csvSimpleFile.name)
        self.assertEqual(schedule, schedule2)
