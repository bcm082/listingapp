from flask import Flask, render_template, request, redirect, url_for, session
from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, static_folder='static')
app.secret_key = 'secret_key'  # Add secret key for session

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Assuming you have some user authentication mechanism
# Mock function to check if user is logged in
def is_logged_in():
    return session.get('logged_in', False)

@app.route('/')
def index():
    return render_template('index.html')

# Testing Supabase Route
@app.route('/test-supabase')
def test_supabase():
    # Example of fetching data from a table named 'test_table'
    response = supabase.table('accounts').select('*').execute()
    return response.data if response.data else {"error": "No data found or an error occurred."}

@app.route('/dashboard')
def dashboard():
    if not is_logged_in():
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        account_name = request.form['accountName']
        email = request.form['email']
        password = request.form['password']
        # Query the accounts table to get the account ID
        account_response = supabase.table('accounts').select('id').eq('account_name', account_name).execute()
        if account_response.data:
            account_id = account_response.data[0]['id']
            # Query the users table with the account ID, email, and password
            user_response = supabase.table('users').select('*').eq('id', account_id).eq('email', email).eq('password', password).execute()
            if user_response.data:
                session['logged_in'] = True
                return redirect(url_for('dashboard'))  # Redirect to dashboard after successful login
        # Handle login failure
        return render_template('login.html', error="Invalid account name, email, or password. Please try again.")
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Handle registration logic here
        account_name = request.form['accountName']
        email = request.form['email']
        password = request.form['password']
        # Add registration logic
        session['logged_in'] = True  # Mock registration
        return redirect(url_for('dashboard'))  # Redirect to dashboard after registration
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))  # Redirect to index after logout

if __name__ == '__main__':
    app.run(debug=True)