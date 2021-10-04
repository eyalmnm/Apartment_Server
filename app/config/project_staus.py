# Project Status Code
from enum import Enum


class ProjectStatus(Enum):
    TEMP = 0
    ACTIVE = 1
    INACTIVE = 2
    DELETED = -1
