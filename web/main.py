import json
import os
from flask import Flask, render_template, request, redirect, url_for
from redis import Redis
from rq import Queue
from dotenv import load_dotenv
from jetshift_core.helpers.clcikhouse import ping_clickhouse
from jetshift_core.helpers.common import run_job_in_new_process

app = Flask(__name__)
load_dotenv()

# Set up Redis connection and RQ queue
redis_conn = Redis(host='localhost', port=6379)  # Update with your Redis connection details
rq_queue = Queue(connection=redis_conn)


@app.route('/')
def index():
    full_host = request.host
    domain_name = full_host.split(':')[0]
    return render_template('index.html', domain_name=domain_name)


@app.route('/run-job', methods=['GET', 'POST'])
def run_job():
    full_host = request.host
    domain_name = full_host.split(':')[0]

    jobs_directory = 'jobs'
    py_files = [
        f.replace('.py', '') for f in os.listdir(jobs_directory)
        if f.endswith('.py') and f != '__init__.py' and not f.startswith('test_')
    ]
    job_dict = {f: f.replace('_', ' ').title() for f in py_files}
    selected_job = request.args.get('j', '')
    job_completed = False

    if request.method == 'POST':
        selected_job = request.form.get('job')
        if selected_job in job_dict:
            module_name = f'jobs.{selected_job}'

            operating_system = os.environ.get('OS', 'linux')
            if operating_system == 'windows':
                job_completed = run_job_in_new_process(module_name)
            else:
                # Enqueue the job to the RQ queue
                rq_queue.enqueue(run_job_in_new_process, module_name)
                job_completed = True

        return redirect(url_for('run_job', j=selected_job, completed=job_completed))

    job_completed = request.args.get('completed', 'False') == 'True'
    return render_template('run_job.html', domain_name=domain_name, job_dict=job_dict, selected_job=selected_job, job_completed=job_completed)


if __name__ == '__main__':
    app.run()
