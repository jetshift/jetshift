import os
import platform

from flask import Flask, render_template, request, redirect, url_for
from redis import Redis
from rq import Queue
from dotenv import load_dotenv
from jetshift_core.helpers.common import run_job_in_new_process
from config.logging import logger

# Environment variables
load_dotenv()
redis_host = os.environ.get('REDIS_HOST', 'localhost')
redis_port = os.environ.get('REDIS_PORT', 6379)
job_queue = os.environ.get('JOB_QUEUE', 'False') == 'True'
operating_system = os.environ.get('OS', platform.system().lower())

# Set up Flask app
app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Set up Redis connection and RQ queue
if job_queue is True:
    logger.info(f'JSetting up RQ queue')
    redis_conn = Redis(host=redis_host, port=redis_port)
    rq_queue = Queue(connection=redis_conn)
else:
    rq_queue = None


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

    logger.info(f'Job Queue: {job_queue}')
    logger.info(f'Operating System: {operating_system}')

    if request.method == 'POST':
        selected_job = request.form.get('job')
        if selected_job in job_dict:
            module_name = f'jobs.{selected_job}'

            if job_queue is True and operating_system == 'linux':
                logger.info(f'Queueing job: {selected_job}')

                # Send the job to the RQ queue
                rq_queue.enqueue(run_job_in_new_process, module_name)
                job_completed = True
            else:
                job_completed = run_job_in_new_process(module_name)
        else:
            logger.error(f'Invalid job selected: {selected_job}')
            job_completed = False

        return redirect(url_for('run_job', j=selected_job, completed=job_completed))

    job_completed = request.args.get('completed', 'False') == 'True'
    return render_template('run_job.html', domain_name=domain_name, job_dict=job_dict, selected_job=selected_job, job_completed=job_completed)


if __name__ == '__main__':
    app.run()
