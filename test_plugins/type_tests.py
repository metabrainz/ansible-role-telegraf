def test_bool(value):
    return isinstance(value, bool)

def test_list(value):
    return isinstance(value, list)

class TestModule(object):

    def tests(self):
        return {
            'bool': test_bool,
            'list': test_list
        }
