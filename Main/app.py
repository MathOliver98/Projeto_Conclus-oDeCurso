from flask import Flask, render_template, request, url_for, flash
from werkzeug.utils import redirect
from flaskext.mysql import MySQL


app = Flask(__name__)
mysql = MySQL(app)
app.secret_key = 'many random bytes'

app.config['MYSQL_HOST'] = '172.17.0.2'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'apple'
app.config['MYSQL_DB'] = 'crud'


@app.route('/')
def Index():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    data = cursor.fetchall()
    conn.commit()
    return render_template('index.html', students=data)


@app.route('/insert', methods = ['POST'])
def insert():
    if request.method == "POST":
        flash("Data Inserted Successfully")
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO students (name, email, phone) VALUES (%s, %s, %s)", (name, email, phone))
        conn.commit()
        return redirect(url_for('Index'))

@app.route('/delete/<string:id_data>', methods = ['GET'])
def delete(id_data):
    flash("Record Has Been Deleted Successfully")
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE id=%s", (id_data,))
    conn.commit()
    return redirect(url_for('Index'))



@app.route('/update', methods= ['POST', 'GET'])
def update():
    if request.method == 'POST':
        id_data = request.form['id']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("""
        UPDATE students SET name=%s, email=%s, phone=%s
        WHERE id=%s
        """, (name, email, phone, id_data))
        flash("Data Updated Successfully")
        return redirect(url_for('Index'))




if __name__ == "__main__":
    app.run(debug=True)
