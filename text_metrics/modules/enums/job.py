from enum import Enum


class JobType(str, Enum):
    SearchProduct = 'SearchProduct'
    GetProductReviews = 'GetProductReviews'


class JobStatus(str, Enum):
    Pending = 'Pending'
    Dispatched = 'Dispatched'
    Processing = 'Processing'
    Completed = 'Completed'
    Failed = 'Failed'
    Discarded = 'Discarded'


class JobPriority(str, Enum):
    Low = 'Low'
    Normal = 'Normal'
    High = 'High'
    Realtime = 'Realtime'


class JobLogType(str, Enum):
    Info = 'Info'
    Warning = 'Warning'
    Error = 'Error'
