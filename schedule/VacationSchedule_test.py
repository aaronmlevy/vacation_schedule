import unittest
import tempfile
import datetime
import os
import pymysql
from schedule.VacationSchedule import VacationSchedule, _VacationFileParser

ownDir = os.path.dirname(os.path.abspath(__file__))


class VacationParserTest(unittest.TestCase):
    def test_toCsvSimpleAndFromCsvSimple(self):
        filepath = os.path.join(ownDir, "fixtures", "gibberish with.xlsx")
        schedule = VacationSchedule.fromGibberishFile(filepath)

        csvSimpleFile = tempfile.NamedTemporaryFile()
        schedule.toCsvSimple(csvSimpleFile.name)

        schedule2 = VacationSchedule.fromCsvSimple(csvSimpleFile.name)
        self.assertEqual(schedule, schedule2)

    def test_toCalendarCsvAndFromCalendarCsv(self):
        filepath = os.path.join(ownDir, "fixtures", "gibberish with.xlsx")
        schedule = VacationSchedule.fromGibberishFile(filepath)

        calendarFile = tempfile.NamedTemporaryFile()
        schedule.writeAsCalendar(calendarFile.name)

        schedule2 = VacationSchedule.fromCalendar(calendarFile.name)
        self.assertEqual(schedule, schedule2)

    def test_toSqlAndFromSql(self):
        filepath = os.path.join(ownDir, "fixtures", "gibberish with.xlsx")
        schedule = VacationSchedule.fromGibberishFile(filepath)
        schedule.toSql(tableName="test")

        schedule2 = VacationSchedule.fromSql(tableName="test")
        self.assertEqual(schedule, schedule2)

        connection = pymysql.connect(host='localhost', user='root', passwd='', db='vacation_schedule_db')
        cursor = connection.cursor()
        cursor.execute('drop table test;')

    def test_toSqlSimpleAndFromSqlSimple(self):
        filepath = os.path.join(ownDir, "fixtures", "gibberish with.xlsx")
        schedule = VacationSchedule.fromGibberishFile(filepath)
        schedule.toSqlSimple(tableName="test")

        schedule2 = VacationSchedule.fromSqlSimple(tableName="test")
        self.assertEqual(schedule, schedule2)

        connection = pymysql.connect(host='localhost', user='root', passwd='', db='vacation_schedule_db')
        cursor = connection.cursor()
        cursor.execute('drop table test;')

    def test_parsingNumbersInNames(self):
        filepath = os.path.join(ownDir, "fixtures", "gibberish with.xlsx")

        schedule = VacationSchedule.fromGibberishFile(filepath)

        self.assertIn("ag", schedule._datesToDoctors[datetime.date(2020, 11, 16)])
        self.assertIn("ag", schedule._datesToDoctors[datetime.date(2020, 11, 25)])
        self.assertIn("ag", schedule._datesToDoctors[datetime.date(2020, 12, 17)])
        self.assertIn("ag", schedule._datesToDoctors[datetime.date(2020, 12, 21)])
        self.assertIn("ag", schedule._datesToDoctors[datetime.date(2020, 12, 22)])
        self.assertIn("ag", schedule._datesToDoctors[datetime.date(2020, 12, 23)])
        self.assertIn("ag", schedule._datesToDoctors[datetime.date(2020, 12, 28)])
        self.assertIn("ag", schedule._datesToDoctors[datetime.date(2020, 12, 29)])
        self.assertIn("ag", schedule._datesToDoctors[datetime.date(2020, 12, 30)])
        self.assertIn("ag", schedule._datesToDoctors[datetime.date(2021, 1, 4)])
        self.assertIn("ag", schedule._datesToDoctors[datetime.date(2021, 1, 11)])
        self.assertIn("ag", schedule._datesToDoctors[datetime.date(2021, 2, 1)])
        self.assertIn("ag", schedule._datesToDoctors[datetime.date(2021, 2, 15)])
        self.assertIn("ag", schedule._datesToDoctors[datetime.date(2021, 2, 24)])
        self.assertIn("ag", schedule._datesToDoctors[datetime.date(2021, 3, 22)])

    def test_readCell(self):
        res = _VacationFileParser.readCell("ag22/24pm/25/29/30/31")
        expected = dict(ag=[22, 24], pm=[25, 29, 30, 31])
        self.assertEqual(res, expected)

        res = _VacationFileParser.readCell("ag/15/24*/")
        expected = dict(ag=[15, 24])
        self.assertEqual(res, expected)

        res = _VacationFileParser.readCell("ag 1/5")
        expected = dict(ag=[1, 5])
        self.assertEqual(res, expected)

        res = _VacationFileParser.readCell("tn 4")
        expected = dict(tn=[4])
        self.assertEqual(res, expected)

