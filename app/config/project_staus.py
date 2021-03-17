# Project Status Code
from enum import Enum


class ProjectStatus(Enum):
    ACTIVE = 1
    INACTIVE = 2
    DELETED = -1
