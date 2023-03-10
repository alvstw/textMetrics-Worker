from celery.utils.log import get_task_logger
from munch import DefaultMunch

from textmetrics.fetch import Fetcher
from textmetrics.modules.helpers.server.job_api import get_dispatched_jobs
from textmetrics.modules.models.job import Job
from textmetrics.worker import app

logger = get_task_logger(__name__)


@app.task
def monitor():
    logger.info("monitoring")
    pending_jobs = get_dispatched_jobs()


@app.task
def add(x, y):
    logger.info("Adding")
    return x + y


@app.task
def search_product(job: dict):
    job = DefaultMunch.fromDict(job)

    logger.info("Searching Product")
    fetcher = Fetcher()
    fetcher.search(job.payload, job_id=job.id)
    return job.payload
