# Users Status Code
from enum import Enum


class UserStatus(Enum):
    SUPER_ADMIN_USER = 1
    ADMIN_USER = 2
    SIMPLE_USER = 5
    SPECTATOR = 10
    DELETED = -1
