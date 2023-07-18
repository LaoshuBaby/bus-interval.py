import time
from pprint import pprint

source="5:55、6:00*、6:20、6:40、7:00*、7:40、8:10、8:40、9:10*、9:40、10:10、10:40、11:10、11:40、12:20、13:00、13:30、14:00、14:30*、15:00、15:30、15:50*、16:10、16:30、16:50、17:20*、17:40、18:00、18:30、19:00。"

def parse(src:str)->dict:
    schedule=source.replace("*","").replace("。","").split("、")
    # pprint(times)
    schedule=[(lambda x:time.strptime(x, "%H:%M"))(t) for t in schedule]
    # pprint(times)
    intervals=[schedule[i]-schedule[i+1] if i!=len(schedule) else 0 for i in range(len(schedule))]
    print(intervals)


parse(source)