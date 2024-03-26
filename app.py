from flask import Flask, render_template, request, redirect, url_for
import csv

app = Flask(__name__)

def read_csv(file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            data.append(row)
    return data

def paginate(data, page, per_page):
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    return data[start_idx:end_idx]
# Function to check if the username and password are valid
def check_credentials(username, password):
    with open('credentials.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == username and row[1] == password:
                return True
    return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup.html')
def signup():
    return render_template('signup.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if check_credentials(username, password):
        # Redirect to some page after successful login
        return redirect(url_for('success'))
    else:
        # Redirect back to login page with a message indicating invalid credentials
        return redirect(url_for('index', error='Invalid credentials'))

@app.route('/success')
def success():
    page = request.args.get('page', 1, type=int)
    per_page = 25
    data = read_csv('goodreads_data.csv')
    paginated_data = paginate(data, page, per_page)
    return render_template('dashboard.html', data=paginated_data, page=page)



if __name__ == '__main__':
    app.run(debug=True)
