import datetime

from ja_timex import TimexParser
import pendulum

from my_logging import *


def get_datetime_str(text: str) -> tuple[datetime, None]:
    now = pendulum.now()
    jst = now.in_timezone("Asia/Tokyo")
    timexes = TimexParser(reference=jst).parse(text)

    date_tpl = []
    time_tpl = []
    for t in timexes:
        if t.type == "DATE":
            date_tpl.append(t.to_datetime())
            continue
        elif t.type == "TIME":
            time_tpl.append(t)
            continue

    if len(date_tpl) == 0:
        return None, None

    d0 = pendulum.instance(date_tpl[0])
    txp = TimexParser(reference=d0)
    if len(time_tpl) == 0:
        begin = txp.parse("00:00")[0].to_datetime()
        end = begin + datetime.timedelta(hours=24)
    elif len(time_tpl) == 1:
        ts = txp.parse(time_tpl[0].text)
        begin = ts[0].to_datetime()
        end = begin + datetime.timedelta(hours=1)
    elif len(time_tpl) == 2:
        ts = txp.parse(time_tpl[0].text)
        begin = ts[0].to_datetime()
        ts = txp.parse(time_tpl[1].text)
        end = ts[0].to_datetime()
    else:
        return None, None

    logger.debug(f"{begin=}, {begin=}")
    return begin, end


if __name__ == "__main__":
    files = ("input1", "input2")
    for f in files:
        with open("samples/" + f) as f:
            text = f.read()
        print(f)
        get_datetime_str(text=text)
