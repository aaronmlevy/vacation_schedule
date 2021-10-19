import unittest
import tempfile
import MySQLdb
import os
from io import StringIO
import pandas
import pymysql
from schedule.VacationSchedule import VacationSchedule

ownDir = os.path.dirname(os.path.abspath(__file__))

class VacationParserTest(unittest.TestCase):
    def test_toCsvSimpleAndFromCsvSimple(self):
        filepath = os.path.join(ownDir, 'fixtures', 'vac to import to switches.xls')
        filepath = os.path.join('~/code/vacation_schedule/schedule', 'fixtures', 'vac to import to switches.xls')
        schedule = VacationSchedule.fromGibberishFile(filepath)

        csvSimpleFile= tempfile.NamedTemporaryFile()
        schedule.toCsvSimple(csvSimpleFile.name)

        schedule2 = VacationSchedule.fromCsvSimple(csvSimpleFile.name)
        self.assertEqual(schedule, schedule2)

    def test_toCalendarCsvAndFromCalendarCsv(self):
        filepath = os.path.join(ownDir, 'fixtures', 'vac to import to switches.xls')
        schedule = VacationSchedule.fromGibberishFile(filepath)

        calendarFile= tempfile.NamedTemporaryFile()
        schedule.writeAsCalendar(calendarFile.name)

        schedule2 = VacationSchedule.fromCalendar(calendarFile.name)
        self.assertEqual(schedule, schedule2)

    def test_toSqlAndFromSql(self):
        filepath = os.path.join(ownDir, 'fixtures', 'vac to import to switches.xls')
        schedule = VacationSchedule.fromGibberishFile(filepath)
        schedule.toSql(tableName='test')

        schedule2 = VacationSchedule.fromSql(tableName='test')
        self.assertEqual(schedule, schedule2)

