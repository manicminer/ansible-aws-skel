import datetime
import dateutil.parser

def add_seconds(date, interval_seconds):
    return dateutil.parser.parse(date) + datetime.timedelta(seconds=interval_seconds)

def seconds_between(date1, date2):
    date1 = dateutil.parser.parse(date1)
    date2 = dateutil.parser.parse(date2)
    return (date1 - date2).total_seconds()

class FilterModule(object):
    def filters(self):
        return {
            'add_seconds': add_seconds,
            'seconds_between': seconds_between
        }

# vim: set ts=4 sts=4 sw=4 expandtab:
