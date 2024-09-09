from flask import Flask, render_template, request, redirect
from pymysql import MySQLError

from sql import get_conn, create_tables

app = Flask(__name__)

@app.route("/")
def root():
    return render_template("index.html")

@app.route("/show")
def show():
    conn = get_conn()
    cur = conn.cursor()
    contacts = []

    try:
        cur.execute("SELECT * FROM agenda;")
        contacts = cur.fetchall()
    except MySQLError as e:
        print(e)
    finally:
        cur.close()
        conn.close()

    return render_template("out.html", contacts=contacts)

@app.route("/add", methods=["POST"])
def add():
    if request.method != "POST":
        return 404

    firstName = request.form["name"]
    lastName = request.form["lastname"]

    connection = get_conn()
    cursor = connection.cursor()

    try:
        cursor.execute("INSERT INTO agenda (name, lastname) VALUES (%s, %s)", (firstName, lastName))
        connection.commit()
    except MySQLError as e:
        print(e)
        return "Error:(",400
    finally:
        cursor.close()
        connection.close()

    return redirect("show")

@app.route("/remove", methods=["POST"])
def remove():
    if request.method != "POST":
        return 404

    id = request.form["id"]

    connection = get_conn()
    cursor = connection.cursor()

    try:
        cursor.execute("DELETE FROM agenda where id = %s;", id)
        connection.commit()
    except MySQLError as e:
        print(e)
        return "Error:(",400
    finally:
        cursor.close()
        connection.close()

    return redirect("show")

@app.route("/update", methods=["POST"])
def update():
    if request.method != "POST":
        return 404

    id = request.form["id"]
    firstName = request.form["name"]
    lastName = request.form["lastname"]

    connection = get_conn()
    cursor = connection.cursor()

    try:
        cursor.execute("UPDATE agenda SET name = %s, lastname = %s where id = %s;", (firstName, lastName, id))
        connection.commit()
    except MySQLError as e:
        print(e)
        return "Error:(",400
    finally:
        cursor.close()
        connection.close()

    return redirect("show")

if __name__ == "__main__":
    create_tables()
    app.run()
