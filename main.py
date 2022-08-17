# sri
from flask import Flask, render_template, request
import mysql
import mysql.connector
app = Flask(__name__)

"""def prelims():
    con = mysql.connector.connect(
        host="localhost", user="root",
        password="", database="hayavadana")
    # create cursor object
    cursor = con.cursor()
    query1 = "desc college_details"
    cursor.execute(query1)
    table = cursor.fetchall()
    # describe table
    print('\n Table Description:')
    for attr in table:
        print(attr)
    # assign data query
    query2 = "select * from college_details"

    # executing cursor
    cursor.execute(query2)

    # display all records
    table = cursor.fetchall()

    # fetch all columns
    print('\n Table Data:')
    for row in table:
        print(row[0], end=" ")
        print(row[1], end=" ")
        print(row[2], end="\n")
    # closing cursor connection
    cursor.close()
    con.close()
    return None

"""

@app.route('/')
def hello_world():
    college_photo = "static/Global college.jpg"
    return render_template('landingpage.html', college_photo=college_photo)


@app.route("/saverecord",methods = ["POST","GET"])
def saveRecord():
    msg = "msg"
    if request.method == "POST":
        try:
            # all attributes
            name = request.form.get("name")
            gender = request.form.get("gender")
            email = request.form.get("email")
            usn = request.form.get("usn")
            phone = request.form.get("phone")
            branch = request.form.get("branch")
            semester = request.form.get("semester")
            floor_number = request.form.get("floor_number")
            room_number = request.form.get("room_number")
            city = request.form.get("city")

            # creating connection
            connection = mysql.connector.connect(
                host="localhost", user="root",
                password="", database="hayavadana")
            # cursor object
            cursor = connection.cursor()

            # inserting values
            queries = [
                f'INSERT INTO College_details(USN, branch, semester) values ("{usn}", "{branch}", "{semester}")',
                f'INSERT INTO Personal_details(USN, city) values ("{usn}", "{city}")'
            ]
            for query in queries:
                cursor.execute(query)
            connection.commit()
            msg = "Student details successfully Added"
        except:
            connection.rollback()
            msg = "We can not add Student details to the database"
        finally:
            return render_template("success_record.html",msg = msg)
            connection.close()


@app.route("/delete_student")
def delete_student():
    return render_template("delete_student.html")


@app.route("/student_info")
def student_info():
    connection = mysql.connector.connect(
        host="localhost", user="root",
        password="", database="hayavadana")
    # cursor object

    cursor = connection.cursor()
    cursor.execute("select * from Personal_details")
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template("student_info.html",rows = rows)


@app.route("/deleterecord",methods = ["POST"])
def deleterecord():
    usn = request.form["usn"]
    connection = mysql.connector.connect(
        host="localhost", user="root",
        password="", database="hayavadana")
    # cursor object
    cursor = connection.cursor()
    cursor.execute(f"select * from Personal_details where usn = ('{usn}')")
    rows = cursor.fetchall()
    if not rows == []:
        cursor.execute(f"delete from Personal_details where usn = ('{usn}')")
        cursor.close()
        connection.close()
        msg = "Student detail successfully deleted"
        return render_template("delete_record.html", msg=msg)
    else:
        msg = "Could not be deleted"
        cursor.close()
        connection.close()
        return render_template("delete_record.html", msg=msg)


app.run(debug=True)