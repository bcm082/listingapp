from flask import Flask, render_template
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

if __name__ == '__main__':
    app.run(debug=True)