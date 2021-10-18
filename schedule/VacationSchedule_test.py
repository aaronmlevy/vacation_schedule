import unittest
import tempfile
import os

from .VacationSchedule import VacationSchedule

ownDir = os.path.dirname(os.path.abspath(__file__))

class VacationParserTest(unittest.TestCase):
    def test_parseFile(self):
        filepath = os.path.join(ownDir, 'fixtures', 'vac to import to switches.xls')
        schedule = VacationSchedule.fromGibberishFile(filepath)

        parentDir = os.path.dirname(os.path.join(ownDir))
        csvPath = os.path.join(parentDir, 'csv_outputs', 'test3.csv')
        schedule.toCsvSimple(csvPath)

    def test_toCsvSimpleAndFromCsvSimple(self):
        filepath = os.path.join(ownDir, 'fixtures', 'vac to import to switches.xls')
        schedule = VacationSchedule.fromGibberishFile(filepath)

        csvSimpleFile= tempfile.NamedTemporaryFile()
        schedule.toCsvSimple(csvSimpleFile.name)

        schedule2 = VacationSchedule.fromCsvSimple(csvSimpleFile.name)
        self.assertEqual(schedule, schedule2)


    # def test_toSql(self):
        # filepath = os.path.join(ownDir, 'fixtures', 'vac to import to switches.xls')
        # schedule = VacationSchedule.fromGibberishFile(filepath)
        # import pdb; pdb.set_trace()
        # csvString = schedule.asCsvString()
        # csvRows = csvString.split('\n')
        # headers = csvRows[0].split(',')
        # monthNames = headers[1:]
        # tableName = 'vacation_schedule'

        # createTableQueryComponents = [f"CREATE TABLE `{tableName}` ("] 
        # createTableQueryComponents.extendappend([f"`{monthName}` varchar(255) NOT NULL" for monthName in monthNames])
        # createTableQueryComponents.append(") ENGINE=MyISAM DEFAULT CHARSET=latin1;")
        # createTableQuery = ' '.join(createTableQueryComponents)




