import re

def dict_values(the_dict):
    return the_dict.values()

def match_dict_keys(the_dict, expression):
    ret = dict()
    p = re.compile(expression)
    for k, v in the_dict.iteritems():
        if p.search(k):
            ret[k] =v
    return ret

def ordered_dict_values(the_dict):
    return [val for key, val in sorted(the_dict.items())]

class FilterModule(object):
    def filters(self):
        return {
            'dict_values': dict_values,
            'match_dict_keys': match_dict_keys,
            'ordered_dict_values': ordered_dict_values,
        }

# vim: set ts=4 sts=4 sw=4 expandtab:
