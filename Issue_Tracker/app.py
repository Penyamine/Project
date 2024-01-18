from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
import mysql.connector
import hashlib
import re
import base64
import os

app = Flask(__name__, template_folder='templates')
app.secret_key = 'your_secret_key_here'

conn=mysql.connector.connect(host='127.0.0.1',password='peny',user='root',database='IssueTracker')
if conn.is_connected():
    print("Connection is Established")
cursor=conn.cursor()

@app.route("/", methods=['POST', 'GET'])
def dashboard():
    return render_template('home.html')


@app.route("/login", methods=['POST', 'GET'])
def login():
    msg = ''
    if (request.method == "POST"):
        email = request.form.get("email")
        password = request.form.get("password")
        sql = "SELECT * FROM USERN WHERE EMAIL=%s and password=%s"
        cursor.execute(sql,(email,password))
        account=cursor.fetchone()
        
        if account:
            session['Loggedin'] = True
            session['ID'] = account[0]
            session['USERNAME'] = account[2]
            msg = "logged Successfully"
            return render_template('/postComplaints.html', msg=' ')
        else:
            msg = "Incorrect Email/Password"
            return render_template('/login.html', msg=msg)
    
    return render_template('login.html', msg=msg)


@app.route("/adminLogin", methods=['POST', 'GET'])
def adminLogin():
    msg = ''
    if (request.method == "POST"):
        email = request.form.get("email")
        password = request.form.get("password")
        sql = "SELECT * FROM USERN WHERE EMAIL=%s and password=%s"
        cursor.execute(sql,(email,password))
        account=cursor.fetchone()
        
        if account:
            session['Loggedin'] = True
            session['ID'] = account[0]
            session['USERNAME'] = account[2]
            msg = "logged Successfully"
            return render_template('/adminHome.html', msg=msg)
        else:
            msg = "Incorrect Email/Password"
            return render_template('/adminLogin.html', msg=msg)
    return render_template('adminLogin.html', msg=msg)
    
@app.route("/agentLogin", methods=['POST', 'GET'])
def agentLogin():
    msg = ''
    if (request.method == "POST"):
        email = request.form.get("email")
        password = request.form.get("password")
        sql = "SELECT * FROM USERN WHERE EMAIL=? AND PASSWORD=?"
        cursor.execute(sql,(email,password))
        account=cursor.fetchone()
        
        if account:
            session['Loggedin'] = True
            session['ID'] = account[0]
            session['USERNAME'] = account[2]
            msg = "logged Successfully"
            return render_template('/agentHome', msg=msg)
        else:
            msg = "Incorrect Email/Password"
            return render_template('/agentLogin.html', msg=msg)
    return render_template('agentLogin.html', msg=msg)


@app.route("/register", methods=['POST', 'GET'])
def register():
    msg = ''
    print("hello")
    if (request.method == "POST"):
        print("Hello")
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        ROLE = 'USER'
        print(username+email+password)
        sql="select *from usern where email=%s and password=%s"
        cursor.execute(sql,(email,password))
        account=cursor.fetchone()

        print(account)
        if account:
            msg = "Your signup details  already exits please login"
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = "Invalid Email Address"
        else:
            sql = "SELECT COUNT(*) FROM USERN"
            cursor.execute(sql)
            result=cursor.fetchone()
            length=result[0] if result is not None  else 0
            # length=cursor.rowcount
            print(length)

            insert_sql = "INSERT INTO USERN (id,role,username,email,password)values(%s,%s,%s,%s,%s)"
            cursor.execute(insert_sql,(length+1,ROLE,username,email,password))
            conn.commit()
            msg = "You have  Successfully Registered !!!"
    print(msg)
    return render_template("register.html", msg=msg)

