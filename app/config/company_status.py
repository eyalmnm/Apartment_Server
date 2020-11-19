# Company Status Code
from enum import Enum


class CompanyStatus(Enum):
    ACTIVE = 1
    INACTIVE = 2
    DELETED = -1
