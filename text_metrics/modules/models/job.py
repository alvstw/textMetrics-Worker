from dataclasses import dataclass
from datetime import datetime

from text_metrics.modules.enums.job import JobStatus, JobPriority, JobType


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
