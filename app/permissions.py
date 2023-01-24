from enum import IntEnum, unique


@unique
class Permission(IntEnum):
    """Permission levels for users."""

    CAN_READ = 1
    CAN_CREATE = 2
    CAN_UPDATE = 3
    CAN_DELETE = 4
    CAN_RULE_THE_WORLD = 5
