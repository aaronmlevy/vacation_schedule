import datetime
from flask import Flask, request, render_template, jsonify, url_for, session, redirect
from flaskext.mysql import MySQL
import pymysql
import os
from waitress import serve

from git_util import Git
from schedule.VacationSchedule import VacationSchedule


app = Flask(__name__)

ownDir = os.path.dirname(os.path.abspath(__file__))
logRepoRoot = os.path.join(os.path.dirname(os.path.dirname(ownDir)), "log")
logFilepath = os.path.join(logRepoRoot, "schedule.csv")

git = Git(logRepoRoot)

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
        cursor.execute("select * from vacation_schedule;")
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
            # Get the date that changed.
            date = request.form["field"]

            # Get old assignments on that date.
            sql = f"select * from vacation_schedule where date='{date}';"
            cursor.execute(sql)
            row = cursor.fetchone()
            oldDoctorList = row['doctors']

            # Set new assignments on date.
            newDoctorList = request.form["value"]
            sql = (
                f"update vacation_schedule set doctors='{newDoctorList}' where date='{date}';"
            )
            cursor.execute(sql)
            conn.commit()

            # Commit new table to log repo.
            commitMessage = (
                f"CHANGE: User '{user}' changed date '{date}' "
                f"from '{oldDoctorList}' to '{newDoctorList}'."
            )
            commitTableToLog(logFilepath, commitMessage)
            success = True

        return jsonify(success)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


def commitTableToLog(writePath, commitMessage):
    schedule = VacationSchedule.fromSqlSimple()
    schedule.toCsvSimple(writePath)
    git.add(writePath)
    git.commit(withMessage=commitMessage)


if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=5000)