@app.route("/adminRegister", methods=['POST', 'GET'])
def adminRegister():
    msg = ''
    print("hello")
    if (request.method == "POST"):
        print("Hello")
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        ROLE = 'ADMIN'
        secret_key = request.form.get('secret')

        sql = "SELECT *FROM  USERN WHERE EMAIL='"+email+"' and  PASSWORD='"+password+"'"
        cursor.execute(sql)
        account=cursor.fetchone()
        print(account)
        if account:
            secret_key == "12345"
            msg = "Your signup details  already exits please login"
            return render_template("adminRegister.html", msg=msg)
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = "Invalid Email Address"
        else:
            secret_key = "12345"
            sql = "SELECT COUNT(*) FROM USERN"
            cursor.execute(sql)
            record=cursor.fetchone()
            length=record[0] if record[0] is not None else 0
            print(length)
 
            insert_sql = "INSERT INTO USERN(id,role,username,email,password) VALUES (%s,%s,%s,%s,%s)"
            cursor.execute(insert_sql,(length+1,ROLE,username,email,password))
            conn.commit()
            msg = "You have  Successfully Registered !!!"
            return render_template("adminRegister.html", msg=msg)
    print(msg)
    return render_template("adminRegister.html", msg=msg)

@app.route("/agentRegister", methods=['POST', 'GET'])
def agentRegister():
    msg = ''
    print("hello")
    if (request.method == "POST"):
        print("Hello")
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')
        secret_key = request.form.get('secret')
        print(role)

        sql = "SELECT *FROM  USERN WHERE EMAIL='"+email+"' AND PASSWORD='"+password+"'"
        cursor.execute(sql)
        account = cursor.fetchone()
        print(account)
        if account:
            msg = "Your signup details  already exits please login"
            return render_template("agentRegister.html", msg=msg)
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = "Invalid Email Address"
        else:
            sql = "SELECT COUNT(*) FROM USERN"
            cursor.execute(sql)
            record=cursor.fetchone()
            length=record[0] if record[0] is not None else 0
            print(length)
            
            insert_sql = "INSERT INTO USERN(id,role,username,email,password) VALUES (%s,%s,%s,%s,%s)"
            cursor.execute(insert_sql,(length+1,role,username,email,password))
            conn.commit()
            msg = "You have  Successfully Registered !!!"
            return render_template("agentRegister.html", msg=msg)
    print(msg)
    return render_template("agentRegister.html", msg=msg)

@app.route('/adminHome', methods=["POST", "GET"])
def adminHome():
    print("admin Home")
    sql = "SELECT USER_ID,USERNAME , IMAGE_ID,DESCRIPTION,PROGRESS,AFTER_IMAGE_ID FROM TICKETS WHERE PROGRESS = 'No' "
    cursor.execute(sql)
    
    data = []
    
    record = list(cursor.fetchall())
    for row in record:
        if row:
            row2=list(row)
            row2[2] = '../static/Uploads/' + row2[2]
            if row2[5]:
                row2[5] = '../static/Completed/' + row[5]
            data.append(tuple(row2))
        else:
            break
    return render_template("adminHome.html", data=data)


@app.route('/agentHome', methods=["POST", "GET"])
def agentHome():
    print("agent Home")
    EMAIL=request.form.get('email')
    data = []
    if EMAIL is not None:
        role_sql = "SELECT ROLE FROM USERN WHERE EMAIL = '"+EMAIL+"'"
        cursor.execute(role_sql)
        Role=cursor.fetchone()
        
        if Role:
            Role=Role[0]
            print(Role)
            sql = "SELECT USER_ID, IMAGE_ID, USERNAME, ADDRESS, PINCODE, DESCRIPTION FROM TICKETS WHERE ASSIGNED = '"+Role+"'"
            cursor.execute(sql)
            record=list(cursor.fetchall())

            for row in record:
                if row:
                    row2=list(row)
                    row2[1] = '../static/Uploads/' + row2[1]
                    data.append(tuple(row2))
                else:
                    break    
            for row in record:
                print(row)
    return render_template("agentHome.html", data=data)



@app.route('/assign-agent', methods=['POST'])
def assign_agent():
    print("This is assign agent")
    userId = request.form.get('userId')
    roleId = request.form.get('roleId')
    print(roleId)
    print(userId)
    sql = "UPDATE TICKETS SET ASSIGNED ='"+roleId+"' WHERE  USER_ID= '" + userId+"'"
    cursor.execute(sql)
    conn.commit()
    return redirect(url_for("adminHome"))

