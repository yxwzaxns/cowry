class Demo(object):
    """docstring for Demo."""
    def __init__(self):
        super(Demo, self).__init__()

        self.en = {'certificates': {'publickey': '/Users/ruby/workspace/git/cowry/client/pubkey/server.crt'},
 'database': {},
 'default': {'debug': 'True',
  'recv_cmd_buffer_size': '1024',
  'recv_file_buffer_size': '1024',
  'send_cmd_buffer_size': '1024',
  'send_file_buffer_size': '1024'},
 'storage': {'datapath': '/Users/ruby/workspace/git/cowry/server/data'}}

        self.c = self.to_object(self.en)

        # self.__dict__.keys['a'] = 'b'
        # self.__setattr__('a',self.c)
    @staticmethod
    def to_object(item):
        """
        Convert a dictionary to an object (recursive).
        """
        def convert(item):
            if isinstance(item, dict):
                return type('jo', (), {k: convert(v) for k, v in item.items()})
            if isinstance(item, list):
                def yield_convert(item):
                    for index, value in enumerate(item):
                        yield convert(value)
                return list(yield_convert(item))
            else:
                return item

        return convert(item)
