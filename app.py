import os
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)
app.secret_key = "secret"

app.config['MYSQL_HOST'] = os.environ.get("MYSQL_HOST", "localhost")
app.config['MYSQL_USER'] = os.environ.get("MYSQL_USER", "root")
app.config['MYSQL_PASSWORD'] = os.environ.get("MYSQL_PASSWORD", "")
app.config['MYSQL_DB'] = os.environ.get("MYSQL_DB", "geekprofile")
app.config['MYSQL_PORT'] = int(os.environ.get("MYSQL_PORT", 3306))

mysql = MySQL(app)


# Routes HTML existantes (conservées pour l'interface web)
@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            msg = 'Logged in successfully!'
            return render_template('index.html', msg=msg)
        else:
            msg = 'Incorrect username / password!'
    return render_template('login.html', msg=msg)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'address' in request.form and 'city' in request.form and 'country' in request.form and 'postalcode' in request.form and 'organisation' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        organisation = request.form['organisation']
        address = request.form['address']
        city = request.form['city']
        state = request.form['state']
        country = request.form['country']
        postalcode = request.form['postalcode']
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        account = cursor.fetchone()
        
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        else:
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s)', 
                          (username, password, email, organisation, address, city, state, country, postalcode))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('register.html', msg=msg)

@app.route("/index")
def index():
    if 'loggedin' in session:
        return render_template("index.html")
    return redirect(url_for('login'))

@app.route("/display")
def display():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
        return render_template("display.html", account=account)
    return redirect(url_for('login'))

@app.route("/update", methods=['GET', 'POST'])
def update():
    msg = ''
    if 'loggedin' in session:
        if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'address' in request.form and 'city' in request.form and 'country' in request.form and 'postalcode' in request.form and 'organisation' in request.form:
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']
            organisation = request.form['organisation']
            address = request.form['address']
            city = request.form['city']
            state = request.form['state']
            country = request.form['country']
            postalcode = request.form['postalcode']
            
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
            account = cursor.fetchone()
            
            if account and account['id'] != session['id']:
                msg = 'Account already exists!'
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                msg = 'Invalid email address!'
            elif not re.match(r'[A-Za-z0-9]+', username):
                msg = 'Username must contain only characters and numbers!'
            else:
                cursor.execute('UPDATE accounts SET username = %s, password = %s, email = %s, organisation = %s, address = %s, city = %s, state = %s, country = %s, postalcode = %s WHERE id = %s', 
                              (username, password, email, organisation, address, city, state, country, postalcode, session['id']))
                mysql.connection.commit()
                msg = 'You have successfully updated!'
        elif request.method == 'POST':
            msg = 'Please fill out the form!'
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
        return render_template("update.html", msg=msg, account=account)
    return redirect(url_for('login'))

# NOUVELLES ROUTES API POUR CURL
@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Username and password required'}), 400
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', 
                  (data['username'], data['password']))
    account = cursor.fetchone()
    
    if account:
        return jsonify({
            'success': True,
            'message': 'Logged in successfully',
            'user': {
                'id': account['id'],
                'username': account['username'],
                'email': account['email']
            }
        })
    else:
        return jsonify({'success': False, 'error': 'Invalid credentials'}), 401

@app.route('/api/register', methods=['POST'])
def api_register():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    required_fields = ['username', 'password', 'email', 'address', 'city', 'country', 'postalcode', 'organisation']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM accounts WHERE username = %s', (data['username'],))
    account = cursor.fetchone()
    
    if account:
        return jsonify({'error': 'Account already exists'}), 400
    
    if not re.match(r'[^@]+@[^@]+\.[^@]+', data['email']):
        return jsonify({'error': 'Invalid email address'}), 400
    
    if not re.match(r'[A-Za-z0-9]+', data['username']):
        return jsonify({'error': 'Username must contain only characters and numbers'}), 400
    
    cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s)', 
                  (data['username'], data['password'], data['email'], data['organisation'], 
                   data['address'], data['city'], data.get('state', ''), data['country'], data['postalcode']))
    mysql.connection.commit()
    
    return jsonify({'success': True, 'message': 'User registered successfully'})

@app.route('/api/users/<int:user_id>', methods=['GET'])
def api_get_user(user_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT id, username, email, organisation, address, city, state, country, postalcode FROM accounts WHERE id = %s', (user_id,))
    account = cursor.fetchone()
    
    if account:
        return jsonify({'success': True, 'user': account})
    else:
        return jsonify({'error': 'User not found'}), 404

@app.route('/api/users/<int:user_id>', methods=['PUT'])
def api_update_user(user_id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM accounts WHERE id = %s', (user_id,))
    account = cursor.fetchone()
    
    if not account:
        return jsonify({'error': 'User not found'}), 404
    
    # Vérifier si le username existe déjà pour un autre utilisateur
    if 'username' in data:
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND id != %s', (data['username'], user_id))
        existing_account = cursor.fetchone()
        if existing_account:
            return jsonify({'error': 'Username already exists'}), 400
    
    # Mettre à jour les champs
    update_fields = []
    update_values = []
    
    field_mapping = {
        'username': 'username',
        'password': 'password',
        'email': 'email',
        'organisation': 'organisation',
        'address': 'address',
        'city': 'city',
        'state': 'state',
        'country': 'country',
        'postalcode': 'postalcode'
    }
    
    for field, db_field in field_mapping.items():
        if field in data:
            update_fields.append(f"{db_field} = %s")
            update_values.append(data[field])
    
    if update_fields:
        update_values.append(user_id)
        query = f"UPDATE accounts SET {', '.join(update_fields)} WHERE id = %s"
        cursor.execute(query, update_values)
        mysql.connection.commit()
    
    return jsonify({'success': True, 'message': 'User updated successfully'})

@app.route('/api/users', methods=['GET'])
def api_get_all_users():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT id, username, email, organisation, city, country FROM accounts')
    accounts = cursor.fetchall()
    
    return jsonify({'success': True, 'users': accounts})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
