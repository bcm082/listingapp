from flask import Flask, render_template, request, redirect, url_for
from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, static_folder='static')

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test-supabase')
def test_supabase():
    # Example of fetching data from a table named 'test_table'
    response = supabase.table('accounts').select('*').execute()
    return response.data if response.data else {"error": "No data found or an error occurred."}

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Handle login logic here
        username = request.form['username']
        password = request.form['password']
        # Add authentication logic
        return redirect(url_for('index'))  # Redirect to home after login
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Handle registration logic here
        account_name = request.form['accountName']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        # Add registration logic
        return redirect(url_for('login'))  # Redirect to login after registration
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)