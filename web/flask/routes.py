from flask import Blueprint, render_template, request, redirect, url_for
from web.flask.main import *
from jetshift_core.helpers.common import run_job_in_new_process

# Define Blueprint
main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    from web.flask.helpers import broadcast_message
    full_host = request.host
    domain_name = full_host.split(':')[0]

    # Start a background task to broadcast the message
    socketio.start_background_task(broadcast_message)

    return render_template('index.html', domain_name=domain_name)

@main_bp.route('/run-job', methods=['GET', 'POST'])
def run_job():
    full_host = request.host
    domain_name = full_host.split(':')[0]

    jobs_directory = 'app/jobs'
    py_files = [
        f.replace('.py', '') for f in os.listdir(jobs_directory)
        if f.endswith('.py') and f != '__init__.py' and not f.startswith('test_')
    ]
    available_jobs = {f: f.replace('_', ' ').title() for f in py_files}
    selected_job = request.args.get('j', '')

    logger.info(f'Job Queue: {job_queue}')
    logger.info(f'Operating System: {operating_system}')

    if request.method == 'POST':
        selected_job = request.form.get('job')
        if selected_job in available_jobs:
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
    return render_template('run_job.html', domain_name=domain_name, available_jobs=available_jobs, selected_job=selected_job, job_completed=job_completed)
