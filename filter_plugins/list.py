import re

def is_list(value):
    return isinstance(value, list)

def list_match(value, expression):
    ret = []
    p = re.compile(expression)
    for v in value:
        if p.match(v):
            ret.append(v)
    return ret

def list_regex_replace(value, search, replace):
    p = re.compile(search)
    return [p.sub(replace, v) for v in value]

def list_search(value, expression):
    ret = []
    p = re.compile(expression)
    for v in value:
        if p.search(v):
            ret.append(v)
    return ret

def string_or_first_list_item(value):
    if isinstance(value, list):
        return value[0]
    else:
        return value

class FilterModule(object):
    def filters(self):
        return {
            'is_list': is_list,
            'list_match': list_match,
            'list_regex_replace': list_regex_replace,
            'list_search': list_search,
            'string_or_first_list_item': string_or_first_list_item
        }

# vim: set ts=4 sts=4 sw=4 expandtab:
