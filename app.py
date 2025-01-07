from flask import Flask, render_template, request, redirect, url_for, session
from supabase import create_client, Client
import os
from dotenv import load_dotenv
import bcrypt

load_dotenv()

app = Flask(__name__, static_folder='static')
app.secret_key = 'secret_key'  # Add secret key for session

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def is_logged_in():
    return session.get('logged_in', False)

@app.route('/')
def index():
    return render_template('coming_soon.html')


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
            user_response = supabase.table('users').select('*').eq('accounts_id', account_id).eq('email', email).execute()
            if user_response.data:
                hashed_password = user_response.data[0]['password'].encode('utf-8')
                if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
                    session['logged_in'] = True
                    session['account_id'] = user_response.data[0]['id']
                    return redirect(url_for('dashboard'))  # Redirect to dashboard after successful login
        # Handle login failure
        return render_template('login.html', error="Invalid account name, email, or password. Please try again.")
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        account_name = request.form['accountName']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirmPassword']
        plan = request.form['plan']

        # Check if passwords match
        if password != confirm_password:
            return render_template('register.html', error="Passwords do not match.")

        # Perform a case-insensitive check for existing account name
        account_response = supabase.table('accounts').select('id').ilike('account_name', account_name).execute()
        if account_response.data:
            return render_template('register.html', error="Account name already exists. Please choose a different name.")

        # Check if email already exists
        email_response = supabase.table('users').select('id').eq('email', email).execute()
        if email_response.data:
            return render_template('register.html', error="Email already exists.")

        # Create new account with selected plan
        new_account_response = supabase.table('accounts').insert({'account_name': account_name, 'plan': plan}).execute()
        if not new_account_response.data:
            return render_template('register.html', error="Failed to create account.")
        account_id = new_account_response.data[0]['id']

        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        # Create new user with account_id
        user_response = supabase.table('users').insert({'email': email, 'password': hashed_password.decode('utf-8'), 'accounts_id': account_id}).execute()
        if not user_response.data:
            return render_template('register.html', error="Failed to create user.")

        session['logged_in'] = True
        session['account_id'] = account_id
        return redirect(url_for('dashboard'))

    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('account_id', None)
    return redirect(url_for('index'))  # Redirect to index after logout

@app.route('/dashboard')
def dashboard():
    if not is_logged_in():
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/settings')
def settings():
    if not is_logged_in():
        return redirect(url_for('login'))
    return render_template('settings.html')

@app.route('/generate-images')
def generate_images():
    if not is_logged_in():
        return redirect(url_for('login'))
    return render_template('generate_images.html')

@app.route('/create-listing')
def create_listing():
    if not is_logged_in():
        return redirect(url_for('login'))
    return render_template('create_listing.html')

@app.route('/callback/amazon')
def amazon_callback():
    # This is where you will handle the OAuth response from Amazon
    # You will need to extract the authorization code from the request
    # and exchange it for an access token.
    code = request.args.get('code')
    if not code:
        return "Error: No code returned", 400

    # Exchange the authorization code for an access token
    # This will require sending a request to Amazon's token endpoint
    # You will need to include your client ID, client secret, and the code
    # received in this callback.

    # For now, just log the code
    print(f"Authorization code received: {code}")

    # Redirect the user back to the settings page or show a success message
    return redirect(url_for('settings'))

if __name__ == '__main__':
    app.run(debug=True)