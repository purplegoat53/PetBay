from cassandra.cluster import Cluster
from cassandra.query import dict_factory

"""
    This file is heavily based off the bottle plugin tutorial:
        http://bottlepy.org/docs/dev/plugindev.html#plugin-example-sqliteplugin
"""

class CassandraPlugin(object):
    name = 'cassandra'
    api = 2

    def __init__(self, host=("127.0.0.1", 9042), keyspace=None, keyword='db'):
         self.host = host
         self.keyspace = keyspace
         self.keyword = keyword
         self.cluster = None
         self.session = None

    def getsession(self):
        return self.session

    def setup(self, app):
        ''' Make sure that other installed plugins don't affect the same
            keyword argument.'''
        for other in app.plugins:
            if not isinstance(other, CassandraPlugin): continue
            if other.keyword == self.keyword:
                raise PluginError("Found another sqlite plugin with " \
                "conflicting settings (non-unique keyword).")

        ip, port = self.host
        self.cluster = Cluster([ip], port=port)
        self.session = self.cluster.connect(self.keyspace)

    def close(self):
        self.cluster.shutdown()

    def apply(self, callback, context):
        if self.keyword not in context.get_callback_args():
            return callback

        def wrapper(*args, **kwargs):
            self.session.row_factory = dict_factory
            kwargs[self.keyword] = self.session

            return callback(*args, **kwargs)

        # Replace the route callback with the wrapped one.
        return wrapper
