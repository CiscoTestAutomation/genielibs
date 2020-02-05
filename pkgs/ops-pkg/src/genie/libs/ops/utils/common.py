import re


def get_enable(item):
    return True


def to_list(item):
    return [item]


def to_int(item):
    return int(item)


def convert_to_lower(item):
    return item.lower()


def convert_to_bool(item):
    if item and "up" in item.lower():
        return True
    else:
        return False


def get_state(item):
    item = item.lower()
    # Add more status when needed
    if item in ('up', 'ok'):
        return "up"
    elif (item in ('unknown',) or
          not item):
        return "down"


def convert_to_seconds(item):
    # 15 hours, 4 minutes
    p = re.compile(
                r"((?P<day>\d+) +(day|days), *)?"
                r"((?P<hour>\d+) +(hour|hours), *)?"
                r"((?P<minute>\d+) +(minute|minutes))|"
                r"((?P<second>\d+) +(seconds|seconds))$")
    m = p.match(item)
    if m:
        time_in_seconds = 0
        if m.groupdict()["day"]:
            time_in_seconds += int(m.groupdict()["day"]) * 86400
        if m.groupdict()["hour"]:
            time_in_seconds += int(m.groupdict()["hour"]) * 3600
        if m.groupdict()["minute"]:
            time_in_seconds += int(m.groupdict()["minute"]) * 60
        if m.groupdict()["second"]:
            time_in_seconds += int(m.groupdict()["second"])
    return time_in_seconds


def slot_num(item):
    r1 = re.compile(r'slot\s*(?P<slot>\d+)')
    result = r1.match(item)
    if result:
        item = result.groupdict()['slot']
        return item