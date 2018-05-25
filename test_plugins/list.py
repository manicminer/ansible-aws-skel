def in_list(value, the_list):
    return value in the_list

class TestModule(object):
    ''' Ansible core jinja2 tests '''

    def tests(self):
        return {'in_list': in_list} 
