import pandas
import numpy
import datetime
import os
from dateutil.relativedelta import relativedelta as rd, MO, TU, WE, TH, FR, SA, SU

MONTHS = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec"
]


class VacationSchedule:
    def __init__(self, startDate, endDate):
        """endDate is not included."""
        self._datesToDoctors = {}
        self.startDate = startDate
        self.endDate = endDate

        dt = startDate
        dates = []
        while dt < endDate:
            self._datesToDoctors[dt] = set()
            dt += rd(days=1)

        self._doctorsToDates = {}

    def addDoctorToDate(self, doc, dt):
        if doc in self._datesToDoctors[dt]:
            raise Exception(f"Doctor {doc} is already off on {dt}")

        self._doctorsToDates.setdefault(doc, set()).add(dt)
        self._datesToDoctors[dt].add(doc)

    def removeDoctorFromDate(self, doc, dt):
        if doc not in self._datesToDoctors[dt]:
            raise Exception(
                f"Doctor {doc} is is not off on {dt}, so cannot be removed."
            )

        self._doctorsToDates[doc].remove(dt)
        self._datesToDoctors[dt].remove(doc)

    def swap(self, doctor1, dt1, doctor2, dt2):
        self.removeDoctorFromDate(doctor1, dt1)
        self.removeDoctorFromDate(doctor2, dt2)

        self.addDoctorToDate(doctor1, dt2)
        self.addDoctorToDate(doctor2, dt1)

    def toSqlTable(tableName='call_schedule'):
        NotImplementedError




    def toCsv(self, filepath):
        # Build this up column by column. Then transpose.
        data = []

        # Each column will be a month; the first one has to be padded
        # since we will start with day = 1, regardless of the day number
        # of startDate.
        dt = self.startDate
        numberOfPaddedCells = dt.day - 1
        column = [MONTHS[dt.month-1] + f" {dt.year}"] + numberOfPaddedCells * ['X']

        # Now loop over each date and create a new column when the month changes.
        currMonth = dt.month
        while dt < self.endDate:
            if dt.month != currMonth:
                data.append(column)
                column = [MONTHS[dt.month-1] + f" {dt.year}"]
                currMonth = dt.month
            doctors = self._datesToDoctors[dt]
            column.append(' '.join(doctors))
            dt+=rd(days=1)
        data.append(column)

        # Since the months have differing numbers of days, we have to pad
        # the shorter months with 'X' at the end.
        pad = len(max(data, key=len))
        data = numpy.array([i + ['X']*(pad-len(i)) for i in data])

        # Now prepend the day number column, transpose, and turn into a string.
        data = numpy.r_[[['Day']+list(range(1, 32))], data]
        data = data.T
        data = '\n'.join([','.join([el for el in row]) for row in data])

        with open(filepath, 'w') as f:
            f.write(data)

        return data


class VacationFileParser:
    def __init__(self, filepath):
        self._df = pandas.read_excel(filepath, dtype=str)
        self.startDate = None

        dateColumn = self._df["offweek-mon"]
        nonTrivialDates = dateColumn[~pandas.isna(dateColumn)].tolist()

        currentYear = None
        dt = None
        doctorAssignments = []

        for (ix, row) in self._df.iterrows():
            dtCell = row["offweek-mon"]

            if self._isValidCell(dtCell):
                try:
                    dt = self._getCellDate(row["offweek-mon"], year=currentYear)
                    currentYear = dt.year

                    if self.startDate is None:
                        self.startDate = dt

                    for col in (
                        "off1",
                        "off2",
                        "off3",
                        "off4",
                        "off5",
                        "off6",
                        "off7",
                        "off8",
                    ):
                        cell = row[col]

                        if self._isValidCell(cell):
                            doctors, weekType = self._getDoctorsAndWeekTypeFromCell(
                                row[col]
                            )
                            if len(doctors) > 0:
                                doctorAssignments.append((dt, weekType, doctors))

                except Exception:
                    pass

        self.endDate = dt + rd(weeks=1)
        self.doctorAssignments = doctorAssignments

    def _getCellDate(self, dateCell, year=None):
        components = dateCell.split(" ")

        # No idea.
        if len(components) < 2:
            raise Exception(
                f"Not sure how to figure out the date of row {row}, "
                "since it has less than two 'words'."
            )

        # Ordinary row.
        elif len(components) == 2:
            dateInfo = components[0]
            [_, month, day] = dateInfo.split("-")
            return datetime.datetime.strptime(
                f"{year}-{month}-{day}", "%Y-%m-%d"
            ).date()

        # Must be a year row.
        else:
            year = components[0]
            monthAndDay = components[-1]
            day, month = monthAndDay.split("-")
            return datetime.datetime.strptime(
                f"{year}/{month}/{day}", "%Y/%b/%d"
            ).date()

    def _isValidCell(self, cell):
        return not pandas.isna(cell)

    def _getDoctorsAndWeekTypeFromCell(self, cell):
        cell = cell.strip(" ")

        if cell.endswith("1/2f"):
            weekType = "firstHalf"
            doctors = cell.split("1/2f")[0].split(" ")

        elif cell.endswith("1/2s"):
            weekType = "secondHalf"
            doctors = cell.split("1/2s")[0].split(" ")

        else:
            weekType = "full"
            doctors = cell.split(" ")

        doctorNames = []
        for doctor in doctors:
            doc = doctor.strip(" ")
            if doc != "":
                doctorNames.append(doc)

        return doctorNames, weekType

    def _applyAssignment(self, schedule, monday, weekType, doctors):
        friday = monday + rd(weekday=FR(1))
        wednesday = monday + rd(weekday=WE(1))
        thursday = monday + rd(weekday=TH(1))

        for doctor in doctors:
            dt = monday
            if weekType == "full":
                while dt <= friday:
                    schedule.addDoctorToDate(doctor, dt)
                    dt += rd(days=1)

            elif weekType == "firstHalf":
                while dt < wednesday:
                    schedule.addDoctorToDate(doctor, dt)
                    dt += rd(days=1)
                schedule.addDoctorToDate(doctor + "1", wednesday)

            elif weekType == "secondHalf":
                schedule.addDoctorToDate(doctor + "2", wednesday)
                dt = thursday
                while dt <= friday:
                    schedule.addDoctorToDate(doctor, dt)
                    dt += rd(days=1)
            else:
                raise Exception(f'Invalid weekType {weekType}')

    def getSchedule(self):
        schedule = VacationSchedule(self.startDate, self.endDate)

        for assignment in self.doctorAssignments:
            monday, weekType, doctors = assignment
            self._applyAssignment(schedule, monday, weekType, doctors)

        return schedule
