from flask import Flask,render_template,request,flash,redirect
from flask_mysqldb import MySQL

app = Flask('__name__')
app.config['SECRET_KEY'] = '6127f1ba5f868bdb1bf50b7d63531766'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'user'

mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route("/register", methods = ['GET','POST'])
def register():
    if request.method == 'POST':
        details = request.form
        name = details['name']
        mail = details['email']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO info(name, email) VALUES (%s, %s)", (name, mail))
        mysql.connection.commit()
        cur.close()
        return render_template('register.html',success = "success")
    return render_template('register.html')

@app.route("/view",methods = ['GET','POST'])
def view():
    if request.method == 'POST':
        details = request.form
        n = details['name']
        n = str(n)
        cur = mysql.connection.cursor()
        #print("the name is ",n)
        sql_select_query = """select * from info where name = %s"""
        cur.execute(sql_select_query, (n, ))
        #cur.execute("SELECT * from info where name  = ",n)
        result = cur.fetchall()
        sql_select_query = """select count(*) from info where name = %s"""
        cur.execute(sql_select_query, (n, ))

        count = cur.fetchone()
        return render_template('view.html',result = result,count=count[0],success = "success")
    return render_template('view.html')

@app.route("/edit", methods = ['GET','POST'])
def edit():
    if request.method == 'POST':
        details = request.form
        n = details['name']
        cur = mysql.connection.cursor()
        sql_select_query = """select * from info where name = %s"""
        cur.execute(sql_select_query, (n, ))
        result = cur.fetchall()
        return render_template('edit.html',result = result)
    return render_template('edit.html')

@app.route("/realedit", methods = ['GET','POST'])
def realedit():
    if request.method == 'POST':
        details = request.form
        name = details['name']
        mail = details['email']
        cur = mysql.connection.cursor()
        #cur.execute("DELETE FROM info where name = %s and email = %s",(name, mail, ))
        cur.execute("UPDATE info set email = %s where name =%s", (mail, name))
        mysql.connection.commit()
        cur.close()
        return render_template('edit.html',success = "success")
    return render_template('edit.html')

@app.route("/delete", methods = ['GET','POST'])
def delete():
    if request.method == 'POST':
        details = request.form
        name = details['name']
        mail = details['email']
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM info where name = %s and email = %s",(name, mail, ))
        #cur.execute("UPDATE info set email = %s where name =%s", (mail, name))
        mysql.connection.commit()
        cur.close()
        return render_template('delete.html',success = "success")
    return render_template('delete.html')

@app.route("/editdelete", methods = ['GET','POST'])
def editdelete():
        if request.method == 'POST':
            details = request.form
            n = details['name']
            cur = mysql.connection.cursor()
            sql_select_query = """select * from info where name = %s"""
            cur.execute(sql_select_query, (n, ))
            result = cur.fetchall()
            return render_template('delete.html',result = result)
        return render_template('delete.html')

if __name__ == "__main__":
    app.run(debug=True)
