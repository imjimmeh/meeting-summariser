from enum import Enum


class Status(Enum):
    NOT_STARTED = 0
    RUNNING = 1
    FINISHED = 2


class SummarisationStatus(Enum):
    NOT_STARTED = 0
    RECORDING_AND_TRANSCRIBING = 1
    FINISHING_RECORDING = 2
    SUMMARISING = 3
    FINISHED = 4
