from datetime import datetime
from pprint import pprint

source = "5:55、6:00*、6:20、6:40、7:00*、7:40、8:10、8:40、9:10*、9:40、10:10、10:40、11:10、11:40、12:20、13:00、13:30、14:00、14:30*、15:00、15:30、15:50*、16:10、16:30、16:50、17:20*、17:40、18:00、18:30、19:00。"


def parse(src: str) -> dict:
    schedule_raw=source.replace("*", "").replace("。", "").split("、")
    schedule_obj = [
        (lambda x: datetime.strptime(x, "%H:%M"))(t)
        for t in schedule_raw
    ]
    # pprint(times)
    intervals_raw = [
        int((schedule_obj[i + 1] - schedule_obj[i]).total_seconds() / 60)
        if i != len(schedule_obj) - 1
        else 0
        for i in range(len(schedule_obj))
    ]
    # pprint(intervals)
    intervals_count={}
    default_interval=0


parse(source)
