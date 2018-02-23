from __future__ import absolute_import

from os import listdir

import werkzeug.exceptions
from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
from os.path import isdir, join

from web.datasets import DatasetJob
from web.webapp import scheduler
from . import images as dataset_images

blueprint = Blueprint(__name__, __name__)


@blueprint.route('/<job_id>', methods=['GET'])
def show(job_id):
    job = scheduler.get_job(job_id)
    if job is None:
        raise werkzeug.exceptions.NotFound('Job not found')
    related_jobs = scheduler.get_related_jobs(job)
    if isinstance(job, dataset_images.ImageDatasetJob):
        return dataset_images.views.show(job, related_jobs=related_jobs)
    else:
        raise werkzeug.exceptions.BadRequest('Invalid job type')


@blueprint.route('/summary', methods=['GET'])
def summary():
    try:
        datasets = get_dataset_list()
        return render_template('datasets/datasets.html', datasets=datasets)
    except TemplateNotFound:
        abort(404)


def get_dataset_list():
    return sorted([d for d in listdir('/data/datasets') if isdir(join('/data/datasets', d))])


def get_job_list(cls, running):
    return sorted(
        [j for j in scheduler.jobs.values() if isinstance(j, cls) and j.status.is_running() == running],
        key=lambda j: j.status_history[0][1],
        reverse=True,
    )