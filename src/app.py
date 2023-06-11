from flask import Flask, render_template, request
import pandas as pd
from main import main
import time

app = Flask(__name__)

def get_top_rows(resume, job_title, num_pages, conditions, top_k):
    df = main(resume, job_title, num_pages, conditions=conditions, top_k=top_k)
    # df = pd.read_csv("top_jobs.csv")
    # # wait 1 seconds
    # time.sleep(500)
    df = df.head(top_k)  # Filter top k rows
    df[['num_applications', 'salary_max', 'salary_min']] = df[['num_applications', 'salary_max', 'salary_min']].astype(int)
    return df

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        resume = request.form['resume']
        job_title = request.form['job_title']
        num_pages = int(request.form['num_pages'])
        top_k = int(request.form['top_k'])
        job_levels = request.form.getlist('job_levels[]')  # Retrieve selected job levels as a list
        df = get_top_rows(resume, job_title, num_pages, job_levels, top_k)
        return render_template('table.html', data=df)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')