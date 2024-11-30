from flask import Flask, render_template, request
import mysql.connector
from flask_cors import CORS
import json

mysql = mysql.connector.connect(
    user='web', password='webPass', host='127.0.0.1', database='student'
)
app = Flask(__name__)
CORS(app)

@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        cur = mysql.cursor()
        cur.execute(f"INSERT INTO students(studentName, email) VALUES('{name}', '{email}')")
        mysql.commit()
        return '{"Result":"Success"}'
    else:
        return render_template('add.html')

@app.route("/")
def hello():
    cur = mysql.cursor()
    cur.execute("SELECT * FROM students")
    rv = cur.fetchall()
    results = [{"Name": row[0], "Email": row[1], "ID": row[2]} for row in rv]
    return app.response_class(
        response=json.dumps({"Results": results, "count": len(results)}),
        status=200,
        mimetype='application/json'
    )

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8080', ssl_context=('cert.pem', 'privkey.pem'))
