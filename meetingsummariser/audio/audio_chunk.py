from datetime import datetime, timedelta
from typing import Callable, List

from ..models import Segment


class AudioChunk:
    filename: str
    start_time: datetime
    device_index: int
    segments: List[Segment] = []

    def __init__(self, filename: str, start_time: datetime, device_index: int):
        self.filename = filename
        self.start_time = start_time
        self.device_index = device_index

    def add_transcriptions(self, segments: List[Segment]):
        self.segments = self.filter_out_silent_segments(
            self.add_starttime_to_segment_times(segments)
        )

    def filter_out_silent_segments(self, segments: List[Segment]) -> List[Segment]:
        return [segment for segment in segments if not segment.is_silent]

    def add_starttime_to_segment_times(self, segments: List[Segment]) -> List[Segment]:
        for segment in segments:
            segment.start = self.start_time + timedelta(seconds=segment.start)
            segment.end = self.start_time + timedelta(seconds=segment.end)
        return segments


type AddAudioChunkToQueueCallabale = Callable[[AudioChunk], None]
