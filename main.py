#import sqlite3
#db = sqlite3.connect("website.db")
from flask import Flask, request, render_template, redirect, url_for,send_file
import mysql.connector
import os


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="heet#1199",
  database="heet"
)



app = Flask(__name__)


mycursor = mydb.cursor()


@app.route('/', methods=['GET','POST'])

def insert():
    if request.method == 'POST':
        # Get the form data


        fname = request.form['fname']
        lname = request.form['lname']
        review = request.form['review']
        eno = request.form['enrollment']
        contact_no = request.form['contact']
        no_of_copies = request.form['copies']

        print(f"{fname}=={lname}=={eno}=={contact_no}=={review}=={no_of_copies}")

        if "dropdown_value" in request.form:
             dropdown_values = request.form['dropdown_value']
             sql = "INSERT INTO purchase (fname,lname,eno,review,copies,contact,dropdown_value) VALUES (%s, %s, %s, %s, %s, %s, %s)"
             val = (fname, lname, eno, review, no_of_copies, contact_no,dropdown_values)
             mycursor.execute(sql, val)
             mydb.commit()
             return render_template('index.html')

        else:

             sql = "INSERT INTO purchase (fname,lname,eno,review,copies,contact) VALUES (%s, %s, %s, %s, %s, %s)"
             val = (fname, lname, eno, review, no_of_copies, contact_no)
             mycursor.execute(sql, val)

             files = request.files.getlist("file")
             for file in files:
                 # Extract relevant file information
                 filename = file.filename

                 # Save the file to the 'files_data' folder
                 file_path = os.path.join("files_data", filename)
                 file.save(file_path)

                 sql2 = "INSERT INTO file_table (file_name, file_path) VALUES (%s, %s)"
                 val2 = (filename, file_path)
                 mycursor.execute(sql2, val2)

             mydb.commit()

             return render_template('index.html')


    else:
        return render_template("index.html")


@app.route('/admin', methods=['GET','POST'])
def check():
    if request.method =='POST':
        name = request.form['name']
        password =request.form['password']
        if name == 'xopify' and password == 'heet001':
            mycursor.execute("SELECT * FROM purchase")
            myresult = mycursor.fetchall()


            mycursor.execute("SELECT * FROM file_table")
            myfiletable = mycursor.fetchall()

            return render_template('admin2.html',users=myresult,files_table=myfiletable)
        else:
            return render_template('login.html')


    else:
        return render_template('login.html')


@app.route('/download/<int:file_id>')
def download(file_id):
    # Retrieve file information from the database

    mycursor.execute("SELECT * FROM file_table WHERE id = %s", (file_id,))
    file = mycursor.fetchone()


    if file:
        filename = file[1]
        file_data = file[2]
        return send_file(file_data)

    return "File not found."

if __name__ == "__main__":
    app.run(debug=True)

