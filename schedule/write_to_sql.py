#!/usr/bin/env python3

from schedule.VacationSchedule import VacationSchedule

gibberishFile = "~/code/vacation_schedule/schedule/fixtures/gibberish with.xlsx"

def main():
    schedule = VacationSchedule.fromGibberishFile(gibberishFile)
    schedule.toSqlSimple()

if __name__ == "__main__":
    exit(main())
