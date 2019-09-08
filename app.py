from collections import namedtuple
import http.cookiejar, urllib.request

from flask import Flask, render_template, redirect, url_for, request, json, session

from flaskext.mysql import MySQL
from flask import session as login_session
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '123456'
app.config['MYSQL_DATABASE_DB'] = 'Practice'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

#Message = namedtuple('Message', 'name username password')
#messages = []

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/reg', methods=['GET'])
def reg():
    return render_template('reg.html')#, messages=messages)

@app.route('/avt', methods=['GET'])
def avt():
    return render_template('avt.html')


@app.route('/Reg', methods=['POST'])
def Reg():
   # return 'Вы успешно зарегистрированы!!!'
    name = request.form['name']
    username = request.form['username']
    password = request.form['password']
    #messages.append(Message(name, username, password))


    conn = mysql.connect()
    cursor = conn.cursor()
    _hashed_password = generate_password_hash(password)
    cursor.callproc('sp_createUser', (name, username, _hashed_password))
    #return redirect(url_for('reg'))
    data = cursor.fetchall()

    if len(data) is 0:
        conn.commit()
       # p = 'User created successfully !'
        #return json.dumps({'message': 'User created successfully !'})
        #return render_template('index.html') #, 'User created successfully !')
        return redirect(url_for('avt'))
    else:
        return json.dumps({'error': str(data[0])})
        #return json.dumps({'Хуй тебе'})

@app.route('/Avt', methods=['POST'])
def Avt():
    try:
        username = request.form['username']
        password = request.form['password']

        # connect to mysql

        con = mysql.connect()
        cursor = con.cursor()
        cursor.callproc('sp_validateLogin', (username,))
        data = cursor.fetchall()

        if len(data) > 0:
            if check_password_hash(str(data[0][3]), password):
                session['user'] = data[0][0]
                return redirect('/userHome')
            else:
                return json.dumps({'message': 'Wrong Email address or Password.'})
                #return render_template('error.html', error='Wrong Email address or Password.')
        else:
            #return render_template('error.html', error='Wrong Email address or Password.')
            return json.dumps({'message': 'Wrong Email address or Password.'})


    except Exception as e:
       # return render_template({'message'}) #, error=str(e)})
       return json.dumps({'error': str(e)})
    finally:
        cursor.close()
        con.close()
    #return render_template('avt.html')

@app.route('/userHome')
def userHome():
    return render_template('userHome.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')
    #return render_template('index.html')