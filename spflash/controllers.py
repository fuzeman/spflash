from celery import Celery
from celery.exceptions import TimeoutError
from flask import Flask, Response, abort, request, render_template
import logging
import os

log = logging.getLogger(__name__)

app = Flask(__name__, template_folder='../templates', static_folder='../static')
cel = Celery()

cel.conf.update(
    BROKER_URL=os.environ.get('CELERY_BROKER', 'redis://localhost:6379'),
    CELERY_RESULT_BACKEND=os.environ.get('CELERY_BACKEND', 'redis://localhost:6379'),
)


@app.route('/<version>/get')
def get(version):
    ping = request.args.get('ping')

    if not ping:
        abort(400)

    log.debug("Waiting for result from worker...")
    task = cel.send_task('spflash.get', (version, ping), expires=10)

    try:
        pong = task.get(timeout=5)
        log.debug('Ping: "%s", Pong: "%s"', ping, pong)
    except TimeoutError:
        abort(503)

    return Response(pong, mimetype='text/plain')


@app.route('/<version>/host')
def host(version):
    return render_template('host.html', version=version)


@app.errorhandler(503)
def service_unavailable(e):
    return Response('', mimetype='text/plain'), 503
