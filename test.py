from flask import Flask, render_template, request
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

@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    per_page = 25
    data = read_csv('goodreads_data.csv')
    paginated_data = paginate(data, page, per_page)
    return render_template('dashboard.html', data=paginated_data, page=page)

if __name__ == '__main__':
    app.run(debug=True)
