# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>

import datetime
import time


def dateOf(date):
    if isinstance(date, datetime.datetime):
        return datetime.datetime.strftime(date, '%m/%d/%Y %I:%M %p')
    elif isinstance(date, int):
        return time.strftime('%m/%d/%Y %I:%M %p', time.gmtime(date))
    return ""


def timeOf(time):
    if isinstance(time, int):
        return str(datetime.timedelta(seconds=time))
    return ""
