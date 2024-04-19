def test_list(value):
    return isinstance(value, list)

class TestModule(object):

    def tests(self):
        return {
            'list': test_list
        }