@app.route('/assignWork', methods=["POST", "GET"])
def assignWork():
    if request.method == "POST":
        userId = request.form.get("userId")
        print(userId)
        print(request.form)
        f = request.files['image']
        save_directory = os.path.join(app.root_path, 'static', 'Completed')
        f.save(os.path.join(save_directory, f.filename))
        progress = request.form['status']
        after_image_id = f.filename

        print(progress)
        print(after_image_id)
        print(userId)
        sql = "UPDATE TICKETS SET PROGRESS = '"+progress+"' WHERE  USER_ID= '" + userId+"'"
        cursor.execute(sql)
        # conn.commit()

        sql = "UPDATE TICKETS SET AFTER_IMAGE_ID ='"+after_image_id+"'  WHERE  USER_ID= '"+ userId+"'"
        cursor.execute(sql)
        conn.commit()
    return "Image Uploaded Successfully"

@app.route("/logout",methods=["POST","GET"])
def logout():
    session.pop('loggedin', None)
    session.pop('USERID', None)
    return render_template("home.html")

@app.route("/home",methods=["POST","GET"])
def home():
    return render_template("home.html")

@app.route('/postComplaints', methods=['POST', 'GET'])
def postComplaints():
    sql = "SELECT * FROM USERN WHERE ID=" + str(session['ID'])
    cursor.execute(sql)
    User=cursor.fetchone()
    
    if User[0] != '0':
        if request.method == "POST":
            f = request.files['image']
            print('FIle name is :',f.filename)
            if (len(f.filename)==0):
                print("No Image")
                return render_template('postComplaints.html', msg="Select the image")

            save_directory = os.path.join(app.root_path, 'static', 'Uploads')
            f.save(os.path.join(save_directory, f.filename))
            print(f.filename)
            IMAGE_ID = f.filename
            
            DESCRIPTION = request.form.get("description")
            ADDRESS = request.form.get("address")
            PINCODE = request.form.get("pincode")

            print(DESCRIPTION)
            print(ADDRESS)
            print(PINCODE)
            sql = "SELECT * FROM USERN WHERE ID=" + str(session['ID'])
            cursor.execute(sql)
            record=cursor.fetchall()
            for row in record:
                email=row[3]
                username=row[2]
                break
            print("email"+email)
            print("username"+username)
            assigned="NO"
            progress="NO"
            after_image_id="No Image due to not completion"
            sql="select count(*) from tickets"
            cursor.execute(sql)
            record=cursor.fetchone()
            length=record[0]if record is not None else 0

            print(length+1)


            sql="insert into tickets (user_id,username,email,assigned,description,progress,address,pincode,image_id,after_image_id) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql,(str(length+1),username,email,assigned,DESCRIPTION,progress,ADDRESS,str(PINCODE),IMAGE_ID,after_image_id))
            conn.commit()

        return render_template('postComplaints.html', msg="Your Complaints are provided to Successfully")

@app.route("/viewComplaints",methods=["post","GET"])
def viewComplaints():
        sql = "SELECT * FROM USERN WHERE ID=" + str(session['ID'])
        cursor.execute(sql)
        record=cursor.fetchall()
        for row in record:
            email=row[3]
            username=row[2]
            break
        #,ADDRESS ,PINCODE
        sql = "SELECT IMAGE_ID,PROGRESS,AFTER_IMAGE_ID,DESCRIPTION,ADDRESS,PINCODE  FROM TICKETS WHERE EMAIL = '"+email+"'"
        cursor.execute(sql)
        record=list(cursor.fetchone())
    
        data = []
        if record:
            record[0]= "../static/Uploads/" + str(record[0])
            record[2]="../static/Completed/"+str(record[2]) if record[2]!="NoImage" else "NoImage"
            data.append(record)
        return render_template("viewComplaints.html",data=data)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
