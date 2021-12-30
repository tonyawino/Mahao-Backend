from enum import Enum


class FeedbackType(str, Enum):
    CLICK = "CLICK"
    VIEW = "VIEW"
    FAVORITE = "FAVORITE"
    READ = "READ"
    CALL = "CALL"
    TEXT = "TEXT"
    MAP = "MAP"
    SHARE = "SHARE"
