from flask import Flask, render_template, request
import csv
import sqlite3
import time

app = Flask(__name__)


# Query database for cities that match given criteria
def query_data(rank_min, rank_max, state):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    start_time = time.time()
    c.execute("SELECT City, State, Rank, Population FROM cities WHERE Rank BETWEEN ? AND ? AND State=?", (rank_min, rank_max, state))
    results = c.fetchall()
    end_time = time.time()
    time_taken = round(end_time - start_time, 2)
    conn.close()
    return results, time_taken

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    rank_min = int(request.form['rank_min'])
    rank_max = int(request.form['rank_max'])
    state = request.form['state']
    results, time_taken = query_data(rank_min, rank_max, state)
    return render_template('results.html', results=results, time_taken=time_taken)

if __name__ == '__main__':
    app.run(debug=True)
