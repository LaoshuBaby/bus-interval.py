from datetime import datetime
from pprint import pprint


def parse(source: str) -> dict:
    schedule_raw = source.replace("*", "").replace("。", "").split("、")
    # pprint(schedule_raw)
    schedule_obj = [
        (lambda x: datetime.strptime(x, "%H:%M"))(t) for t in schedule_raw
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
    interval_parts = []
    stay_pos = 0
    current_pos = 0
    for i in range(len(intervals_raw)):
        if i < len(intervals_raw) - 1:
            if intervals_raw[current_pos + 1] != intervals_raw[current_pos]:
                interval_parts.append(
                    [
                        (
                            schedule_obj[stay_pos],
                            schedule_obj[current_pos + 1],
                        ),
                        intervals_raw[current_pos],
                    ]
                )
                stay_pos = current_pos + 1
            current_pos += 1
    # pprint(interval_parts)
    from collections import Counter

    intervals_count = dict(Counter([i[1] for i in interval_parts]))
    # print(intervals_count)
    default_interval = max(list(intervals_count.items()), key=lambda x: x[1])[
        0
    ]
    # print(default_interval)

    print("=" * 5 + "[PARSE RESULT]" + "=" * 15)
    print(
        "opening_hours"
        + " = "
        + "Mo-Su "
        + schedule_obj[0].strftime("%H:%M")
        + "-"
        + schedule_obj[-1].strftime("%H:%M")
    )
    print(
        "interval"
        + " = "
        + datetime.strptime(str(default_interval).zfill(2), "%M").strftime(
            "%H:%M"
        )
    )  # not %M:%S
    print(
        "interval:conditional"
        + " = "
        + "; ".join(
            [
                datetime.strptime(str(t).zfill(2), "%M").strftime("%M:%S")
                + " @ "
                + "("
                + "Mo-Su "
                + ", ".join(
                    list(
                        filter(
                            bool,
                            [
                                part[0][0].strftime("%H:%M")
                                + "-"
                                + part[0][1].strftime("%H:%M")
                                if part[1] == t
                                else None
                                for part in interval_parts
                            ],
                        )
                    )
                )
                + ")"
                if t != default_interval
                else ""
                for t in intervals_count
            ]
        )
    )


source = ""
parse(source if source != "" else input())
