import re

def match_subnets(subnets, expression):
    ret = []
    p = re.compile(expression)
    for k, v in subnets.iteritems():
        if p.search(k):
            ret.append(v['id'])
    return ret

class FilterModule(object):
    def filters(self):
        return {
            'match_subnets': match_subnets,
        }

# vim: set ts=4 sts=4 sw=4 expandtab:
