import threading
from time import sleep

from loguru import logger

from text_metrics.modules.enums.job import JobStatus
from text_metrics.modules.helpers.server.job_api import get_dispatched_jobs
from text_metrics.modules.helpers.terminal_helper import TerminalHelper
from text_metrics.modules.models.job import Job

import text_metrics.modules.tasks as tasks


class App:
    jobs: list[Job]

    def __init__(self):
        TerminalHelper()
        self.jobs = []

    def add_job(self, job: Job):
        if job.status != JobStatus.Pending:
            return
        for index, j in enumerate(self.jobs):
            if j.id == job.id:
                self.jobs[index] = job
                return
        self.jobs.append(job)

    def start(self):
        thread = threading.Thread(target=self.monitor)
        thread.start()
        thread = threading.Thread(target=self.dispatch)
        thread.start()

    def dispatch(self):
        while True:
            sleep(1)
            for job in self.jobs:
                if job.status == JobStatus.Pending:
                    logger.info(f"Dispatching job {job.id})")
                    tasks.search_product.delay(job)
                    self.jobs.remove(job)

    def monitor(self):
        logger.info("Starting monitor")

        while True:
            sleep(1)
            try:
                result = get_dispatched_jobs()
                if result.succeeded:
                    for job in result.data:
                        self.add_job(job)
                    if len(result.data) > 0:
                        logger.info(f"Found {len(result.data)} pending jobs")
            except Exception as e:
                logger.error(e)
        pass


app = App()
app.start()
