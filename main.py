from flask import Flask, request, render_template, redirect, url_for,send_file,session,Response
import os
import flask_login
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask import Flask, render_template, request, url_for, redirect, session, flash
from pymongo import MongoClient
from os import path
from werkzeug.security import generate_password_hash,check_password_hash
from werkzeug.utils import secure_filename
import datetime 
from bson import ObjectId


# create a Flask application instance  app
app = Flask(__name__)
app.secret_key = 'abcdefgh'  

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

client = MongoClient('mongodb://localhost:27017')
db = client['xopify']
user_collection = db['users']
order_collection = db['orders']


# Define the Order class
class Order():
    def __init__(self,user_email, file_path, file_name, dropdown_value, no_of_copies, review):
        self.user_email = user_email
        self.file_path = file_path
        self.file_name = file_name
        self.dropdown_value = dropdown_value
        self.no_of_copies = no_of_copies
        self.review = review
        self.created_date = datetime.now()


# Define the User class 
class User(UserMixin):
    def __init__(self, user_data):
        self.id = str(user_data['_id'])
        self.name = user_data['name']
        self.email = user_data['email']
        self.password_hash = user_data['password']
        self.contact_no = user_data.get('contact_no', None)
        self.enrollment_no = user_data.get('enrollment_no', None)
        
    
    
    @staticmethod
    def get(user_id):
        user_data = user_collection.find_one({'_id': ObjectId(user_id)})
        if user_data:
            return User(user_data)
        return None

    @staticmethod
    def find_by_email(email):
        user_data = user_collection.find_one({'email': email})
        if user_data:
            return User(user_data)
        return None


    


# Load a user  based on their email address
@login_manager.user_loader
def load_user(user_id):
    user_data = user_collection.find_one({'_id': ObjectId(user_id)})
    if user_data:
        return User(user_data)
    return None

# Load a user  based on their email address during login
@login_manager.request_loader
def load_user_from_request(request):
    email = request.form.get('email')
    if email:
        # user_data = collection.find({'email': email})
        user_data = user_collection.find_one({'email': email}, {'_id': 1, 'email': 1, 'password': 1,'name':1,'contact_no':1,'enrollment_no':1})

        if user_data:
            password = request.form.get('password')
            if password and check_password_hash(user_data['password'], password):
                return User(user_data)
    return None



@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        
        name = request.form.get('name')
        email = request.form.get('email')
        contact_no = request.form.get('contact')
        enrollment_no = request.form.get('enrollment')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm-password')
        
        # Check if the email is already registered
        existing_user = user_collection.find_one({'email': email})
        if existing_user:
            return redirect(url_for('login'))
            
        else:
            if password == confirm_password:
                password_hash = generate_password_hash(password, method='sha256')   
                form_data = {
            "name": name,
            "email": email,
            "contact_no":contact_no,
            "enrollment_no":enrollment_no,
            "password":password_hash
            }
            user_collection.insert_one(form_data)

        session['user_name'] = form_data['name']  
        session['user_email'] = form_data['email']

        return render_template('login.html')
    else:
        return render_template('signup.html')


        
        
        
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':

        email = request.form.get('login_email')
        password = request.form.get('login_password')
        session['user_email'] = email

        user_data = user_collection.find_one({'email': email}, {'_id': 1, 'email': 1, 'password': 1,'name':1,'contact_no':1,'enrollment_no':1})

        if user_data and check_password_hash(user_data['password'],password):
            user = User(user_data)
            login_user(user)
            session['user_id'] = user.id
            print("success")
            return redirect(url_for('dashboard'))

        else:
            return render_template('login.html')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    print('Logged out successfully!')
    return redirect(url_for('login'))


