from datetime import datetime
from pprint import pprint

source = "5:55、6:00*、6:20、6:40、7:00*、7:40、8:10、8:40、9:10*、9:40、10:10、10:40、11:10、11:40、12:20、13:00、13:30、14:00、14:30*、15:00、15:30、15:50*、16:10、16:30、16:50、17:20*、17:40、18:00、18:30、19:00。"

def parse(src: str) -> dict:
    schedule_raw=source.replace("*", "").replace("。", "").split("、")
    # pprint(schedule_raw)
    schedule_obj = [
        (lambda x: datetime.strptime(x, "%H:%M"))(t)
        for t in schedule_raw
    ]
    # pprint(schedule_obj)
    intervals_raw = [
        int((schedule_obj[i + 1] - schedule_obj[i]).total_seconds() / 60)
        if i != len(schedule_obj) - 1
        else 0
        for i in range(len(schedule_obj))
    ]
    # pprint(intervals_raw)
    # 先进行段合并
    interval_parts=[]
    stay_pos=0
    current_pos=0
    for i in range(len(intervals_raw)):
        if i<len(intervals_raw)-1:
            if intervals_raw[current_pos+1]!=intervals_raw[current_pos]:
                interval_parts.append([(schedule_obj[stay_pos],schedule_obj[current_pos+1]),intervals_raw[current_pos]])
                stay_pos=current_pos+1
            current_pos+=1
    # pprint(interval_parts)
    from collections import Counter
    intervals_count = dict(Counter([i[1] for i in interval_parts]))
    # print(intervals_count)    
    default_interval=max(list(intervals_count.items()), key=lambda x: x[1])[0]
    # print(default_interval)
    print("opening_hours"+" = "+"Mo-Su "+schedule_obj[0].strftime("%H:%M")+"-"+schedule_obj[-1].strftime("%H:%M"))
    print("interval"+" = "+datetime.strptime(str(default_interval).zfill(2),"%M").strftime("%H:%M")) # not %M:%S
    print("interval:conditional"+" = "+"; ".join([datetime.strptime(str(t).zfill(2),"%M").strftime("%M:%S")+" @ "+"("+"Mo-Su "+",".join(["1"])+")" if t!=default_interval else "" for t in intervals_count]))

parse(source)
