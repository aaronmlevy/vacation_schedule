import os

from flask import Flask, request, render_template, jsonify
from flaskext.mysql import MySQL
import pymysql

from schedule.VacationSchedule import VacationSchedule

app = Flask(__name__)
ownDir = os.path.dirname(os.path.abspath(__file__))

mysql = MySQL()

app.config["MYSQL_DATABASE_USER"] = "root"
app.config["MYSQL_DATABASE_PASSWORD"] = ""
app.config["MYSQL_DATABASE_DB"] = "schedule_db"
app.config["MYSQL_DATABASE_HOST"] = "localhost"
mysql.init_app(app)


@app.route("/")
def home():
    try:
        csvSimpleDir = os.path.dirname(ownDir)
        # conn = mysql.connect()
        csvSimpleFile = os.path.join(csvSimpleDir, "calendar", "calendar.csv")
        print(f"csvSimpleFile: {csvSimpleFile}")
        vacationSchedule = VacationSchedule.fromCsvSimple(csvSimpleFile)

        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * from call_schedule order by date")
        schedule = cursor.fetchall()
        print(f"schedule: {schedule}")
        return render_template("index.html", schedule=schedule)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route("/update", methods=["POST", "GET"])
def update():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        if request.method == "POST":
            date = request.form["field"]
            docName = request.form["value"]
            location = request.form["id"]

            sql = f"UPDATE call_schedule SET {location}='{docName}' WHERE date=DATE('{date}')"

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql)
            conn.commit()
            success = 1
        return jsonify(success)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    app.run()