@app.route('/dashboard',methods=['GET','POST'])
def dashboard():
    
    user_email = session.get('user_email')

    # Check if the user is logged in
    if not user_email:
        # Handle the case where the user is not logged in or the session is expired
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        # Retrieve user email from the current logged-in user
        user_email = current_user.email

        # Check if the POST request has a file part
        file_path = "undefined"
        filename= "undefined"
        dropdown_value ="undefined"
        
        
        files = request.files.getlist("file")
        for file in files:
            # Extract relevant file information
            filename = file.filename
            print('path')
            current_script_directory = os.path.dirname(os.path.abspath(__file__))
            root_directory = os.path.dirname(current_script_directory)
            folder_name = "files"
            folder_path = os.path.join(root_directory, folder_name)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            # Save the file to the 'files_data' folder
            file_path = (os.path.join(folder_path, filename))    
            file.save(file_path)
        
        no_of_copies = request.form.get('copies')
        review = request.form.get('review')
        dropdown_value = request.form.get('dropdown_value')
        
        # Create orders and add them to the 'orders' collection
        
        order_data = {
                'user_email': user_email,
                'file_path': file_path,  # Store the file path in the database
                'file_name': filename,
                'dropdown_value': dropdown_value,
                'no_of_copies': int(no_of_copies),
                'review': review,
                'created_date': datetime.datetime.now(),
            }
        
        order_collection.insert_one(order_data)
        print(order_data)

        
        return redirect(url_for('dashboard'))

    return render_template('index.html')


@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('forgot_password_email')
        # Check if the email exists in the database
        user = user_collection.find_one({'email': email})
        print(user)
        if user:
            session['user_id'] = str(user['_id'])
            # Redirect the user to the password reset page
            return redirect(url_for('reset_password'))
        else:
            # Email not found in the database, show an error message
            flash('Email not found in our records.', 'error')
    return render_template('forgot_password.html')


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if 'reset_token' not in session:
        return redirect(url_for('forgot_password'))

    if request.method == 'POST':
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        user_id =  ObjectId(session['user_id'])
        user = user_collection.find_one({'_id':user_id})
        print(user)
        if new_password != confirm_password:
            print("both password must be diffrent")
                
        elif check_password_hash( user['password'],new_password):
            print('New password cannot be the same as the previous one.', 'error')
        else:
            # Update the user's password in the database
            user_id = ObjectId(session['user_id'])
            
            password_hash = generate_password_hash(new_password, method='sha256')   
            user_collection.update_one({'_id': user_id}, {'$set': {'password': password_hash}})
            print('Password reset successfully.', 'success')
            session.pop('user_id', None)
            return redirect(url_for('login'))

    return render_template('reset_password.html')

@app.route('/admin', methods=['GET','POST'])
def admin_login():
    if request.method =='POST':
        name = request.form['name']
        password =request.form['password']
        if name == 'xopify' and password == 'heet001':
            users = user_collection.find().sort('name', 1)
            return render_template('admin2.html', users=users)
        return redirect(url_for('admin'))
    return render_template('adminlogin.html')

@app.route('/admin/user/<user_email>', methods=['GET'])
def user_details(user_email):
    # Retrieve the user by user_id
    user = user_collection.find_one({'email': user_email})
    
    if user:
        # Retrieve the user's orders sorted by order_date in descending order
        orders = order_collection.find({'user_email': user_email}).sort('created_date', -1)
        print(orders)
        return render_template('user_page.html', user=user, orders=orders)
    else:
        return 'User not found', 404



@app.route('/download/<filename>')
def download_file(filename):
    # Construct the full path to the file
    current_script_directory = os.path.dirname(os.path.abspath(__file__))
    root_directory = os.path.dirname(current_script_directory)
    folder_name = "files"
    folder_path = os.path.join(root_directory, folder_name)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
         
    file_path = (os.path.join(folder_path, filename))
    # Check if the file exists
    if os.path.exists(file_path):
        # Use send_file to serve the file as an attachment for download
        return send_file(file_path, as_attachment=True)
    else:
        return 'File not found', 404

if __name__ == "__main__":
    app.run(debug=True)

