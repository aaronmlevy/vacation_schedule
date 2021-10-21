import os
import datetime

from flask import Flask, request, render_template, jsonify, url_for, session, redirect
from flaskext.mysql import MySQL
import pymysql

from schedule.VacationSchedule import VacationSchedule
ownDir = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
ownDir = os.path.dirname(os.path.abspath(__file__))
logfile_path = os.path.join(os.path.dirname(ownDir), 'log', 'log.txt')

mysql = MySQL()

app.config["MYSQL_DATABASE_USER"] = "pi"
app.config["MYSQL_DATABASE_PASSWORD"] = ""
app.config["MYSQL_DATABASE_DB"] = "vacation_schedule_db"
app.config["MYSQL_DATABASE_HOST"] = "localhost"
app.secret_key = "super secret key"
mysql.init_app(app)


@app.route("/")
def redirectToSignin():
    return redirect(url_for("sign_in"))

@app.route("/vacation_schedule")
def vacation_schedule():
    if "USERNAME" not in session:
        return redirect(url_for("sign_in"))
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * from vacation_schedule")
        schedule = cursor.fetchall()

        if len(schedule) > 0:
            columnNames = list(schedule[0].keys())
            columnNames = columnNames[1:]

        return render_template(
            "index.html",
            schedule=schedule,
            columnNames=columnNames,
            numColumns=len(columnNames),
        )

    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route("/sign_in", methods=["GET", "POST"])
def sign_in():
    if request.method == "POST":
        req = request.form
        name = req.get("username")
        session["USERNAME"] = name
        return redirect(url_for("vacation_schedule"))

    return render_template("sign_in.html")


@app.route("/vacation_schedule/update", methods=["POST", "GET"])
def update():
    user = session["USERNAME"]

    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        if request.method == "POST":
            date = request.form["field"]
            newDoctorList = request.form["value"]
            oldDoctorList = getOldDoctorListOnDate(date, cursor)
            success = updateSqlDatabase(newDoctorList, oldDoctorList, date, user, cursor)
        return jsonify(success)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


def getOldDoctorListOnDate(date, cursor):
    sql = f"select * from vacation_schedule WHERE date='{date}';"
    cursor.execute(sql)

    counter = 0
    for row in cursor:
        oldDoctorList = row["doctors"]
        counter += 1
    assert counter == 1

    return oldDoctorList


def updateSqlDatabase(newDoctorList, oldDoctorList, date, user, cursor):
    sql = f"UPDATE vacation_schedule SET doctors='{newDoctorList}' WHERE date='{date}';"
    with open(logfile_path, "a") as f:
        f.write(
            "==========================================\n"
            f"======= {datetime.datetime.now()} =======\n"
            "==========================================\n"
            f"User {user} changed {date} from\n"
            f"'{oldDoctorList}' to\n'{newDoctorList}'\n\n"
        )

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    return True


if __name__ == "__main__":
    app.run(host = '0.0.0.0', port=5000)
