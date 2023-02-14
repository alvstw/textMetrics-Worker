from dataclasses import dataclass
from datetime import datetime

from textmetrics.modules.enums.job import JobStatus, JobPriority, JobType


@dataclass
class Job:
    id: int
    type: JobType
    status: JobStatus
    priority: JobPriority
    name: str
    payload: str
    startedAt: datetime
    stoppedAt: datetime
    createdAt: datetime
    updatedAt: datetime
